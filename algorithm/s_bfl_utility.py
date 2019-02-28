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
from algorithm.geo import Geo

# switch to variable mode 
def create_data(raw_data, sysnum, seed=None, out_file=None,
                plot_coords=False):
    """
    Create data for the Sorghum-BFL model.

    Parameters
    ----------
    raw_data : str or dict
        can be a *.yaml or *.json file name (str) or a dict object.
    sysnum : int
        system number.
    mode : str
        type of information available input file.
        options: paper, coordinates.
    seed : int, optional
        random seed.
    out_file : str, optional
        if specified write result to a YAML or JSON file named out_file.
    plot_coords : bool, optional
        plot all the coordinates.

    Variable name replacements
    T = num_weeks_horizon
    F = num_farms
    S = num_ssls
    a = harvested
    cfs = farm_ssl_trans_cost
    cs = ssl_refinery_trans_cost
    csk = fixed_cost_ssls
    ck = cost_ssls
    hf = farm_holding_cost
    hs = ssl_holding_cost
    d = demand
    u = upperbound_inventory
    ue = upperbound_equip_proc_rate

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

    num_weeks_horizon = raw['horizon']
    num_farms = raw['num_fields']
    num_ssls = raw['num_ssls']
    mode = raw['mode']

    # ========== coordinates, harvest, demand data ==========
    radius = raw['field']['radius']
    np.random.seed(seed=seed)
    if mode == "paper":
        # generates random ssl locations
        sites = np.random.uniform(-radius, radius, size=(2 * (num_farms + num_ssls), 2))
        sits_in = sites[np.sum(sites * sites, axis=1) <= radius**2]
        coord_farms = sits_in[:num_farms]
        coord_ssls = sits_in[-num_ssls:]
    elif mode == "coordinates":
        coord_farms = np.array(list(raw["Coord_f"].values()))
        coord_ssls = np.array(list(raw["Coord_s"].values()))
        refinery_location = raw["refinery_location"]
        assert len(coord_farms) == num_farms
        assert len(coord_ssls) == num_ssls

    if plot_coords:
        l1, = plt.plot(0, 'g^', markersize=7)
        l2, = plt.plot(*coord_ssls.T, 'ro', markersize=2)
        l3, = plt.plot(*coord_farms.T, 'bx', markersize=3)
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
    # what is the a_weight? Is it just a way of configuring the matrix? 
    a_weight = np.zeros(num_weeks_horizon + 1, dtype=int)
    a_weight[1:len(harvest_progress) + 1] = harvest_progress
    weekly_supply = a_weight / a_weight.sum() * total_supply
    field_weight = np.random.uniform(1, 10, size=num_farms)
    field_weight = field_weight / field_weight.sum()

    #if a is the amount harvested in farm f at time t why is it a single number here? 
    harvested = weekly_supply[:, None] * field_weight[None]
    harvested = harvested.round(0).astype(int)

    total_demand = raw['demand']
    demand = [0] + [int(total_demand / num_weeks_horizon)] * num_weeks_horizon

    # =================== system dependet data ==========================
    tran_coef = raw['cost']['transport_coef'] #raw is the input file
    equipments = raw['cost']['equipment']
    config = raw['configurations'][sysnum]
    dry_part = 1 - raw['moisture']
    equip_arr = list(product(range(1, 4), repeat=len(config) - 1))
    ssl_sizes = [int(i * dry_part) for i in raw['ssl_sizes']]
    # K is set of SSL types. Indexed by (SSL dry Mg size, # of each equipment)
    K = [(i, *j) for i in ssl_sizes for j in equip_arr]

    if 'whole_stalk' in config:
        # farm_unit_holding_cost
        farm_holding_cost = raw['price'] / raw['degrade']['whole_stalk']
    else:
        farm_holding_cost = raw['price'] / raw['degrade']['chopped']

    if 'bunker' in config:
        # ssl_unit_holding_cost
        ssl_holding_cost = raw['price'] / raw['degrade']['in_bunker']
    elif 'bagger' in config or 'module_former' in config:
        ssl_holding_cost = raw['price'] / raw['degrade']['in_bag']
    else:
        ssl_holding_cost = raw['price'] / raw['degrade']['chopped']

    # c_op = operating cost? 
    operating_cost = 0
    for e in config[1:]:
        if e == 'bunker':
            continue
        operating_cost += equipments[e][3]
    operating_cost /= dry_part
    operating_cost_jit = equipments['loadout'][3]
    operating_cost_jit += equipments['chopper'][3] if 'chopper' in config else 0
    operating_cost_jit /= dry_part

    # cost per Mg to transport from farm f to ssl s
    farm_ssl_trans_cost_rate = raw['cost']['base_infield'] / dry_part
    farm_ssl_trans_cost_rate *= tran_coef['whole_stalk'] if 'whole_stalk' in config else 1
    if mode == 'paper':
        farm_ssl_trans_cost = cdist(coord_farms, coord_ssls) * farm_ssl_trans_cost_rate
    elif mode == 'coordinates':
        geo = Geo()
        farm_ssl_trans_cost = geo.distance_points(coord_farms, coord_ssls) * farm_ssl_trans_cost_rate

    # Cost per Mg to send from ssl to refinery 
    ssl_refinery_trans_cost_jit_rate = ssl_refinery_trans_cost_rate = raw['cost']['base_highway'] / dry_part
    ssl_refinery_trans_cost_rate *= tran_coef['compressed'] if 'press' in config else 1
    ssl_refinery_trans_cost_rate *= tran_coef['in_module'] if 'module_former' in config else 1
 
    # use geolocation here, backward compatable (works with all ways it used to run)
    if mode =='paper':
        ssl_refinery_trans_cost = np.linalg.norm(coord_ssls, axis=1) * ssl_refinery_trans_cost_rate
        ssl_refinery_jit_trans_cost = np.linalg.norm(coord_ssls, axis=1) * ssl_refinery_trans_cost_jit_rate
    elif mode == 'coordinates':
        ssl_refinery_trans_cost = geo.distance_center(refinery_location, coord_ssls) * ssl_refinery_trans_cost_rate
        ssl_refinery_jit_trans_cost = geo.distance_center(refinery_location, coord_ssls) * ssl_refinery_trans_cost_jit_rate

    # UE upperbound equipment processing rate 
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

    # what is own_cost? owner cost? owner of what? 
    own_cost = {'bunker': raw['cost']['bunker_annual_own'] / 52 * num_weeks_horizon}
    for k, v in equipments.items():
        depreciation = (v[0] - v[2]) / v[1]
        interest = v[0] * raw['interest_rate']
        insurance_tax = (v[0] + v[2]) / 2 * (
            raw['insurance_rate'] + raw['tax_rate'])
        own_cost[k] = (depreciation + interest + insurance_tax) / 52 * num_weeks_horizon

    # cost per type of ssl
    cost_ssls = dict()
    for k in K:
        ssl_cost = k[0] * raw['cost']['ssl_annual_own'] / 52 * num_weeks_horizon
        equip_cost = [k[i + 1] * own_cost[e] for i, e in enumerate(config[1:])]
        cost_ssls[k] = int(ssl_cost + sum(equip_cost))

    # =================== output data ==========================
    all_data = {
        'Configuration': config,
        'Coord_farms': {i: v.tolist()
                    for i, v in enumerate(coord_farms)},
        'Coord_ssls': {i: v.tolist()
                    for i, v in enumerate(coord_ssls)},
        'K': {i: list(k)
              for i, k in enumerate(K)},
        'Seed': seed,
        'Sysnum': sysnum,
        'harvested': harvested.tolist(),
        'operating_cost': operating_cost,
        'operating_cost_jit': operating_cost_jit,
        # what is this the "price" of? 
        'c_pen': raw['price'] * 3,
        'farm_ssl_trans_cost': np.round(farm_ssl_trans_cost, 2).tolist(),
        'ssl_refinery_trans_cost': np.round(ssl_refinery_trans_cost, 2).tolist(),
        'ssl_refinery_jit_trans_cost': np.round(ssl_refinery_jit_trans_cost, 2).tolist(),
        'fixed_cost_ssls': [list(cost_ssls.values())] * num_ssls,
        'demand': demand,
        'farm_holding_cost': farm_holding_cost,
        'ssl_holding_cost': ssl_holding_cost,
        'upperbound_inventory': np.repeat(ssl_sizes, len(equip_arr)).tolist(),
        'upperbound_equip_proc_rate': list(UE.values()) * len(ssl_sizes),
        'upperbound_equip_proc_rate_jit': list(UE_jit.values()) * len(ssl_sizes)
    }
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
        # not sure about this metaVar
        metavar='T',
        type=float,
        default=60,
        # Looks like T was used for another purpose here
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