# -*- coding: utf-8 -*-
"""
Created on Fri Sep 21 20:22:27 2018

@author: 999Na
"""

import simpy
import json 
import numpy as np

def create_data():
    with open("sim_example_data.json") as file: 
        data = json.load(file)
        
    num_harvest_trucks = data['harvest_input']['num_trucks_harvest']
    carry_capacity = data['harvest_input']['carry_capacity']
    truck_speed_high = data['harvest_input']['truck_speed_high']
    truck_speed_low = data['harvest_input']['truck_speed_low']
    harvest_time = data['harvest_input']['harvest_time']
    farm_distance = data['harvest_input']['farm_distance']        
    farm_capacitys = data['harvest_input']['farm_capacity']
    harvest_progress = data['harvest_input']['harvest_progress']
    ssl_capacitys = data['ensilation_input']['SSL']
    num_trucks_road = data['road_input']['num_trucks_road']
    truck_capacity = data['road_input']['truck_capacity']
    rtruck_speed_high = data['road_input']['rtruck_speed_high']
    rtruck_speed_low = data['road_input']['rtruck_speed_low']
    ssl_distance = data['road_input']['ssl_distance']
    
    ssl = []
    farms = []
      
    for ssl_capacity in ssl_capacitys:
        ssl.append(simpy.Container(env, ssl_capacity, init=0))
    for farm_capacity in farm_capacitys:
        farms.append(simpy.Container(env, farm_capacity, init=0))
    harvest_trucks = simpy.Resource(env, capacity=num_harvest_trucks)
    road_trucks = simpy.Resource(env, capacity=num_trucks_road)
    refinery = simpy.Container(env, capacity=100000000, init=0)
    
    period_totals = np.zeros(shape=(len(harvest_progress),len(farms)))
    i=0
    j=0
    
    for row in period_totals:
        for col in row:
            period_totals[i][j] = farm_capacitys[j]*(harvest_progress[i]/100)
            j=j+1
        j=0
        i=i+1    
    print(farms)
    print(period_totals)
    harvest(env, farms, period_totals, harvest_trucks, refinery)

            
def harvest(env, farms, period_totals, harvest_trucks, refinery):
    i=0
    j=0
    z=0
    for period in period_totals:
        for farm_num in period:
            farms[j].put(min(np.random.normal(period_totals[i][j]-1/100*period_totals[i][j], 2/100*period_totals[i][j]),period_totals[i][j]))
            print('amount added to farm: ', j)
            print(period_totals[i][j])
            print('Total amount in farm: ', j)            
            print(farms[j].level)
            j=j+1
        j=0
        i=i+1
        transport_harvest(env, farms, harvest_trucks, refinery)
        print(env.now)
        env.timeout(80)

def ensilation():
    pass
   

def transport_harvest(env, farms, harvest_trucks, refinery):
    for farm in farms:
        while farm.level>0:
            with harvest_trucks.request() as req:
                yield req
                farm.get(23)
                #mylog(env, '23 Mg loaded to truck')
                env.timeout(1)
                refinery.put(23)  
    print(refinery.level)
       

#def mylog(env, string):
   #print(f'@{env.now}: {harvest_trucks.count} busy harvest tucks, field inventory={field.level}, ssl inventory={ssl.level}, {trucks.count} busy trucks, refinery inventory={refinery.level}| {string}')'''

env = simpy.Environment()
create_data()
'''mylog(env, 'Begin simulation')
demand = int(input('Enter desired demand for this period: '))
env.run(until=11)
if refinery.level >= demand:
    print('Demand was met for this period')
else:
    print('Demand was not met for this period under current parameters and configuration')'''