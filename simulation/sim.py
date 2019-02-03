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

# Define containers and resources and start process



'''
Data Creation Section
'''

class Simulation(object):
        
    # For testing simulation against algorithm
    '''# open input and output files to be used
    with open("example_output1_jit.json") as output_file:
        output_data = json.load(output_file)
    with open("example_input.json") as algo_input:
        algo_input_data = json.load(algo_input)    
    log = open('log.txt','w+')'''

    def trial_constant_input(self, output_data, algo_input_data):
        num_trials = int(input('How many sample trials would you like to simulate? '))
        # assign variables from algo input
        self.horizon = algo_input_data['horizon']
        self.demand = algo_input_data['demand']
        self.equipment_data = algo_input_data['cost']['equipment']
        self.degradation = algo_input_data['degrade']

        self.SIM_TIME = 1081

        # assign variables from output file
        self.coord_f = output_data['params']['Coord_f'] # coordinates x,y for self.farms (all possible)
        self.coord_s = output_data['params']['self.Coord_s'] # coordinates x,y for ssl (all possible)
        self.K = output_data['params']['K'] # ssl size and equipment loadout configurations
        self.a = np.array(output_data['params']['a']) # 26 harvest schedule (yield for each farm in each period Mg)
        self.d = output_data['params']['d'] # self.demand
        self.u = output_data['params']['u'] # capacities for ssl
        self.ue = output_data['params']['ue'] # processing rate of non-chopping methods
        self.sysnum = output_data['params']['Sysnum']
        self.solutions = output_data['solution'] # holds the algorithms solution dictionary
        self.configuration = output_data['params']['Configuration']
        self.num_ssl = len(self.coord_s)


        self.config_rate = {}
        self.loadout_rates = []
        self.loadout_rates_jit = []
        for equipment in self.configuration:
            if equipment == 'loadout':
                self.loadout_rate_standard = self.equipment_data[equipment][4]/40
            if equipment == 'press':
                self.config_rate.update({'press':self.equipment_data[equipment][4]/40})
                self.press_rate = []
            if equipment == 'chopper':
                self.config_rate.update({'chopper':self.equipment_data[equipment][4]/40})
                self.chopper_rate = []
            if equipment == 'bagger':
                self.config_rate.update({'bagger':self.equipment_data[equipment][4]/40})
                self.bagger_rate = []
            if equipment == 'module_former':
                self.config_rate.update({'module_former':self.equipment_data[equipment][4]/40})
                self.former_rate = []
            if equipment == 'module_hauler':
                self.loadout_rate_module = self.equipment_data[equipment][4]/40
            

        self.m = a.shape[0]
        self.n = a.shape[1]

        self.all_self.refinery_actual = []
        self.all_ssl_actual = []
        self.all_degradation_ensiled_actual = []
        self.all_degradation_farm_actual = []
        self.all_demand = []
        self.harvest_hypothetical = []
        self.refinery_hypothetical = []
        self.hypothetical_ssl = []
        self.refinery_average = []
        self.ssl_average = []
        self.degradation_farm_average = []
        self.degradation_ssl_average = []


    '''

    Start Trials

    '''


    def initialize_simulation(env, self):    
        env = simpy.Environment()
    
        self.farms = []
        
        self.farm_transport_schedule = [] 
        self.harvest_actual = []
        self.jit_farm_transport = [] 
        self.farm_level_actual = []
        self.farm_inventory = []

        self.ssl_route = [] # distance from ssl to orgin (refinery)

        self.equip_in_ssl = {} # dictionary for ssl configuration
        self.before_ssl = {}
        self.ssl_container = {} # dictionary relating ssl site location to container with proper capacity
        self.ssl_location = {} # x,y location of ssl

        self.ssl_level_actual = []
        self.ssl_transport_schedule = [] 
        self.ssl_inventory = [] 

        self.farm_route = [] # distance from farm n to designated ssl
        self.farm_ssl = {} # shows which farm corresponds to using which ssl 

        self.total_harvest = []
        self.refinery_actual = []
        self.actual_ssl = []
        self.degradation_ensiled_actual = []
        self.degradation_farm_actual = []

        for farm in range(n):
            self.farms.append(simpy.Container(env, 10000000, init=0))
        
        for period in range(self.m):
            self.farm_transport_schedule.append([])
            self.harvest_actual.append([])
            self.jit_farm_transport.append([])
            self.farm_level_actual.append([])
            self.farm_inventory.append([])
            for farm in range(n):
                self.harvest_actual[period].append(0)
                self.farm_transport_schedule[period].append(0)
                self.jit_farm_transport[period].append(0)
                self.farm_level_actual[period].append(0)
                self.farm_inventory[period].append(0)
        
        for coord in self.coord_s:
            self.ssl_route.append(math.sqrt(self.coord_s[coord][1]**(2)+self.coord_s[coord][0]**(2)))

        for solution in self.solutions:
            aa = solution[0]
            cc = solution[1]
            bb = re.split('\W', aa)
            if bb[0] == 'w':
                self.equip_in_ssl[bb[1]] = K[bb[2]][1:]
                self.before_ssl[bb[1]] = simpy.Container(env,capacity=K[bb[2]][0], init=0)
                self.ssl_container[bb[1]] = simpy.Container(env,capacity=K[bb[2]][0], init=0)
                self.ssl_location[bb[1]] = self.coord_s[bb[1]]
        
        for period in range(self.m):
            self.ssl_transport_schedule.append([])
            self.ssl_inventory.append([])
            self.ssl_level_actual.append([])
            for ssl in range(self.num_ssl):
                self.ssl_transport_schedule[period].append(0)
                self.ssl_inventory[period].append(0)
                self.ssl_level_actual[period].append(0)
             
        for solution in self.sol:
            aa = solution[0]
            cc = solution[1]
            bb = re.split('\W', aa)
            if bb[0] == 'y':
                self.farm_route.append(math.sqrt((self.ssl_location[bb[2]][0]-self.coord_f[bb[1]][0])**(2)+(self.ssl_location[bb[2]][1]-self.coord_f[bb[1]][1])**(2)))
                self.farm_ssl.update({int(bb[1]):int(bb[2])})
            if bb[0] == 'zfs':  # populate the farm transport schedule from algorithm solution
                self.farm_transport_schedule[int(bb[1])][int(bb[2])] = cc
            if bb[0] == 'zs':   # populate the ssl transportation schedule from algorithm solution
                self.ssl_transport_schedule[int(bb[1])][int(bb[2])] = cc
            if bb[0] == 'z_jit':
                self.jit_farm_transport[int(bb[1])][int(bb[2])] = cc
            if bb[0] == 'Is':
                self.ssl_inventory[int(bb[1])][int(bb[2])] = cc
            if bb[0] == 'If':
                self.farm_inventory[int(bb[1])][int(bb[2])] = cc

        self.degradation_farm_expected = []
        self.degradation_ensiled_expected = [] 
        
        '''
        Functions Section
        '''
        
        # create functions      
        def harvest(env, self):
            self.harvest_total_period = 0
            self.harvest_total = 0
            for period in range(self.m):
                if 'module_hauler' in self.configuration:
                    self.loadout_rate = np.random.normal(self.loadout_rate_module, 1/5*self.loadout_rate_module)
                else:
                    self.loadout_rate = np.random.normal(self.loadout_rate_standard, 1/5*self.loadout_rate_standard)
                self.loadout_rates.append(loadout_rate)
                for farm in range(n):
                    if a[period][farm] != 0:
                        self.harvest_actual[period][farm]=max(0, np.random.normal(a[period][farm], 1/5*a[period][farm]))
                        self.farms[farm].put(self.harvest_actual[period][farm])
                        self.harvest_total_period = self.harvest_total_period + self.harvest_actual[period][farm]
                    else:
                        pass
                    if self.jit_farm_transport[period][farm] != 0:
                        env.process(JIT_delivery(env,period,farm,loadout_rate))
                    env.process(preprocessing(env, self, period, farm))
                self.harvest_total = self.harvest_total + self.harvest_total_period    
                yield env.timeout(40)           
        
        
        def preprocessing(env, self, period, farm):
            self.expected_preprocess_amount = self.farm_transport_schedule[period][farm]
            self.actual_preprocess_amount = min(self.expected_preprocess_amount,self.farms[farm].level)
            i=1
            if self.actual_preprocess_amount > 0:
                self.farms[farm].get(x)
                #mylog(env,'Sorghum is being sent to ssl and unloaded for preprocessing and ensilation', log)
                self.before_ssl[str(self.farm_ssl[farm])].put(x)
                for equipment in self.config_rate:
                    rate = np.random.normal(self.config_rate[equipment],1/5*self.config_rate[equipment])
                    if equipment == 'press':
                        self.press_rate.append(rate)
                    if equipment == 'chopper':
                        self.chopper_rate.append(rate)
                    if equipment == 'bagger':
                        self.bagger_rate.append(rate)
                    if equipment == 'module_former':
                        self.former_rate.append(rate)
                    env.timeout(self.actual_preprocess_amount/(rate*self.equip_in_ssl[str(self.farm_ssl[farm])][i]))
                    i=i+1
                    yield env.timeout(.25)
                #mylog(env,'sorghum has been preprocessed and ensiled', log)
                self.before_ssl[str(self.farm_ssl[farm])].get(self.actual_preprocess_amount)
                self.ssl_container[str(self.farm_ssl[farm])].put(self.actual_preprocess_amount)
                self.ssl_level_actual[period][self.farm_ssl[farm]] = self.ssl_container[str(self.farm_ssl[farm])].level
                i=1
            
        
        def moniter_ssl(env, self):
            yield env.timeout(1)
            for period in range(self.m):
                if 'module_hauler' in self.configuration:
                    self.loadout_rate = np.random.normal(self.loadout_rate_module, 1/5*self.loadout_rate_module)
                else:
                    self.loadout_rate = np.random.normal(self.loadout_rate_standard, 1/5*self.loadout_rate_standard)
                self.loadout_rates.append(loadout_rate)
                for ssl in range(self.num_ssl):
                    env.process(refinery_transport(env, self, ssl, period))
                yield env.timeout(40)
                #mylog(env,'period is over', log)
                
                
        def refinery_transport(env, self, ssl, period):
            x=int(self.ssl_transport_schedule[period][ssl])
        #    travel_time = self.ssl_route[ssl]/np.random.uniform(low=rtruck_speed_low, high=rtruck_speed_high)
            if x > 0 and self.ssl_container[str(ssl)].level > 0:
        #        self.ssl_container[str(ssl)].get(x)
                y=min(x,self.ssl_container[str(ssl)].level)
                self.ssl_container[str(ssl)].get(y)
        #        yield env.timeout(travel_time)
                yield env.timeout(x/(self.equip_in_ssl[str(self.farm_ssl[farm])][0]*loadout_rate))
                #mylog(env,'Sorghum loaded and is being sent to refinery', log)
                refinery.put(y)
            else:
                pass
            
        
        
        def JIT_delivery(env, self, period, farm):
            self.deliver_to_refinery = min(self.jit_farm_transport[period][farm],self.farms[farm].level)
            #travel_time_sr = self.ssl_route[self.farm_ssl[farm]]/np.random.uniform(low=rtruck_speed_low, high=rtruck_speed_high)
            if self.deliver_to_refinery > 0:
                self.farms[farm].get(self.deliver_to_refinery)
                if self.configuration[0] == 'whole_stalk':
                    yield env.timeout(self.deliver_to_refinery/self.config_rate['chopper'])
                yield env.timeout(self.deliver_to_refinery/(self.equip_in_ssl[str(self.farm_ssl[farm])][0]*loadout_rate))
                #yield env.timeout(travel_time_sr)        
                refinery.put(self.deliver_to_refinery)
        
        
        
        def degradation_field(env, self): 
            x = 0
            y = 0
            for period in range(self.m):
                yield env.timeout(20)
                for farm in range(n):
                    if self.farms[farm].level > 0:
                        if self.sysnum in [0,1,2,3,4,5,6,7]:
                            self.degradation_amount = self.farms[farm].level/9
                            degraded_field.put(self.degradation_amount)
                        if self.sysnum in [8,9,10,11,12,13,14,15]:
                            self.degradation_amount = self.farms[farm].level/5
                            degraded_field.put(self.degradation_amount)
                    else:
                        pass
                    if self.farm_inventory[period][farm] > 0:
                        if self.sysnum in [0,1,2,3,4,5,6,7]:
                            self.degradation_amount = self.farm_inventory[period][farm]/9
                            x=x+self.degradation_amount
                        if self.sysnum in [8,9,10,11,12,13,14,15]:
                            self.degradation_amount = self.farm_inventory[period][farm]/5
                            x=x+self.degradation_amount
                    else:
                        pass
                y=y+x
                x=0
                degradation_field_to.append(y)
                yield env.timeout(20)
                                
        def degradation_ensiled(env, self):
            x=0
            y=0
            for period in range(self.m):
                yield env.timeout(39)
                for ssl in self.ssl_container:
                    if self.ssl_container[ssl].level > 0:
                        if self.sysnum in [0,4,8,12]:
                            self.degradation_amount = self.ssl_container[ssl].level/5
                            degraded_ensiled.put(self.degradation_amount)
                        if self.sysnum in [1,5,9,13]:
                            self.degradation_amount = self.ssl_container[ssl].level/100
                            degraded_ensiled.put(self.degradation_amount)
                        if self.sysnum in [2,6,10,14]:
                            self.degradation_amount = self.ssl_container[ssl].level/8
                            degraded_ensiled.put(self.degradation_amount)
                        if self.sysnum in [3,7,11,15]:
                            pass
                    else:
                        pass
                    if self.ssl_inventory[period][int(ssl)] > 0:
                        if self.sysnum in [0,4,8,12]:
                            self.degradation_amount = self.ssl_inventory[period][int(ssl)]/5
                            x=x+self.degradation_amount
                        if self.sysnum in [1,5,9,13]:
                            self.degradation_amount = self.ssl_inventory[period][int(ssl)]/100
                            x=x+self.degradation_amount
                        if self.sysnum in [2,6,10,14]:
                            self.degradation_amount = self.ssl_inventory[period][int(ssl)]/80
                            x=x+self.degradation_amount
                y=y+x
                x=0
                self.degradation_ensiled_expected.append(y)
                yield env.timeout(1)
        
        
    
        def record_data(env, self):
            total = 0
            total5 = 0
            for period in range(self.m):
                for farm in range(n):   
                    total = total + self.harvest_actual[period][farm]
                self.total_harvest.append(total)
                for ssl in self.ssl_container:
                    total5 = total5 + self.ssl_container[ssl].level
                self.actual_ssl.append(total5)
                self.degradation_ensiled_actual.append(degraded_ensiled.level)
                self.degradation_farm_actual.append(degraded_field.level)
                self.refinery_actual.append(refinery.level)
                yield env.timeout(40)
                total5 = 0
            self.all_self.refinery_actual.append(self.refinery_actual)
            self.all_ssl_actual.append(self.actual_ssl)
            self.all_degradation_ensiled_actual.append(self.degradation_ensiled_actual)
            self.all_degradation_farm_actual.append(self.degradation_farm_actual)
                                            
                                            
        '''def mylog(env, string, log):
            print(f'@{env.now}: refinery inventory={refinery.level}| {string}')
            log.write(f'@{env.now}: refinery inventory={refinery.level}| {string} \n')'''            
            
    def graphs():
        total2 = 0
        total3 = 0
        total4 = 0
        for period in range(self.m):
            for farm in range(n):
                total2 = total2 + self.a[period][farm] 
                total3 = total3 + self.jit_farm_transport[period][farm]
            self.harvest_hypothetical.append(total2)
            for ssl in range(self.num_ssl):
                total3 = total3 + self.ssl_transport_schedule[period][ssl] 
                total4 = total4 + self.ssl_inventory[period][ssl]
            self.hypothetical_ssl.append(total4)
            self.refinery_hypothetical.append(total3)
            total4 = 0
        for period in range(self.m):
            total6 = 0
            total7 = 0
            total8 = 0
            total9 = 0
            for trial in range(num_trials):
                total6 = total[trial][period]
                total7 = total[trial][period]
                total8 = total8 + self.all_ssl_actual[trial][period]
                total9 = total9 + self.all_self.refinery_actual[trial][period]
            self.degradation_ssl_average.append(total6/num_trials)
            self.degradation_farm_average.append(total7/num_trials)
            self.ssl_average.append(total8/num_trials)
            self.refinery_average.append(total9/num_trials)
            
            
            
            
        X = np.linspace(0,1080,27)
        
        print('\nRefinery Inventory level v.s. Time')
        plt.plot(X, self.refinery_hypothetical, color="blue", linewidth=1.0, linestyle="-", label='scheduled refinery inventory')
        plt.plot(X, self.refinery_average, color="red", linewidth=1.0, linestyle="-", label='actual refinery inventory')
        plt.xlim(0,1080)
        plt.ylim(0,230000)
        plt.xticks(np.linspace(0,1080,10,endpoint=True))
        plt.yticks(np.linspace(0,230000,12,endpoint=True))
        plt.legend(loc='upper left', frameon=False)
        plt.show()
        
        print('\nSum of Ensiled Sorghum v.s. Time')
        plt.plot(X, self.hypothetical_ssl, color="blue", linewidth=1.0, linestyle="-", label='scheduled total ssl inventory')
        plt.plot(X, ssl_average, color="red", linewidth=1.0, linestyle="-", label='actual total ssl inventory')
        plt.xlim(0,1080)
        plt.ylim(0,150000)
        plt.xticks(np.linspace(0,1080,10,endpoint=True))
        plt.legend(loc='upper left', frameon=False)
        plt.show()
        
        print('\nself.Degradation of Ensiled Sorghum v.s. Time')
        plt.plot(X,self.degradation_ssl_average,label='Degraded sorghum in MG')
        plt.plot(X,self.degradation_ensiled_expected,label='Expected degraded sorghum in MG')
        plt.xlim(0,1080)
        plt.ylim(0,100000)
        plt.xticks(np.linspace(0,1080,10,endpoint=True))
        plt.legend(loc='upper left',frameon=False)
        plt.show()
        
        print('\nself.Degradation of Harvested Field Sorghum v.s. Time')
        plt.plot(X,self.degradation_farm_average,label='Degraded sorghum in MG')
        plt.plot(X,,label='Expected degraded sorghum in MG')
        plt.xlim(0,1080)
        plt.ylim(0,100000)
        plt.xticks(np.linspace(0,1080,10,endpoint=True))
        plt.legend(loc='upper left',frameon=False)
        plt.show()
        
    
    def main(self, output_data, algo_input_data):  

        self.output_data = output_data
        self.algo_input_data = algo_input_data  

        trial_constant_input(self)
        self.num_trials = int(input('How many simulation trials would you like to run?: '))
        for tial in range(self.num_trials):
            initialize_simulation(env, self)
            env.process(harvest((env, self))
            env.process(moniter_ssl(env, self))
            env.process(degradation_field(env, self))
            env.process(degradation_ensiled(env, self))
            env.process(record_data(env, self))

        for equipment in self.config_rate:
            if equipment == 'press':
                print('The average compression rate in MG/hour:',np.mean(self.press_rate))
            if equipment == 'chopper':
                print('The average chopper rate in MG/hour:',np.mean(self.chopper_rate))
            if equipment == 'bagger':
                print('The average bagger rate in MG/hour:',np.mean(self.bagger_rate))
            if equipment == 'module_former':
                print('The average module former rate in MG/hour:',np.mean(self.former_rate))

            if equipment == 'module_hauler':
                print('The average loadout rate for module hauler in MG/hour:',np.mean(self.loadout_rates)) 
        if 'module_hauler' in self.configuration:
            print('Average module hauler loadout rate in MG/hour:',np.mean(self.loadout_rates))
        else:
            print('Average loadout rate in MG/hour:',np.mean(self.loadout_rates))

        if np.m) >= self.demand:
            print('The whole self.demand of ',self.demand,'MG was met over the current planning hrorizon for',num_trials,'samples')
        else:
            percent_met = np.m)/self.demand*100
            print(percent_met,'% of the ',self.demand,'MG self.demand was met over the current planning self.horizon for',num_trials,'samples')

    '''self.degradation_cost = 0
    for period in range(self.m):
        self.degradation_cost = self.degradation_cost + ((self.degradation_ssl_average[period]-self.degradation_ensiled_expected[period])*65+(self.degradation_farm_average[period]-[period])*65)
    print('The extra cost incured due to unforseen self.degradation is: ',self.degradation_cost,' dollars')'''
        
        