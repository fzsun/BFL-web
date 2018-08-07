#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 30 21:01:11 2018

@author: Fangzhou Sun
"""
import numpy as np
from scipy.spatial import distance_matrix
from gurobipy import *
import itertools
import yaml, json

class tsp(object):
    def from_num_cities(self, n=20, length=100, seed=1):
        np.random.seed(seed)
        self.num_cities = n
        self.coords = np.random.uniform(-length, length, size=(n,2)).tolist()

        self.dist_mat = distance_matrix(self.coords, self.coords).tolist()
    def dump(self, filename='', fmt='json'):
        """
        Default: dump JSON as string
        """
        if filename:
            with open(f'{filename}.{fmt}', 'w') as outfile:
                if fmt == 'json':
                    json.dump(self.all_data_, outfile, sort_keys=True, indent=4)
                elif fmt == 'yaml':
                    yaml.dump(self.all_data_, outfile)
        else:
            return json.dumps(self.all_data_)
    def solve(self):
        def subtourelim(model, where):
            '''Callback - use lazy constraints to eliminate sub-tours'''
            try:
                if where == GRB.Callback.MIPSOL:
                    # make a list of edges selected in the solution
                    vals = model.cbGetSolution(model._vars)
                    selected = tuplelist((i,j) for i,j in model._vars.keys() if
                                         vals[i,j] > 0.5)
                    # find the shortest cycle in the selected edge list
                    tour = subtour(selected)
                    if len(tour) < n:
                        # add subtour elimination constraint for every pair of cities in tour
                        model.cbLazy(quicksum(model._vars[i,j] for
                                              i,j in itertools.combinations(tour, 2))
                                             <= len(tour)-1)
            except KeyboardInterrupt:
                model.terminate()

        def subtour(edges):
            '''Given a tuplelist of edges, find the shortest subtour'''
            unvisited = list(range(n))
            cycle = range(n+1) # initial length has 1 more city
            while unvisited: # true if list is non-empty
                thiscycle = []
                neighbors = unvisited
                while neighbors:
                    current = neighbors[0]
                    thiscycle.append(current)
                    unvisited.remove(current)
                    neighbors = [j for i,j in edges.select(current,'*') if j in unvisited]
                if len(cycle) > len(thiscycle):
                    cycle = thiscycle
            return cycle

        m = Model()
        dist = {(i,j) : self.dist_mat[i][j] for i in range(self.num_cities) for
                 j in range(self.num_cities) if j>i}
        n = self.num_cities
        vars = m.addVars(dist.keys(), obj=dist, vtype=GRB.BINARY, name='e')
        for i,j in vars.keys():
            vars[j,i] = vars[i,j] # edge in opposite direction
        m.addConstrs(vars.sum(i,'*') == 2 for i in range(n))

        m._vars = vars
        m.Params.lazyConstraints = 1
        m.setParam('Threads',6)

        m.optimize(subtourelim)

        vals = m.getAttr('x', vars)
        selected = tuplelist((i,j) for i,j in vals.keys() if vals[i,j] > 0.5)

        tour = subtour(selected)
        self.runtime_ = m.Runtime
        self.obj_ = m.objVal
        self.tour_ = tour
        self.all_data_ = {'coords':self.coords,
                          'tour': self.tour_,
                          'obj': self.obj_,
                          'runtime': self.runtime_}


if __name__ == '__main__':
    tt = tsp()
    tt.from_num_cities()
    tt.solve()


