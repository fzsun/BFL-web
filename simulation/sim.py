# -*- coding: utf-8 -*-
"""
Created on Fri Sep 21 20:22:27 2018

@author: 999Na
"""

import simpy
import json 
import numpy as np
import re
import math 


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
solutions = output_data['solution'] # holds the algorithms solution dictionary

ssl_container = {} # dictionary relating ssl site location to container with proper capacity
ssl_location = {} # x,y location of ssl
farm_route = [] # distance from farm n to designated ssl
farm_tranport_schedule = {} # dictionary with keys=period and value s= dictionary with amount and time
period1_farm = {}   # dictionary with keys of farm # and corresponding values of amount to be sent in that period
period2_farm = {}
period3_farm = {}
period4_farm = {}
period5_farm = {}
period6_farm = {}
period7_farm = {}
period8_farm = {}
period9_farm = {}
period10_farm = {}
period11_farm = {}
period12_farm = {}
period13_farm = {}
period14_farm = {}
ssl_transport_schedule = {}
period1_ssl = {}
period2_ssl = {}
period3_ssl = {}
period4_ssl = {}
period5_ssl = {}
period6_ssl = {}
period7_ssl = {}
period8_ssl = {}
period9_ssl = {}
period10_ssl = {}
period11_ssl = {}
period12_ssl = {}
period13_ssl = {}
period14_ssl = {}
period15_ssl = {}
period16_ssl = {}
period17_ssl = {}
period18_ssl = {}
period19_ssl = {}
period20_ssl = {}
period21_ssl = {}
period22_ssl = {}
period23_ssl = {}
period24_ssl = {}
period25_ssl = {}
period26_ssl = {}



for solution in solutions:
    aa = solution[0]
    cc = solution[1]
    bb = re.split('\W', aa)
    if bb[0] == 'w':
        ssl_container.update({bb[1]:simpy.Container(env, capacity=K[bb[2]][0], init=0)})
        ssl_location.update({bb[1]:coord_s[bb[1]]})
    if bb[0] == 'y':
        farm_route.append(math.sqrt((ssl_location[bb[2]][0]-coord_f[bb[1]][0])**(2)+(ssl_location[bb[2]][1]-coord_f[bb[1]][1])**(2)))
    if bb[0] == 'zfs':
        if bb[1] == '1':
            period1_farm.update({bb[2]:cc})
        if bb[1] == '2':
            period2_farm.update({bb[2]:cc})
        if bb[1] == '3':
            period3_farm.update({bb[2]:cc})
        if bb[1] == '4':
            period4_farm.update({bb[2]:cc})
        if bb[1] == '5':
            period5_farm.update({bb[2]:cc})
        if bb[1] == '6':
            period6_farm.update({bb[2]:cc})
        if bb[1] == '7':
            period7_farm.update({bb[2]:cc})
        if bb[1] == '8':
            period8_farm.update({bb[2]:cc})
        if bb[1] == '9':
            period9_farm.update({bb[2]:cc})
        if bb[1] == '10':
            period10_farm.update({bb[2]:cc})
        if bb[1] == '11':
            period11_farm.update({bb[2]:cc})
        if bb[1] == '12':
            period12_farm.update({bb[2]:cc})
        if bb[1] == '13':
            period13_farm.update({bb[2]:cc})
        if bb[1] == '14':
            period14_farm.update({bb[2]:cc})
    farm_tranport_schedule.update({1:period1_farm,2:period2_farm,3:period3_farm,4:period4_farm,5:period5_farm,
                                   6:period6_farm,7:period7_farm,8:period8_farm,9:period9_farm,10:period10_farm,
                                   11:period11_farm,12:period12_farm,13:period13_farm,14:period14_farm})
    if bb[0] == 'zs':
        if bb[1] == '1':
            period1_ssl.update({bb[2]:cc})
        if bb[1] == '2':
            period2_ssl.update({bb[2]:cc})
        if bb[1] == '3':
            period3_ssl.update({bb[2]:cc})
        if bb[1] == '4':
            period4_ssl.update({bb[2]:cc})
        if bb[1] == '5':
            period5_ssl.update({bb[2]:cc})
        if bb[1] == '6':
            period6_ssl.update({bb[2]:cc})
        if bb[1] == '7':
            period7_ssl.update({bb[2]:cc})
        if bb[1] == '8':
            period8_ssl.update({bb[2]:cc})
        if bb[1] == '9':
            period9_ssl.update({bb[2]:cc})
        if bb[1] == '10':
            period10_ssl.update({bb[2]:cc})
        if bb[1] == '11':
            period11_ssl.update({bb[2]:cc})
        if bb[1] == '12':
            period12_ssl.update({bb[2]:cc})
        if bb[1] == '13':
            period13_ssl.update({bb[2]:cc})
        if bb[1] == '14':
            period14_ssl.update({bb[2]:cc})
        if bb[1] == '15':
            period15_ssl.update({bb[2]:cc})
        if bb[1] == '16':
            period16_ssl.update({bb[2]:cc})
        if bb[1] == '17':
            period17_ssl.update({bb[2]:cc})
        if bb[1] == '18':
            period18_ssl.update({bb[2]:cc})
        if bb[1] == '19':
            period19_ssl.update({bb[2]:cc})
        if bb[1] == '20':
            period20_ssl.update({bb[2]:cc})
        if bb[1] == '21':
            period21_ssl.update({bb[2]:cc})
        if bb[1] == '22':
            period22_ssl.update({bb[2]:cc})
        if bb[1] == '23':
            period23_ssl.update({bb[2]:cc})
        if bb[1] == '24':
            period24_ssl.update({bb[2]:cc})
        if bb[1] == '25':
            period25_ssl.update({bb[2]:cc})
        if bb[1] == '26':
            period26_ssl.update({bb[2]:cc})
    ssl_transport_schedule.update({1:period1_ssl, 2:period2_ssl,3:period3_ssl,4:period4_ssl,5:period5_ssl,6:period6_ssl,
                                   7:period7_ssl,8:period8_ssl,9:period9_ssl,10:period10_ssl,11:period11_ssl,12:period12_ssl,
                                   13:period13_ssl,14:period14_ssl,15:period15_ssl,16:period16_ssl,17:period17_ssl,
                                   18:period18_ssl,19:period19_ssl,20:period20_ssl,21:period21_ssl,22:period22_ssl,
                                   23:period23_ssl,24:period24_ssl,25:period25_ssl,26:period26_ssl})
            
farms = []
m = a.shape[0]
n = a.shape[1]

print(n, " ",m)

# create functions      
def harvest(env, farms, a, m, n, harvest_trucks, refinery, carry_capacity):
    '''
Harvest function utilizes the matrix a from the algorithm output file, which is the harvest schedule.
The function iterates through the harvest schedule and adds sorghum to the farms container utilizing a normal distribution.
After a farm recieves the sorghum, the transport_harvest() process is called.
After each period, we yield a timeout of 40 to represent a 40 hour work week.
    '''
    for row in range(m):
        for col in range(n):
            if a[row][col] != 0:
                farms[col].put(np.random.normal(a[row][col], 1/100*a[row][col]))
                print('Total amount in farm: ', col, ' ', farms[col].level)
                env.process(transport_harvest(env, farm_tranport_schedule[1], harvest_trucks, refinery, carry_capacity))
            else:
                pass
        yield env.timeout(40)
        print('Current time', env.now)

def ensilation():
    pass
   
def transport_harvest(env, farm, harvest_trucks, refinery, carry_capacity):
    '''
This process is called by the harvest process to request harvest_trucks resource to move sorghum from farms to ssl's.
It uses a while loop to achieve the goal of calling trucks until the farm has sent all of its sorghum out.
At the moment it has a timeout with no real logic behind it as a place holder until a more accurate number can be derived.
    '''
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

