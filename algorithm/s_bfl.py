# -*- coding: utf-8 -*-
"""
Created on Wed Sep 13 10:10:09 2017

@author: fangzhou
"""

from algorithm.s_bfl_utility import create_data, cli_s_bfl
import logging
import os
import numpy as np
from itertools import product as setprod
from collections import Counter
from gurobipy import *
import json
import yaml

logger = logging.getLogger(__name__)

class s_bfl(object):
    def keyboard_terminate(self, model, where):
        try:
            pass
        except KeyboardInterrupt:
            model.terminate()
    
    def input(self, input_data, sysnum, t_lim = 30, jit=False, **kwargs):
        self.t_lim = t_lim
        self.jit = jit
        self.sysnum = sysnum
        self.params = create_data(input_data, self.sysnum, **kwargs)
        (*_, self.harvested, self.operating_cost, self.operating_cost_jit, self.c_pen, self.farm_ssl_trans_cost, self.ssl_refinery_trans_cost, self.ssl_refinery_jit_trans_cost, 
        self.fixed_cost_ssls, self.demand, self.farm_holding_cost, self.ssl_holding_cost, self.upperbound_inventory, self.upperbound_equip_proc_rate, self.upperbound_equip_proc_rate_jit) = self.params.values()

    def solve(self):
        # T, F, S, K : Set of time periods, farms, potential SSL sites, and available types of SSLs, respectively
        # t, f, s, k : element of T, F, S, K
        T = list(range(1, len(self.demand)))
        F = list(range(len(self.farm_ssl_trans_cost)))
        S = list(range(len(self.fixed_cost_ssls)))
        K = list(range(len(self.upperbound_inventory)))

        harvested = np.array(self.harvested)
        M = harvested.sum(axis=0)
        farm_ssl_cost_per_period = (np.array(self.farm_ssl_trans_cost) + self.operating_cost).tolist()
        jit_trans_costs = (np.array(self.ssl_refinery_jit_trans_cost)[None] + np.array(self.farm_ssl_trans_cost) + self.operating_cost_jit).tolist()

        logger.info("Parameters created. Begin building model.")

        m = Model('ms1m_base')

        # ++++++ Linear Programming Notation ++++++ 
        # ====== Create vars and objectives ======

        # w[s][k] = 1 => is an ssl of type k is built at site s; otherwise 0
        w = m.addVars(S, K, obj=self.fixed_cost_ssls, vtype='B', name='w')
        
        # y[f][s] = 1 => if farm f supplies ssl s; 0 otherwise
        y = m.addVars(F, S, vtype='B', name='y')
        
        shipped_farm_ssl = m.addVars(T, F, S, obj=farm_ssl_cost_per_period * len(T), name='shipped_farm_ssl')
        shipped_ssl_refinery = m.addVars(T, S, obj=self.ssl_refinery_trans_cost * len(T), name='shipped_ssl_refinery')
        
        # Note: inventory levels taken at the end of period t
        inventory_level_ssl = m.addVars([0] + T, S, obj=self.ssl_holding_cost, name='inventory_level_ssl')
        inventory_level_farm = m.addVars([0] + T, F, obj=self.farm_holding_cost, name='inventory_level_farm')
        
        if self.jit:
            z_jit = m.addVars(T, F, S, obj=jit_trans_costs * len(T), name='z_jit')
        penalty = m.addVars(T, obj=self.c_pen, name='penalty')

        m.setAttr('UB', inventory_level_ssl.select(0, '*'), [0] * len(S))
        m.setAttr('UB', inventory_level_farm.select(0, '*'), [0] * len(F))

        m.ModelSense = GRB.MINIMIZE

        # ====== Create constraints ======
        m.addConstrs((w.sum(s, '*') <= 1 for s in S), name='c1')
        m.addConstrs((y[f, s] <= w.sum(s, '*') for f in F for s in S), name='c2')
        m.addConstrs((y.sum(f, '*') == 1 for f in F), name='c3')
        m.addConstrs((inventory_level_ssl[t, s] == inventory_level_ssl[t - 1, s] - shipped_ssl_refinery[t, s] + shipped_farm_ssl.sum(t, '*', s)
                    for t in T for s in S),
                    name='c4')
        m.addConstrs((inventory_level_ssl[t, s] <= quicksum([self.upperbound_inventory[k] * w[s, k] for k in K]) for t in T
                    for s in S),
                    name='c7')
        m.addConstrs((shipped_farm_ssl.sum(t, '*', s) <= quicksum([self.upperbound_equip_proc_rate[k] * w[s, k] for k in K])
                    for t in T for s in S),
                    name='c9a')
        if not self.jit:
            m.addConstrs((inventory_level_farm[t, f] == inventory_level_farm[t - 1, f] + harvested[t, f] - shipped_farm_ssl.sum(t, f, '*')
                        for t in T for f in F),
                        name='c5')
            m.addConstrs((shipped_ssl_refinery.sum(t, '*') + penalty[t] == self.demand[t] for t in T),
                        name='c6')
            m.addConstrs(
                (shipped_farm_ssl.sum('*', f, s) <= M[f] * y[f, s] for f in F for s in S),
                name='c8')
            m.addConstrs(
                (shipped_farm_ssl.sum(t, '*', s) <= quicksum([self.upperbound_equip_proc_rate_jit[k] * w[s, k] for k in K])
                for t in T for s in S),
                name='c9b')
        else:
            m.addConstrs((inventory_level_farm[t, f] == inventory_level_farm[t - 1, f] + harvested[t, f] - shipped_farm_ssl.sum(t, f, '*') -
                        z_jit.sum(t, f, '*') for t in T for f in F),
                        name='c5')
            m.addConstrs(
                (z_jit.sum(t, '*', '*') + shipped_ssl_refinery.sum(t, '*') + penalty[t] == self.demand[t]
                for t in T),
                name='c6')
            m.addConstrs(
                (z_jit.sum('*', f, s) + shipped_farm_ssl.sum('*', f, s) <= M[f] * y[f, s]
                for f in F for s in S),
                name='c8')
            m.addConstrs((z_jit.sum(t, '*', s) + shipped_farm_ssl.sum(t, '*', s) <= quicksum(
                [self.upperbound_equip_proc_rate_jit[k] * w[s, k] for k in K]) for t in T for s in S),
                        name='c9b')
        logger.info("Model created. Begin solving.")

        # ====== Solve ======
        # m.update()
        # m.write('ms1m_grb.lp')
        # m.setParam('MIPGap', 0.01)
        m.setParam('TimeLimit', self.t_lim)
        m.setParam('Threads', 6)
        m.update()
        if not os.path.exists('warm_starts/'):
            os.makedirs('warm_starts/')
        else:
            if os.path.isfile(f'warm_starts/base_{self.sysnum}.mst'):
                m.read(f'warm_starts/base_{self.sysnum}.mst')
            if os.path.isfile(f'warm_starts/hybrid_sys{self.sysnum}.mst'):
                m.read(f'warm_starts/hybrid_sys{self.sysnum}.mst')
        m.optimize()

        logger.info("Model solved. Begin post-processing.")

        # ====== Result ======
        status = {
            1: 'LOADED',
            2: 'OPTIMAL',
            3: 'INFEASIBLE',
            7: 'ITERATION_LIMIT',
            8: 'NODE_LIMIT',
            9: 'TIME_LIMIT',
            10: 'SOLUTION_LIMIT',
            11: 'INTERRUPTED'
        }

        if m.SolCount:
            m.write('warm_starts/start.mst')
            if self.jit:
                m.write(f'warm_starts/hybrid_sys{self.sysnum}.mst')
            else:
                m.write(f'warm_starts/base_sys{self.sysnum}.mst')

            cost_total_lb = m.objBound
            # Total cost
            cost_total = m.objVal
            gap = (cost_total - cost_total_lb) / cost_total
            # what does cost locations mean? 
            cost_loc = w.prod({(s, k): self.fixed_cost_ssls[s][k] for s in S for k in K}).getValue()

            cost_op = shipped_farm_ssl.sum().getValue() * self.operating_cost
            cfs_dict = {(t, f, s): self.farm_ssl_trans_cost[f][s] for t, f, s in setprod(T, F, S)}

            # cost of transporting from f to s in time t
            cost_tran_fs = shipped_farm_ssl.prod(cfs_dict).getValue()
            cost_tran_sr = shipped_ssl_refinery.prod({(t, s): self.ssl_refinery_trans_cost[s]
                                    for t in T for s in S}).getValue()
            if self.jit:
                cost_op += z_jit.sum().getValue() * self.operating_cost_jit
                cost_tran_fs += z_jit.prod(cfs_dict).getValue()
                cost_tran_sr += z_jit.prod({(t, f, s): self.ssl_refinery_jit_trans_cost[s]
                                            for t in T for f in F
                                            for s in S}).getValue()

            cost_inv_S = inventory_level_ssl.sum().getValue() * self.ssl_holding_cost
            cost_inv_F = inventory_level_farm.sum().getValue() * self.farm_holding_cost

            K_cnt = dict(Counter(k for s in S for k in K if w[s, k].x > 0.5))
            jit_amount = z_jit.sum().getValue() if self.jit else np.nan

            # maybe a function for getting all the variables that are active and convert to lat, lng? 
            # getActiveRoutes()
            # Binary encoding of open ssls
            solution = [[v.VarName, v.X] for v in m.getVars() if v.X > 1e-6]
            summary = dict()
            summary['others'] = {
                'status': status[m.status],
                'CPU_time': m.runtime,
                'gap': gap,
                'available_types_ssl': len(K),
                'num_weeks_horizon': len(T),
                'num_farms': len(F),
                # I'm not super sure about the ssl one
                'num_ssls_considered': len(S),
                'num_ssls_used': w.sum().getValue(),
                'SSL_type_cnt': K_cnt,
            }
            summary['cost'] = {
                'total_lb': cost_total_lb,
                'total_ub': cost_total,
                'penalty': penalty.sum().getValue(),
                'operation': cost_op,
                'loc_own': cost_loc,
                'tran_farms_ssl': cost_tran_fs,
                'tran_ssl_refinery': cost_tran_sr,
                'farm_inventory': cost_inv_F,
                'ssl_inventory': cost_inv_S,
            }
            harvested_sum = float(harvested.sum())
            summary['per_dry_Mg'] = {
                k: v / harvested_sum
                for k, v in summary['cost'].items()
            }
            summary['trans_amount'] = {
                'base_fs': shipped_farm_ssl.sum().getValue(),
                'base_sb': shipped_ssl_refinery.sum().getValue(),
                # 'jit': jit_amount
            }

            # logger.info(args_str + yaml.dump(summary, default_flow_style=False))

            # self.optimization_result = {'params': self.params,'solution': solution, 'summary': summary}
            self.optimization_result = {'summary': summary}

if __name__ == '__main__':
    if not logger.hasHandlers():
        stream_handler = logging.StreamHandler()
        file_handler = logging.FileHandler('RunLog.log')
        formatter = logging.Formatter(
            fmt='%(asctime)s %(filename)s:%(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S')
        file_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)
        logger.addHandler(file_handler)
        logger.setLevel(logging.DEBUG)

    args = cli_s_bfl()
    s_bfl(
        args.input_file,
        args.sysnum,
        t_lim=args.t_lim,
        jit=args.jit,
        seed=args.seed,
        out_file=args.out_file)
#    s_bfl('cundiff_input.yaml', 2, t_lim=60, jit=True, out_file='outout.yaml')