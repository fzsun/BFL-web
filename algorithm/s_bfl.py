# -*- coding: utf-8 -*-
"""
Created on Wed Sep 13 10:10:09 2017

@author: fangzhou
"""

from s_bfl_utility import create_data, cli_s_bfl
import logging
import os
import numpy as np
from itertools import product as setprod
from collections import Counter
from gurobipy import *
import json
import yaml

class s_bfl(object):
    def keyboard_terminate(self, model, where):
        try:
            pass
        except KeyboardInterrupt:
            model.terminate()


    logger = logging.getLogger(__name__)


    def s_bfl(self, input_data, sysnum, t_lim=60, jit=False, out_file=None, **kwargs):
        """
        Solve the Sorghum-BFL problem instance.

        Parameters
        ----------
        input_data : str or dict
            can be a *.yaml or *.json file name (str) or a dict object.
        sysnum : int
            system number.
        out_file : str, optional
            if specified write return value to a YAML or JSON file named out_file.
        kwargs : other keywords in my_utility.create_data()
            including seed and plot_coords.

        Returns
        -------
        ret : dict
            a dict object containing three sub-dicts params, solution, summary.

            params is all the model parameters converted from input_data.

            solution is all the decision variables and the optimal values.

            summary is a summary of the solution.
        """
        func_args = locals()
        args_str = yaml.dump(func_args, default_flow_style=True, width=np.inf)

        logger.info(f"Code begins with {args_str} ")
        params = create_data(input_data, sysnum, **kwargs)
        (*_, a, c_op, c_op_jit, c_pen, cfs, cs, cs_jit, csk, d, hf, hs, U, UE,
        UE_jit) = params.values()

        T = list(range(1, len(d)))
        F = list(range(len(cfs)))
        S = list(range(len(csk)))
        K = list(range(len(U)))
        a = np.array(a)
        M = a.sum(axis=0)
        c_zfs = (np.array(cfs) + c_op).tolist()
        c_z_jit = (np.array(cs_jit)[None] + np.array(cfs) + c_op_jit).tolist()

        logger.info("Parameters created. Begin building model.")

        m = Model('ms1m_base')

        # ====== Create vars and objectives ======
        w = m.addVars(S, K, obj=csk, vtype='B', name='w')
        y = m.addVars(F, S, vtype='B', name='y')
        zfs = m.addVars(T, F, S, obj=c_zfs * len(T), name='zfs')
        zs = m.addVars(T, S, obj=cs * len(T), name='zs')
        Is = m.addVars([0] + T, S, obj=hs, name='Is')
        If = m.addVars([0] + T, F, obj=hf, name='If')
        if jit:
            z_jit = m.addVars(T, F, S, obj=c_z_jit * len(T), name='z_jit')
        penalty = m.addVars(T, obj=c_pen, name='penalty')

        m.setAttr('UB', Is.select(0, '*'), [0] * len(S))
        m.setAttr('UB', If.select(0, '*'), [0] * len(F))

        m.ModelSense = GRB.MINIMIZE

        # ====== Create constraints ======
        m.addConstrs((w.sum(s, '*') <= 1 for s in S), name='c1')
        m.addConstrs((y[f, s] <= w.sum(s, '*') for f in F for s in S), name='c2')
        m.addConstrs((y.sum(f, '*') == 1 for f in F), name='c3')
        m.addConstrs((Is[t, s] == Is[t - 1, s] - zs[t, s] + zfs.sum(t, '*', s)
                    for t in T for s in S),
                    name='c4')
        m.addConstrs((Is[t, s] <= quicksum([U[k] * w[s, k] for k in K]) for t in T
                    for s in S),
                    name='c7')
        m.addConstrs((zfs.sum(t, '*', s) <= quicksum([UE[k] * w[s, k] for k in K])
                    for t in T for s in S),
                    name='c9a')
        if not jit:
            m.addConstrs((If[t, f] == If[t - 1, f] + a[t, f] - zfs.sum(t, f, '*')
                        for t in T for f in F),
                        name='c5')
            m.addConstrs((zs.sum(t, '*') + penalty[t] == d[t] for t in T),
                        name='c6')
            m.addConstrs(
                (zfs.sum('*', f, s) <= M[f] * y[f, s] for f in F for s in S),
                name='c8')
            m.addConstrs(
                (zfs.sum(t, '*', s) <= quicksum([UE_jit[k] * w[s, k] for k in K])
                for t in T for s in S),
                name='c9b')
        else:
            m.addConstrs((If[t, f] == If[t - 1, f] + a[t, f] - zfs.sum(t, f, '*') -
                        z_jit.sum(t, f, '*') for t in T for f in F),
                        name='c5')
            m.addConstrs(
                (z_jit.sum(t, '*', '*') + zs.sum(t, '*') + penalty[t] == d[t]
                for t in T),
                name='c6')
            m.addConstrs(
                (z_jit.sum('*', f, s) + zfs.sum('*', f, s) <= M[f] * y[f, s]
                for f in F for s in S),
                name='c8')
            m.addConstrs((z_jit.sum(t, '*', s) + zfs.sum(t, '*', s) <= quicksum(
                [UE_jit[k] * w[s, k] for k in K]) for t in T for s in S),
                        name='c9b')

        logger.info("Model created. Begin solving.")

        # ====== Solve ======
        # m.update()
        # m.write('ms1m_grb.lp')
        # m.setParam('MIPGap', 0.01)
        m.setParam('TimeLimit', t_lim)
        m.setParam('Threads', 6)
        m.update()
        if not os.path.exists('warm_starts/'):
            os.makedirs('warm_starts/')
        else:
            if os.path.isfile(f'warm_starts/base_{sysnum}.mst'):
                m.read(f'warm_starts/base_{sysnum}.mst')
            if os.path.isfile(f'warm_starts/hybrid_sys{sysnum}.mst'):
                m.read(f'warm_starts/hybrid_sys{sysnum}.mst')
        m.optimize(keyboard_terminate)

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
            if jit:
                m.write(f'warm_starts/hybrid_sys{sysnum}.mst')
            else:
                m.write(f'warm_starts/base_sys{sysnum}.mst')

            cost_total_lb = m.objBound
            cost_total = m.objVal
            gap = (cost_total - cost_total_lb) / cost_total
            cost_loc = w.prod({(s, k): csk[s][k] for s in S for k in K}).getValue()

            cost_op = zfs.sum().getValue() * c_op
            cfs_dict = {(t, f, s): cfs[f][s] for t, f, s in setprod(T, F, S)}
            cost_tran_fs = zfs.prod(cfs_dict).getValue()
            cost_tran_sb = zs.prod({(t, s): cs[s]
                                    for t in T for s in S}).getValue()
            if jit:
                cost_op += z_jit.sum().getValue() * c_op_jit
                cost_tran_fs += z_jit.prod(cfs_dict).getValue()
                cost_tran_sb += z_jit.prod({(t, f, s): cs_jit[s]
                                            for t in T for f in F
                                            for s in S}).getValue()

            cost_inv_S = Is.sum().getValue() * hs
            cost_inv_F = If.sum().getValue() * hf

            K_cnt = dict(Counter(k for s in S for k in K if w[s, k].x > 0.5))
            jit_amount = z_jit.sum().getValue() if jit else np.nan

            solution = [[v.VarName, v.X] for v in m.getVars() if v.X > 1e-6]
            summary = dict()
            summary['others'] = {
                'status': status[m.status],
                'CPU_time': m.runtime,
                'gap': gap,
                'K': len(K),
                'T': len(T),
                'F': len(F),
                'S': len(S),
                'num_SSL': w.sum().getValue(),
                'SSL_type_cnt': K_cnt,
            }
            summary['cost'] = {
                'lb': cost_total_lb,
                'ub': cost_total,
                'penalty': penalty.sum().getValue(),
                'operation': cost_op,
                'loc_own': cost_loc,
                'tran_fs': cost_tran_fs,
                'tran_sb': cost_tran_sb,
                'inv_f': cost_inv_F,
                'inv_s': cost_inv_S,
            }
            a_sum = float(a.sum())
            summary['per_dry_Mg'] = {
                k: v / a_sum
                for k, v in summary['cost'].items()
            }
            summary['trans_amount'] = {
                'base_fs': zfs.sum().getValue(),
                'base_sb': zs.sum().getValue(),
                'jit': jit_amount
            }

            logger.info(args_str + yaml.dump(summary, default_flow_style=False))

            ret = {'params': params, 'solution': solution, 'summary': summary}
            if out_file:
                with open(out_file, 'w') as f:
                    if out_file.split('.')[-1] == 'json':
                        json.dump(ret, f)
                    else:
                        yaml.dump(ret, f)
                logger.info(f"Output {out_file} saved.\n")
            return ret
        else:
            logger.info(f"{status[m.status]}\n")


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