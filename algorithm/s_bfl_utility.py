# -*- coding: utf-8 -*-
"""
Created on Thu Sep 14 12:09:16 2017

@author: fangzhou
"""

import numpy as np
from scipy.spatial.distance import cdist
from itertools import product
import yaml
import json
from math import pi
import sys
import argparse
from matplotlib import pyplot as plt


def create_data(raw_data, sysnum, seed=None, out_file=None, plot_coords=False):
    """
    Create data for the Sorghum-BFL model.

    Parameters
    ----------
    raw_data : str or dict
        can be a *.yaml or *.json file name (str) or a dict object.
    sysnum : int
        system number.
    seed : int, optional
        random seed.
    out_file : str, optional
        if specified write result to a YAML or JSON file named out_file.
    plot_coords : bool, optional
        plot all the coordinates.

    Returns
    -------
    all_data : dict
        a dict object containing all the data for modeling.
    """
    # %%
    if type(raw_data) is str:
        with open(raw_data, 'r') as stream:
            if raw_data.split('.')[-1] == 'json':
                raw = json.load(stream)
            else:
                raw = yaml.load(stream)
    elif type(raw_data) is dict:
        raw = raw_data
    else:
        raise TypeError('raw_data must be str (filename) or dict.')

    T = raw['horizon']
    F = raw['num_fields']
    S = raw['num_ssls']

    # ========== coordinates, harvest, demand data ==========
    radius = raw['field']['radius']
    np.random.seed(seed=seed)
    sites = np.random.uniform(-radius, radius, size=(2 * (F + S), 2))
    sits_in = sites[np.sum(sites * sites, axis=1) <= radius**2]
    coord_f = sits_in[:F]
    coord_s = sits_in[-S:]

    if plot_coords:
        l1, = plt.plot(0, 'g^', markersize=7)
        l2, = plt.plot(*coord_s.T, 'ro', markersize=2)
        l3, = plt.plot(*coord_f.T, 'bx', markersize=3)
        plt.legend([l3, l2, l1], ['Farm', 'SSL', 'Bio-refinery'])
        circles = [
            plt.Circle((0, 0),
                       i * 10,
                       color='k',
                       fill=False,
                       linestyle='dotted',
                       linewidth=.5) for i in range(1, 6)
        ]
        [plt.gcf().gca().add_artist(circles[i]) for i in range(5)]
        plt.axis('equal')
        plt.show()

    harvest_progress = raw['harvest_progress']
    dry_yield = raw['field']['dry_yield']
    proportion_devoted = raw['field']['proportion_devoted']
    # 1 sqkm = 100 ha
    total_supply = 100 * pi * radius**2 * proportion_devoted * dry_yield
    a_weight = np.zeros(T + 1, dtype=int)
    a_weight[1:len(harvest_progress) + 1] = harvest_progress
    weekly_supply = a_weight / a_weight.sum() * total_supply
    field_weight = np.random.uniform(1, 10, size=F)
    field_weight = field_weight / field_weight.sum()
    a = weekly_supply[:, None] * field_weight[None]
    a = a.round(0).astype(int)

    total_demand = raw['demand']
    d = [0] + [int(total_demand / T)] * T

    # =================== system dependet data ==========================
    tran_coef = raw['cost']['transport_coef']
    equipments = raw['cost']['equipment']
    config = raw['configurations'][sysnum]
    dry_part = 1 - raw['moisture']
    equip_arr = list(product(range(1, 4), repeat=len(config) - 1))
    ssl_sizes = [int(i * dry_part) for i in raw['ssl_sizes']]
    # K is set of SSL types. Indexed by (SSL dry Mg size, # of each equipment)
    K = [(i, *j) for i in ssl_sizes for j in equip_arr]

    if 'whole_stalk' in config:
        hf = raw['price'] / raw['degrade']['whole_stalk']
    else:
        hf = raw['price'] / raw['degrade']['chopped']

    if 'bunker' in config:
        hs = raw['price'] / raw['degrade']['in_bunker']
    elif 'bagger' in config or 'module_former' in config:
        hs = raw['price'] / raw['degrade']['in_bag']
    else:
        hs = raw['price'] / raw['degrade']['chopped']

    c_op = 0
    for e in config[1:]:
        if e == 'bunker':
            continue
        c_op += equipments[e][3]
    c_op /= dry_part
    c_op_jit = equipments['loadout'][3]
    c_op_jit += equipments['chopper'][3] if 'chopper' in config else 0
    c_op_jit /= dry_part

    cfs_rate = raw['cost']['base_infield'] / dry_part
    cfs_rate *= tran_coef['whole_stalk'] if 'whole_stalk' in config else 1
    cfs = cdist(coord_f, coord_s) * cfs_rate

    cs_jit_rate = cs_rate = raw['cost']['base_highway'] / dry_part
    cs_rate *= tran_coef['compressed'] if 'press' in config else 1
    cs_rate *= tran_coef['in_module'] if 'module_former' in config else 1
    cs = np.linalg.norm(coord_s, axis=1) * cs_rate
    cs_jit = np.linalg.norm(coord_s, axis=1) * cs_jit_rate

    UE, UE_jit = dict(), dict()
    for v in equip_arr:
        caps_jit = [
            v[i] * equipments[e][4] for i, e in enumerate(config[1:])
            if e in ['loadout', 'chopper']
        ]
        caps_other = [
            v[i] * equipments[e][4] for i, e in enumerate(config[1:])
            if e not in ['loadout', 'chopper', 'bunker']
        ]
        if not caps_other:  # in case caps_other is empty
            caps_other = [max(caps_jit)]
        UE[v] = int(min(caps_other) * dry_part)
        UE_jit[v] = int(min(caps_jit) * dry_part)

    own_cost = {'bunker': raw['cost']['bunker_annual_own'] / 52 * T}
    for k, v in equipments.items():
        depreciation = (v[0] - v[2]) / v[1]
        interest = v[0] * raw['interest_rate']
        insurance_tax = (v[0] + v[2]) / 2 * (
            raw['insurance_rate'] + raw['tax_rate'])
        own_cost[k] = (depreciation + interest + insurance_tax) / 52 * T

    ck = dict()
    for k in K:
        ssl_cost = k[0] * raw['cost']['ssl_annual_own'] / 52 * T
        equip_cost = [k[i + 1] * own_cost[e] for i, e in enumerate(config[1:])]
        ck[k] = int(ssl_cost + sum(equip_cost))

    # =================== output data ==========================
    all_data = {
        'Configuration': config,
        'Coord_f': {i: v.tolist()
                    for i, v in enumerate(coord_f)},
        'Coord_s': {i: v.tolist()
                    for i, v in enumerate(coord_s)},
        'K': {i: list(k)
              for i, k in enumerate(K)},
        'Seed': seed,
        'Sysnum': sysnum,
        'a': a.tolist(),
        'c_op': c_op,
        'c_op_jit': c_op_jit,
        'c_pen': raw['price'] * 3,
        'cfs': np.round(cfs, 2).tolist(),
        'cs': np.round(cs, 2).tolist(),
        'cs_jit': np.round(cs_jit, 2).tolist(),
        'csk': [list(ck.values())] * S,
        'd': d,
        'hf': hf,
        'hs': hs,
        'u': np.repeat(ssl_sizes, len(equip_arr)).tolist(),
        'ue': list(UE.values()) * len(ssl_sizes),
        'ue_jit': list(UE_jit.values()) * len(ssl_sizes)
    }
    # %%
    if out_file is not None:
        with open(out_file, 'w') as f:
            if out_file.split('.')[-1] == 'json':
                json.dump(all_data, f)
            else:
                yaml.dump(all_data, f)
    return all_data


def check_filename(value):
    if value.split('.')[-1] not in ['json', 'yaml']:
        raise argparse.ArgumentTypeError(
            f"'{value}' does not end with '.json' or '.yaml'")
    return value


def cli_s_bfl():
    """
    command line interface for s_bfl
    """
    parser = argparse.ArgumentParser(description='Sorghum BFL model.')
    parser.add_argument(
        'input_file',
        type=check_filename,
        help="locate input file (must end with '.json' or '.yaml')")
    parser.add_argument(
        'sysnum', type=int, help='specify configuration number')
    parser.add_argument(
        '--jit', action='store_true', help='use hybrid delivery (base + jit)')
    parser.add_argument(
        '-t',
        '--t_lim',
        metavar='T',
        type=float,
        default=60,
        help='set computation time limit T in seconds (default: 60)')
    parser.add_argument(
        '--seed',
        metavar='S',
        type=int,
        default=None,
        help='set a random seed S.')
    parser.add_argument(
        '-o',
        '--out_file',
        metavar='O',
        type=check_filename,
        default=None,
        help="output to file O (must end with '.json' or '.yaml')")
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    args = parser.parse_args()
    return args