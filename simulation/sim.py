# -*- coding: utf-8 -*-
"""
Created on Fri Sep 21 20:22:27 2018

@author: 999Na
"""

import simpy
import json 
import numpy as np


# open input and output files to be used
with open("sim_example_data.json") as input_file: 
    input_data = json.load(input_file)
with open("example_output.json") as output_file: 
    output_data = json.load(output_file)
    
# assign variables from input file
SIM_TIME = 1040
num_harvest_trucks = input_data['harvest_input']['num_trucks_harvest']
carry_capacity = input_data['harvest_input']['carry_capacity']
truck_speed_high = input_data['harvest_input']['truck_speed_high']
truck_speed_low = input_data['harvest_input']['truck_speed_low']
harvest_time = input_data['harvest_input']['harvest_time']  
num_trucks_road = input_data['road_input']['num_trucks_road']
truck_capacity = input_data['road_input']['truck_capacity']
rtruck_speed_high = input_data['road_input']['rtruck_speed_high']
rtruck_speed_low = input_data['road_input']['rtruck_speed_low']

# assign variables from output file
coord_f = output_data['params']['Coord_f'] # coordinates x,y for farms (all possible)
coord_s = output_data['params']['Coord_s'] # coordinates x,y for ssl (all possible)
K = output_data['params']['K'] # ssl size and equipment loadout configurations
a = np.array(output_data['params']['a']) # 26 harvest schedule (yield for each farm in each period Mg)
d = output_data['params']['d'] # demand
u = output_data['params']['u'] # capacities for ssl
ue = output_data['params']['ue'] # processing rate of non-chopping methods

print(coord_f["3"][0])  #this is how we access

ssl = []
farms = []
m = a.shape[0]
n = a.shape[1]

print(n, " ",m)

# create functions      
def harvest(env, farms, a, m, n, harvest_trucks, refinery, carry_capacity):
    print(farms)
    
    print(n)
    for row in range(1,14):
        for col in range(n):
            farms[col].put(np.random.normal(a[row][col], 1/100*a[row][col]))
            print('Total amount in farm: ', col, ' ', farms[col].level)
            env.process(transport_harvest(env, farms[col], harvest_trucks, refinery, carry_capacity))
        yield env.timeout(40)
        print('Current time', env.now)

def ensilation():
    pass
   
def transport_harvest(env, farm, harvest_trucks, refinery, carry_capacity):
    while farm.level>carry_capacity:
        with harvest_trucks.request() as req:
            yield req
            farm.get(carry_capacity)
            print('Number of trucks busy: ', harvest_trucks.count)
            env.timeout(1)
            refinery.put(carry_capacity)  
    print('Amount in refinery: ', refinery.level)
       

def mylog(env, string):
   print(f'@{env.now}: {harvest_trucks.count} busy harvest tucks, ssl inventory={ssl.level}, {trucks.count} busy trucks, refinery inventory={refinery.level}| {string}')

# Define containers and resources and start process
env = simpy.Environment()

# create farms
for farm in range(n):
    farms.append(simpy.Container(env, 10000000, init=0))
    
harvest_trucks = simpy.Resource(env, capacity=num_harvest_trucks)
road_trucks = simpy.Resource(env, capacity=num_trucks_road)
refinery = simpy.Container(env, capacity=100000000, init=0)

env.process(harvest(env, farms, a, m, n, harvest_trucks, refinery, carry_capacity))
env.run(until=SIM_TIME)

