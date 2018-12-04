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
with open("example_output2.json") as output_file:
    output_data = json.load(output_file)
with open("example_input.json") as algo_input:
    algo_input_data = json.load(algo_input)
    
log = open('log.txt','w+')
    
# assign variables from algo input
horizon = algo_input_data['horizon']
demand = algo_input_data['demand']
equipment_data = algo_input_data['cost']['equipment']
degradation = algo_input_data['degrade']

SIM_TIME = 1081

# assign variables from output file
coord_f = output_data['params']['Coord_f'] # coordinates x,y for farms (all possible)
coord_s = output_data['params']['Coord_s'] # coordinates x,y for ssl (all possible)
K = output_data['params']['K'] # ssl size and equipment loadout configurations
a = np.array(output_data['params']['a']) # 26 harvest schedule (yield for each farm in each period Mg)
d = output_data['params']['d'] # demand
u = output_data['params']['u'] # capacities for ssl
ue = output_data['params']['ue'] # processing rate of non-chopping methods
sysnum = output_data['params']['Sysnum']
solutions = output_data['solution'] # holds the algorithms solution dictionary
configuration = output_data['params']['Configuration']
num_ssl = len(coord_s)


config_rate = {}
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
    

m = a.shape[0]
n = a.shape[1]

farms = []
# create farms
for farm in range(n):
    farms.append(simpy.Container(env, 10000000, init=0))
refinery = simpy.Container(env, capacity=100000000, init=0)
degraded_ensiled = simpy.Container(env, capacity=100000000, init=0)
degraded_field = simpy.Container(env, capacity=100000000, init=0)

farm_transport_schedule = [] 
harvest_actual = []
jit_farm_transport = [] 
farm_level_actual = []

for period in range(m):
    farm_transport_schedule.append([])
    harvest_actual.append([])
    jit_farm_transport.append([])
    farm_level_actual.append([])
    for farm in range(n):
        harvest_actual[period].append(0)
        farm_transport_schedule[period].append(0)
        jit_farm_transport[period].append(0)
        farm_level_actual[period].append(0)



ssl_route = [] # distance from ssl to orgin (refinery)
for coord in coord_s:
    ssl_route.append(math.sqrt(coord_s[coord][1]**(2)+coord_s[coord][0]**(2)))
    

equip_in_ssl = {} # dictionary for ssl configuration
before_ssl = {}
ssl_container = {} # dictionary relating ssl site location to container with proper capacity
ssl_location = {} # x,y location of ssl
for solution in solutions:
    aa = solution[0]
    cc = solution[1]
    bb = re.split('\W', aa)
    if bb[0] == 'w':
        equip_in_ssl[bb[1]] = K[bb[2]][1:]
        before_ssl[bb[1]] = simpy.Container(env,capacity=K[bb[2]][0], init=0)
        ssl_container[bb[1]] = simpy.Container(env,capacity=K[bb[2]][0], init=0)
        ssl_location[bb[1]] = coord_s[bb[1]]


ssl_level_actual = []
ssl_transport_schedule = [] 
ssl_inventory = []        
for period in range(m):
    ssl_transport_schedule.append([])
    ssl_inventory.append([])
    ssl_level_actual.append([])
    for ssl in range(num_ssl):
        ssl_transport_schedule[period].append(0)
        ssl_inventory[period].append(0)
        ssl_level_actual[period].append(0)
  

farm_route = [] # distance from farm n to designated ssl
farm_ssl = {} # shows which farm corresponds to using which ssl      
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
def harvest(env):
    x = 0
    y = 0
    for period in range(m):
        for farm in range(n):
            if a[period][farm] != 0:
                harvest_actual[period][farm]=max(0,np.random.normal(a[period][farm], 1/5*a[period][farm]))
                farms[farm].put(harvest_actual[period][farm])
                x=x+harvest_actual[period][farm]
            else:
                pass
            env.process(preprocessing(env, period, farm))
            y=y+x
            x=0
        yield env.timeout(40)
    print('total harvested = ',y)

def preprocessing(env, period, farm):
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
        ssl_level_actual[period][farm_ssl[farm]] = ssl_container[str(farm_ssl[farm])].level
        i=1
       

def moniter_ssl(env):
    yield env.timeout(10)
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
#        ssl_container[str(ssl)].get(x)
        y=min(x,ssl_container[str(ssl)].level)
        ssl_container[str(ssl)].get(y)
#        yield env.timeout(travel_time)
        yield env.timeout(x/(equip_in_ssl[str(farm_ssl[farm])][0]*loadout_rate))
        mylog(env,'Sorghum loaded and is being sent to refinery', log)
        refinery.put(y)
    else:
        pass
      
        
def JIT_schedule(env):
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


def degradation_field(env):  
    for period in range(m):
        yield env.timeout(39)
        for farm in range(n):
            if farms[farm].level > 0:
                if sysnum in [0,1,2,3,4,5,6,7]:
                    degradation_amount = farms[farm].level/9
                    farms[farm].get(degradation_amount)
                    degraded_field.put(degradation_amount)
                if sysnum in [8,9,10,11,12,13,14,15]:
                    degradation_amount = farms[farm].level/5
                    farms[farm].get(degradation_amount)
                    degraded_field.put(degradation_amount)
            else:
                pass
        yield env.timeout(1)
                    
        
def degradation_ensiled(env):
    for period in range(m):
        yield env.timeout(39)
        for ssl in ssl_container:
            if ssl_container[ssl].level > 0:
                if sysnum in [0,4,8,12]:
                    degradation_amount = ssl_container[ssl].level/5
                    ssl_container[ssl].get(degradation_amount)
                    degraded_ensiled.put(degradation_amount)
                if sysnum in [1,5,9,13]:
                    degradation_amount = ssl_container[ssl].level/100
                    ssl_container[ssl].get(degradation_amount)
                    degraded_ensiled.put(degradation_amount)
                if sysnum in [2,6,10,14]:
                    degradation_amount = ssl_container[ssl].level/80
                    ssl_container[ssl].get(degradation_amount)
                    degraded_ensiled.put(degradation_amount)
                if sysnum in [3,7,11,15]:
                    pass
            else:
                pass
        yield env.timeout(1)


harvest_hypothetical = []
total_harvest = []
refinery_hypothetical = []
time = []
demand_met = []
refinery_actual = []
hypothetical_ssl = []
actual_ssl = []
degradation_ensiled_actual = []
degradation_farm_actual = []
def graphs(env):
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
            
        degradation_ensiled_actual.append(degraded_ensiled.level)
        degradation_farm_actual.append(degraded_field.level)
        hypothetical_ssl.append(total4)
        actual_ssl.append(total5)
        total4 = 0
        total5 = 0
        refinery_hypothetical.append(total3)
        refinery_actual.append(refinery.level)
        yield env.timeout(40)
        time.append(env.now)
    env.timeout(1)    
    X = np.linspace(0,1080,27)
    
    print('\nRefinery Inventory level v.s. Time')
    plt.plot(X, refinery_hypothetical, color="blue", linewidth=1.0, linestyle="-", label='scheduled refinery inventory')
    plt.plot(X, refinery_actual, color="red", linewidth=1.0, linestyle="-", label='actual refinery inventory')
    plt.xlim(0,1080)
    plt.ylim(0,230000)
    plt.xticks(np.linspace(0,1080,10,endpoint=True))
    plt.yticks(np.linspace(0,230000,12,endpoint=True))
    plt.legend(loc='upper left', frameon=False)
    plt.show()
    
    print('\nSum of Ensiled Sorghum v.s. Time')
    plt.plot(X, hypothetical_ssl, color="blue", linewidth=1.0, linestyle="-", label='scheduled total ssl inventory')
    plt.plot(X, actual_ssl, color="red", linewidth=1.0, linestyle="-", label='actual total ssl inventory')
    plt.xlim(0,1080)
    plt.ylim(0,150000)
    plt.xticks(np.linspace(0,1080,10,endpoint=True))
    plt.legend(loc='upper left', frameon=False)
    plt.show()
    
    print('\nDegradation of Ensiled Sorghum v.s. Time')
    plt.plot(X,degradation_ensiled_actual,label='Degraded sorghum in MG')
    plt.xlim(0,1080)
    plt.ylim(0,100000)
    plt.xticks(np.linspace(0,1080,10,endpoint=True))
    plt.legend(loc='upper left',frameon=False)
    plt.show()
    
    print('\nDegradation of Harvested Field Sorghum v.s. Time')
    plt.plot(X,degradation_farm_actual,label='Degraded sorghum in MG')
    plt.xlim(0,1080)
    plt.ylim(0,100000)
    plt.xticks(np.linspace(0,1080,10,endpoint=True))
    plt.legend(loc='upper left',frameon=False)
    plt.show()

    
def mylog(env, string, log):
    print(f'@{env.now}: refinery inventory={refinery.level}| {string}')
    log.write(f'@{env.now}: refinery inventory={refinery.level}| {string} \n') 
        

'''
Simulation Run
'''

env.process(harvest(env))
env.process(moniter_ssl(env))
env.process(JIT_schedule(env))
env.process(degradation_ensiled(env))
env.process(degradation_field(env))
env.process(graphs(env))
env.run(until=SIM_TIME)

if refinery.level >= demand:
    print('The whole demand of ',demand,'MG was met over the current planning hrorizon')
else:
    percent_met = refinery.level/demand*100
    print(percent_met,'% of the ',demand,'MG demand was met over the current planning horizon')
