# -*- coding: utf-8 -*-
"""
Created on Sun Nov 11 16:58:23 2018

@author: 999Na
"""


import simpy
import json 
import numpy as np
import re
import math 

# Define containers and resources and start process
env = simpy.Environment()

# open input and output files to be used
with open("sim_example_data.json") as input_file: 
    input_data = json.load(input_file)
with open("example_output.json") as output_file:
    output_data = json.load(output_file)
with open("example_input.json") as algo_input:
    algo_input_data = json.load(algo_input)
    
# assign variables from algo input
horizon = algo_input_data['horizon']
demand = algo_input_data['demand']
    
# assign variables from input file
SIM_TIME = 1041
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
solutions = output_data['solution'] # holds the algorithms solution dictionary

farms = []
m = a.shape[0]
n = a.shape[1]

# create farms
for farm in range(n):
    farms.append(simpy.Container(env, 10000000, init=0))
refinery = simpy.Container(env, capacity=100000000, init=0)

ssl_container = {} # dictionary relating ssl site location to container with proper capacity
ssl_location = {} # x,y location of ssl
ssl_route = [] # distance from ssl to orgin (refinery)
farm_route = [] # distance from farm n to designated ssl
farm_ssl = {} # shows which farm corresponds to using which ssl
farm_transport_schedule = [] # dictionary with keys=period and value s= dictionary with amount and time
ssl_transport_schedule = []

# create the farm transport schedule list of lists
for period in range(m):
    farm_transport_schedule.append([])
    for farm in range(len(farms)):
        farm_transport_schedule[period].append(0)

for coord in coord_s:
    ssl_route.append(math.sqrt(coord_s[coord][1]**(2)+coord_s[coord][0]**(2)))

# create the ssl containers from algorithm solution
for solution in solutions:
    aa = solution[0]
    cc = solution[1]
    bb = re.split('\W', aa)
    if bb[0] == 'w':
        ssl_container.update({bb[1]:simpy.Container(env,capacity=K[bb[2]][0], init=0)})
        ssl_location.update({bb[1]:coord_s[bb[1]]})
 
# create the ssl transportation schedule list of lists      
for period in range(m):
    ssl_transport_schedule.append([])
    for ssl in range(len(coord_s)):
        ssl_transport_schedule[period].append(0)
    
    
for solution in solutions:
    aa = solution[0]
    cc = solution[1]
    bb = re.split('\W', aa)
    if bb[0] == 'y':
        farm_route.append(math.sqrt((ssl_location[bb[2]][0]-coord_f[bb[1]][0])**(2)+(ssl_location[bb[2]][1]-coord_f[bb[1]][1])**(2)))
        farm_ssl.update({int(bb[1]):int(bb[2])})
    if bb[0] == 'zfs':  # populate the farm transport schedule from algorithm solution
        farm_transport_schedule[int(bb[1])][int(bb[2])] = cc
    if bb[0] == 'zs':   # populate the ssl transportation schedule from algorithm solution
        ssl_transport_schedule[int(bb[1])][int(bb[2])] = cc

# create functions      
def harvest(env, farms, a, m, n, refinery, farm_transport_schedule):
    total=0
    for period in range(m):
        print('total=',total)
        for farm in range(n):
            if a[period][farm] != 0:
                farms[farm].put(np.random.normal(a[period][farm], 1/100*a[period][farm]))
                total = total + np.random.normal(a[period][farm], 1/100*a[period][farm])
                env.process(transport_harvest(env, farms, refinery, farm_transport_schedule, period, farm))
            else:
                pass
            
        yield env.timeout(40)
        print('Current time', env.now)
    
def ensilation():
    pass
 
def transport_harvest(env, farms, refinery, farm_transport_schedule, period, farm):  
    x = farm_transport_schedule[period][farm]
    if x > 0:
        farms[farm].get(x)
        ssl_container[str(farm_ssl[farm])].put(x)
    else:
        pass
    yield env.timeout(0)
       
def moniter_ssl(env, ssl_transport_schedule):
    for period in range(m):
        for ssl in range(len(coord_s)):
            env.process(refinery_transport(env, ssl_transport_schedule[period][ssl], ssl, period))
        yield env.timeout(40)
        mylog(env,'period is over')
        
def refinery_transport(env, amount, ssl, period):
    x=int(amount)
    if x > 0:
        ssl_container[str(ssl)].get(x)
        refinery.put(x)
    else:
        pass
    yield env.timeout(0)
    mylog(env,'')   

def mylog(env, string):
   print(f'@{env.now}: refinery inventory={refinery.level}| {string}')

env.process(harvest(env, farms, a, m, n, refinery, farm_transport_schedule))
env.process(moniter_ssl(env,ssl_transport_schedule))
env.run(until=SIM_TIME)