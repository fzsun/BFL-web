# -*- coding: utf-8 -*-
"""
Created on Sun Nov 11 16:58:23 2018

@author: 999Na
"""
'''


Perfect transport from ssl => should yield a max of 199991.99 Mg

Total transport from farm to ssl can yield a max of 202672.0000000001 Mg

'''

import simpy
import json 
import numpy as np
import re
import math 
import matplotlib.pyplot as plt
import pprint as pp


# Define containers and resources and start process
env = simpy.Environment()


'''
Data Creation Section
'''


# open input and output files to be used
with open("example_output1.json") as output_file:
    output_data = json.load(output_file)
with open("example_input.json") as algo_input:
    algo_input_data = json.load(algo_input)
    
log = open('log.txt','w+')
    
# assign variables from algo input
horizon = algo_input_data['horizon']
demand = algo_input_data['demand']
equipment_data = algo_input_data['cost']['equipment']
degredation = algo_input_data['degrade']

SIM_TIME = 1081

# assign variables from output file
coord_f = output_data['params']['Coord_f'] # coordinates x,y for farms (all possible)
coord_s = output_data['params']['Coord_s'] # coordinates x,y for ssl (all possible)
K = output_data['params']['K'] # ssl size and equipment loadout configurations
a = np.array(output_data['params']['a']) # 26 harvest schedule (yield for each farm in each period Mg)
d = output_data['params']['d'] # demand
u = output_data['params']['u'] # capacities for ssl
ue = output_data['params']['ue'] # processing rate of non-chopping methods
solutions = output_data['solution'] # holds the algorithms solution dictionary
configuration = output_data['params']['Configuration']


config_rate_standard = {} #rate the equipment works on a per hour basis
config_rate = {}
num_ssl = len(coord_s)
loadout_rates = []
loadout_rates_jit = []
for equipment in configuration:
    if equipment == 'loadout':
        loadout_rate_standard = equipment_data[equipment][4]/40
    if equipment == 'press':
        config_rate.update({'press':equipment_data[equipment][4]/40})
    if equipment == 'chopper':
        config_rate.update({'chopper':equipment_data[equipment][4]/40})
    if equipment == 'bagger':
        config_rate.update({'bagger':equipment_data[equipment][4]/40})
    if equipment == 'module_former':
        config_rate.update({'module_former':equipment_data[equipment][4]/40})
    if equipment == 'module_hauler':
        loadout_rate_module = equipment_data[equipment][4]/40
    
    
farms = []
m = a.shape[0]
n = a.shape[1]


# create farms
for farm in range(n):
    farms.append(simpy.Container(env, 10000000, init=0))
refinery = simpy.Container(env, capacity=100000000, init=0)

before_ssl = {}
ssl_container = {} # dictionary relating ssl site location to container with proper capacity
equip_in_ssl = {} # dictionary for ssl configuration
ssl_location = {} # x,y location of ssl
ssl_route = [] # distance from ssl to orgin (refinery)
farm_route = [] # distance from farm n to designated ssl
farm_ssl = {} # shows which farm corresponds to using which ssl
farm_transport_schedule = [] 
ssl_transport_schedule = [] 
jit_farm_transport = [] 
jit_ssl_transport = []
harvest_actual = []
ssl_inventory = []


# create the farm transport schedule list of lists
for period in range(m):
    farm_transport_schedule.append([])
    harvest_actual.append([])
    jit_farm_transport.append([])
    for farm in range(n):
        harvest_actual[period].append(0)
        farm_transport_schedule[period].append(0)
        jit_farm_transport[period].append(0)

for coord in coord_s:
    ssl_route.append(math.sqrt(coord_s[coord][1]**(2)+coord_s[coord][0]**(2)))
    

# create the ssl containers from algorithm solution
for solution in solutions:
    aa = solution[0]
    cc = solution[1]
    bb = re.split('\W', aa)
    if bb[0] == 'w':
        equip_in_ssl[bb[1]] = K[bb[2]][1:]
        before_ssl[bb[1]] = simpy.Container(env,capacity=K[bb[2]][0], init=0)
        ssl_container[bb[1]] = simpy.Container(env,capacity=K[bb[2]][0], init=0)
        ssl_location[bb[1]] = coord_s[bb[1]]

   
# create the ssl transportation schedule list of lists      
for period in range(m):
    ssl_transport_schedule.append([])
    jit_ssl_transport.append([])
    ssl_inventory.append([])
    for ssl in range(num_ssl):
        ssl_transport_schedule[period].append(0)
        jit_ssl_transport[period].append(0)
        ssl_inventory[period].append(0)
        
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
    if bb[0] == 'z_jit':
        jit_farm_transport[int(bb[1])][int(bb[2])] = cc
    if bb[0] == 'Is':
        ssl_inventory[int(bb[1])][int(bb[2])] = cc
 

'''
Functions Section
'''

       
# create functions      
def harvest(env, farms):
    for period in range(m):
        for farm in range(n):
            if a[period][farm] != 0:
                harvest_actual[period][farm]=max(0,np.random.normal(a[period][farm], 1/5*a[period][farm]))
                farms[farm].put(harvest_actual[period][farm])
            else:
                pass
            env.process(preprocessing(env, farms, period, farm))
        yield env.timeout(40)
                     

def preprocessing(env, farms, period, farm):
    x = farm_transport_schedule[period][farm]
    i=1
    if x > 0:
        farms[farm].get(x)
        mylog(env,'Sorghum is being sent to ssl and unloaded for preprocessing and ensilation', log)
        before_ssl[str(farm_ssl[farm])].put(x)
        for equipment in config_rate:
            env.timeout(x/(config_rate[equipment]*equip_in_ssl[str(farm_ssl[farm])][i]))
            i=i+1
            yield env.timeout(.25)
        mylog(env,'sorghum has been preprocessed and ensiled', log)
        before_ssl[str(farm_ssl[farm])].get(x)
        ssl_container[str(farm_ssl[farm])].put(x)
        i=1
       

def moniter_ssl(env, ssl_transport_schedule):
    yield env.timeout(20)
    for period in range(m):
        if 'module_hauler' in configuration:
            loadout_rate = np.random.normal(loadout_rate_module, 1/5*loadout_rate_module)
        else:
            loadout_rate = np.random.normal(loadout_rate_standard, 1/5*loadout_rate_standard)
        loadout_rates.append(loadout_rate)
        for ssl in range(num_ssl):
            env.process(refinery_transport(env, ssl_transport_schedule[period][ssl], ssl, period, loadout_rate))
        yield env.timeout(40)
        mylog(env,'period is over', log)
        
        
def refinery_transport(env, amount, ssl, period, loadout_rate):
    x=int(amount)
#    travel_time = ssl_route[ssl]/np.random.uniform(low=rtruck_speed_low, high=rtruck_speed_high)
    if x > 0 and ssl_container[str(ssl)].level > 0:
#            ssl_container[str(ssl)].get(x)
        y=min(x,ssl_container[str(ssl)].level)
        ssl_container[str(ssl)].get(y)
#            yield env.timeout(travel_time)
        yield env.timeout(x/(equip_in_ssl[str(farm_ssl[farm])][0]*loadout_rate))
        mylog(env,'Sorghum loaded and is being sent to refinery', log)
        refinery.put(y)
    else:
        pass
      
        
def JIT_schedule(env, farms):
    for period in range(m):
        loadout_rate = np.random.normal(loadout_rate_standard, 1/5*loadout_rate_standard)
        loadout_rates_jit.append(loadout_rate)
        for farm in range(n):
            if jit_farm_transport[period][farm] > 0:
                env.process(JIT_delivery(env,period,farm,loadout_rate))
                pass
        yield env.timeout(40)


def JIT_delivery(env, period, farm, loadout_rate):
    y = min(jit_farm_transport[period][farm],farms[farm].level)
    #travel_time_sr = ssl_route[farm_ssl[farm]]/np.random.uniform(low=rtruck_speed_low, high=rtruck_speed_high)
    if y > 0:
        farms[farm].get(y)
        if configuration[0] == 'whole_stalk':
            yield env.timeout(y/config_rate['chopper'])
        yield env.timeout(y/(equip_in_ssl[str(farm_ssl[farm])][0]*loadout_rate))
        #yield env.timeout(travel_time_sr)        
        refinery.put(y)

def mylog(env, string, log):
    print(f'@{env.now}: refinery inventory={refinery.level}| {string}')
    log.write(f'@{env.now}: refinery inventory={refinery.level}| {string} \n')

harvest_hypothetical = []
total_harvest = []
refinery_hypothetical = []
time = []
demand_met = []
refinery_actual = []
hypothetical_ssl = []
actual_ssl = []

def graphs(env, refinery):
    total = 0
    total2 = 0
    total3 = 0
    total4 = 0
    total5 = 0
    for period in range(m):
        for farm in range(n):
            total = total + harvest_actual[period][farm]
            total2 = total2 + a[period][farm] 
            total3 = total3 + jit_farm_transport[period][farm]
        total_harvest.append(total)
        harvest_hypothetical.append(total2)
        
        for ssl in range(num_ssl):
            total3 = total3 + ssl_transport_schedule[period][ssl] 
            total4 = total4 + ssl_inventory[period][ssl]
        for ssl in ssl_container:
            total5 = total5 + ssl_container[ssl].level
        hypothetical_ssl.append(total4)
        actual_ssl.append(total5)
        total4 = 0
        total5 = 0
        refinery_hypothetical.append(total3)
        refinery_actual.append(refinery.level)
        yield env.timeout(40)
        time.append(env.now)
        
    X = np.linspace(0,1080,27)
    plt.plot(X, refinery_hypothetical, color="blue", linewidth=1.0, linestyle="-", label='hypothetical refinery inventory')
    plt.plot(X, refinery_actual, color="red", linewidth=1.0, linestyle="-", label='actual refinery inventory')
    plt.xlim(0,1080)
    plt.ylim(0,230000)
    plt.xticks(np.linspace(0,1080,10,endpoint=True))
    plt.yticks(np.linspace(0,230000,12,endpoint=True))
    plt.legend(loc='upper left', frameon=False)
    plt.show()
    
    
    plt.plot(X, hypothetical_ssl, color="blue", linewidth=1.0, linestyle="-", label='hypothetical total ssl inventory')
    plt.plot(X, actual_ssl, color="red", linewidth=1.0, linestyle="-", label='actual total ssl inventory')
    plt.xlim(0,1080)
    plt.ylim(0,150000)
    plt.xticks(np.linspace(0,1080,10,endpoint=True))
    plt.legend(loc='upper left', frameon=False)
    plt.show()


'''
Simulation Run
'''

env.process(harvest(env, farms))
env.process(moniter_ssl(env,ssl_transport_schedule))
env.process(JIT_schedule(env,farms))
env.process(graphs(env, refinery))
env.run(until=SIM_TIME)