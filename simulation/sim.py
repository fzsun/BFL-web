'''
Perfect transport from ssl => should yield a max of 199991.99 Mg
Total transport from farm to ssl can yield a max of 202672.0000000001 Mg
'''

from scipy import stats as stat
import simpy
import json 
import numpy as np
import re
import math 
import matplotlib.pyplot as plt


#open input and output files to be used
#with open('output_0.json') as output_file:
 #   output_data = json.load(output_file)
#with open('example_input.json') as algo_input:
 #   algo_input_data = json.load(algo_input)

class Simulation(object):
    
    '''
    -init defines all of the data that will saty constant throughout the simulation trials
    -this is a combination of data from the algorithms input and output
    '''
    
    def __init__(self):
        print(" * Created new simulation")
        
    def new_input(self, algo_input_data, output_data):
        self.algo_input_data = algo_input_data
        self.output_data = output_data
                   
        self.num_trials = 10
        self.work_week = 40
         # assign variables from algo input
        self.demand = self.algo_input_data['demand']
        self.equipment_data = self.algo_input_data['cost']['equipment']
        self.degradation = self.algo_input_data['degrade']
        
        self.SIM_TIME = self.algo_input_data['horizon']*self.work_week + self.work_week*2
        
        # assign variables from output file
        self.coord_f = self.output_data['params']['Coord_farms'] # coordinates x,y for farms (all possible)
        self.coord_s = self.output_data['params']['Coord_ssls'] # coordinates x,y for ssl (all possible)
        self.ssl_configurations = self.output_data['params']['SSL_configuration'] # ssl size and equipment loadout configurations
        self.harvest_schedule = np.array(self.output_data['params']['harvested']) # 26 harvest schedule (yield for each farm in each period Mg)
        self.ue = self.output_data['params']['upperbound_equip_proc_rate'] # processing rate of non-chopping methods
        self.sysnum = self.output_data['params']['Sysnum']
        self.solutions = self.output_data['solution'] # holds the algorithms solution dictionary
        self.configuration = self.output_data['params']['Configuration']
        self.num_ssl = len(self.coord_s)
        self.config_rate = {}
        self.loadout_rates_standard = []
        self.loadout_rates_module = []
        self.loadout_rates_standard_jit = []
        self.loadout_rates_module_jit = []
        self.loadout_rate_module_new = 0
        self.loadout_rate_standard_new = 0
        print(algo_input_data["new_input"])
        if algo_input_data["new_input"]:
            print("new!!!!!")
            for equipment in self.configuration:
                if equipment == 'loadout':
                    self.loadout_rate_standard = self.equipment_data[equipment][4]/self.work_week
                    self.loadout_rate_standard_new = self.loadout_rate_standard
                elif equipment == 'press':
                    self.config_rate.update({'press':self.equipment_data[equipment][4]/self.work_week})
                    self.press_rate = []
                elif equipment == 'chopper':
                    self.config_rate.update({'chopper':self.equipment_data[equipment][4]/self.work_week})
                    self.chopper_rate = []
                elif equipment == 'bagger':
                    self.config_rate.update({'bagger':self.equipment_data[equipment][4]/self.work_week})
                    self.bagger_rate = []
                elif equipment == 'module_former':
                    self.config_rate.update({'module_former':self.equipment_data[equipment][4]/self.work_week})
                    self.former_rate = []
                elif equipment == 'module_hauler':
                    self.loadout_rate_module = self.equipment_data[equipment][4]/self.work_week
                    self.loadout_rate_module_new = self.loadout_rate_module
                
        self.breakdown ={'loadout':[], 'press':[], 'chopper':[], 'bagger':[], 'module former':[], 'module hauler': []}  
        for trial in range(self.num_trials):
            self.breakdown['loadout'].append([])
            self.breakdown['press'].append([])
            self.breakdown['chopper'].append([])
            self.breakdown['bagger'].append([])
            self.breakdown['module former'].append([])
            self.breakdown['module hauler'].append([])

        self.m = self.harvest_schedule.shape[0]
        self.n = self.harvest_schedule.shape[1]
        
        self.all_refinery_actual = []
        self.all_ssl_actual = []
        self.all_degradation_ensiled_actual = []
        self.all_degradation_farm_actual = []
        self.all_demand = []
        self.all_farm_level = []
        self.harvest_hypothetical = []
        self.refinery_hypothetical = []
        self.hypothetical_ssl = []
        self.hypothetical_farm = []
        self.degradation_farm_average = []
        self.degradation_ssl_average = []
        self.refinery_graph = []
                   
    def main(self):
        for trial in range(self.num_trials):
            env = simpy.Environment() # sets up a new simpy env for every trial
            self.env = env
            self.trial_reset() # resets the simpy constructs and data structures for recording the information
            self.env.process(self.create_loadout_rate())
            self.env.process(self.harvest()) #triggers the harvest schedule, JIT_schedule and preprocessing every period
            self.env.process(self.farm_transport())
            self.env.process(self.moniter_ssl())# checks the ssl transport schedule for refinery deliveries
            #self.env.process(self.degradation_field()) # counts degredation of sitting sorghum at the fields
            #self.env.process(self.degradation_ensiled()) # counts degradation of ensiled sorghum
            self.env.process(self.record_data()) # Records all of the trial specific data and appends it to trial constant data
            self.env.run(until=self.SIM_TIME) # planning horizon in hours
            self.all_demand.append(self.refinery.level)
        self.schedules()
        self.sim_results = {"demand": {"percent": 0, "average": 0, "stdev":0, "sem":0, "conf int":"N/a", 'range':[0,0], "conf":{'90':0, '95':0}}, "telehandler rate":{"average": 0, "stdev":0, "sem":0, "conf int":0, 'range':[0,0]}, "press rate":{"average": 0, "stdev":0, "sem":0, "conf int":0, 'range':[0,0]}, "chopper rate":{"average": 0, "stdev":0, "sem":0, "conf int":0, 'range':[0,0]}, "bagger rate":{"average": 0, "stdev":0, "sem":0, "conf int":0, 'range':[0,0]}, "module former rate":{"average": 0, "stdev":0, "sem":0, "conf int":0, 'range':[0,0]}, "module hauler rate":{"average": 0, "stdev":0, "sem":0, "conf int":0, 'range':[0,0]}}
        self.simulation_results()
        self.round_conf_int()
        #self.graphs()
        #degradation_cost = 0
        #for period in range(self.m):
         #   degradation_cost = degradation_cost + ((self.degradation_ssl_average[period]-self.degradation_ensiled_expected[period])*65+(self.degradation_farm_average[period]-self.degradation_farm_expected[period])*65)
        #print('The extra cost incured due to unforseen degradation is: ',degradation_cost,' dollars')
        
    def simulation_results(self):        
        for equipment in self.configuration:
            if equipment == 'press':
                print('The average compression rate in MG/hour:',np.mean(self.press_rate))
                self.sim_results['press rate'].update({'average':round(np.mean(self.press_rate),2)})
                self.sim_results['press rate'].update({'stdev':round(np.std(self.press_rate),2)})
                self.sim_results['press rate'].update({'sem':round(stat.sem(self.press_rate),2)})
                self.sim_results['press rate'].update({'conf int':stat.norm.interval(.95,round(np.mean(self.press_rate),1),round(np.std(self.press_rate),1))})
                self.sim_results['press rate']['range'][0] = round(min(self.press_rate),2)
                self.sim_results['press rate']['range'][1] = round(max(self.press_rate),2)
            if equipment == 'chopper':
                print('The average chopper rate in MG/hour:',np.mean(self.chopper_rate))
                self.sim_results['chopper rate'].update({'average':round(np.mean(self.chopper_rate),2)})
                self.sim_results['chopper rate'].update({'stdev':round(np.std(self.chopper_rate),2)})
                self.sim_results['chopper rate'].update({'sem':round(stat.sem(self.chopper_rate),2)})
                self.sim_results['chopper rate'].update({'conf int':stat.t.interval(0.95,len(self.chopper_rate)-1, loc=np.mean(self.chopper_rate), scale=stat.sem(self.chopper_rate))})
                self.sim_results['chopper rate']['range'][0] = round(min(self.chopper_rate),2)
                self.sim_results['chopper rate']['range'][1] = round(max(self.chopper_rate),2)
            if equipment == 'bagger':
                print('The average bagger rate in MG/hour:',np.mean(self.bagger_rate))
                self.sim_results['bagger rate'].update({'average':round(np.mean(self.bagger_rate),2)})
                self.sim_results['bagger rate'].update({'stdev':round(np.std(self.bagger_rate),2)})
                self.sim_results['bagger rate'].update({'sem':round(stat.sem(self.bagger_rate),2)})
                self.sim_results['bagger rate'].update({'conf int':stat.t.interval(0.95,len(self.bagger_rate)-1, loc=np.mean(self.bagger_rate), scale=stat.sem(self.bagger_rate))})
                self.sim_results['bagger rate']['range'][0] = round(min(self.bagger_rate),2)
                self.sim_results['bagger rate']['range'][1] = round(max(self.bagger_rate),2)
            if equipment == 'module_former':
                print('The average module former rate in MG/hour:',np.mean(self.former_rate))
                self.sim_results['module former rate'].update({'average':round(np.mean(self.former_rate),2)})
                self.sim_results['module former rate'].update({'stdev':round(np.std(self.former_rate),2)})
                self.sim_results['module former rate'].update({'sem':round(stat.sem(self.former_rate),2)})
                self.sim_results['module former rate'].update({'conf int':stat.t.interval(0.95,len(self.former_rate)-1, loc=np.mean(self.former_rate), scale=stat.sem(self.former_rate))})
                self.sim_results['module former rate']['range'][0] = round(min(self.former_rate),2)
                self.sim_results['module former rate']['range'][1] = round(max(self.former_rate),2)
            if equipment == 'module_hauler':
                print('The average loadout rate for module hauler in MG/hour:',np.mean(self.loadout_rates_module)) 
                self.sim_results['module hauler rate'].update({'average':round(np.mean(self.loadout_rates_module),2)})
                self.sim_results['module hauler rate'].update({'stdev':round(np.std(self.loadout_rates_module),2)})
                self.sim_results['module hauler rate'].update({'sem':round(stat.sem(self.loadout_rates_module),2)})
                self.sim_results['module hauler rate'].update({'conf int':stat.t.interval(0.95,len(self.loadout_rates_module)-1, loc=np.mean(self.loadout_rates_module), scale=stat.sem(self.loadout_rates_module))})
                self.sim_results['module hauler rate']['range'][0] = round(min(self.loadout_rates_module),2)
                self.sim_results['module hauler rate']['range'][1] = round(max(self.loadout_rates_module),2)
            if equipment == 'loadout':
                print('Average telehandler loadout rate in MG/hour:',np.mean(self.loadout_rates_standard))
                self.sim_results['telehandler rate'].update({'average':round(np.mean(self.loadout_rates_standard),2)})
                self.sim_results['telehandler rate'].update({'stdev':round(np.std(self.loadout_rates_standard),2)})
                self.sim_results['telehandler rate'].update({'sem':round(stat.sem(self.loadout_rates_standard),2)})
                self.sim_results['telehandler rate'].update({'conf int':stat.t.interval(0.95,len(self.loadout_rates_standard)-1, loc=np.mean(self.loadout_rates_standard), scale=stat.sem(self.loadout_rates_standard))})
                self.sim_results['telehandler rate']['range'][0] = round(min(self.loadout_rates_standard),2)
                self.sim_results['telehandler rate']['range'][1] = round(max(self.loadout_rates_standard),2)
    
        self.percent_met = np.mean(self.all_demand)/self.demand*100
        self.sim_results['demand'].update({'percent':round(self.percent_met,2)})
        self.sim_results['demand'].update({'average':round(np.mean(self.all_demand),2)})
        self.sim_results['demand'].update({'stdev':round(np.std(self.all_demand),2)})
        self.sim_results['demand'].update({'sem':round(stat.sem(self.all_demand),2)})
        self.sim_results['demand']['range'][0] = round(min(self.all_demand),2)
        self.sim_results['demand']['range'][1] = round(max(self.all_demand),2)
        
        print(self.percent_met,'% of the ',self.demand,'MG demand was met over the current planning horizon for',self.num_trials,'samples')
        
        count_90 = 0
        count_95 = 0
        for demand in self.all_demand:
            if demand >= .95*self.demand:
                count_90 += 1
                count_95 += 1
            elif demand >= .9*self.demand:
                count_90 += 1
            else:
                pass
        self.sim_results['demand']['conf'].update({'90':float(count_90/self.num_trials*100)})
        self.sim_results['demand']['conf'].update({'95':float(count_95/self.num_trials*100)})

    '''
    Simulation Environment 
    '''

    def harvest(self):
        for period in range(self.m):
            for farm in range(self.n):
                if self.harvest_schedule[period][farm] != 0:
                    self.harvest_actual[period][farm]=max(1/10*self.harvest_schedule[period][farm],np.random.normal(self.harvest_schedule[period][farm], 1/5*self.harvest_schedule[period][farm]))
                    #self.harvest_actual[period][farm] = max(0,self.harvest_schedule[period][farm])
                    self.farms[farm].put(self.harvest_actual[period][farm])
                else:
                    pass
            yield self.env.timeout(self.work_week)
    


    def farm_transport(self):
        for period in range(self.m):
            for farm in range(self.n):
                if self.jit_farm_transport[period][farm] != 0:
                    self.env.process(self.JIT_delivery(period, farm))
                if self.farm_transport_schedule[period][farm] != 0:
                    self.env.process(self.preprocessing(period, farm))
            yield self.env.timeout(self.work_week)

            
    
    def preprocessing(self, period, farm):
        x = min(self.farm_transport_schedule[period][farm],self.farms[farm].level)
        if x > 0:
            self.farms[farm].get(x)
            with self.ssl[self.farm_ssl[farm]][0].request() as req:
                yield req
                yield self.env.timeout(x/(self.equip_in_ssl[self.farm_ssl[farm]][0]*self.loadout_rate_standard_new))
            self.before_ssl[self.farm_ssl[farm]].put(x)
            self.env.process(self.use_equipment(period, farm, x))
            self.before_ssl[self.farm_ssl[farm]].get(x)
            self.ssl_container[self.farm_ssl[farm]].put(x)
            self.ssl_level_actual[period][self.farm_ssl[farm]] = self.ssl_container[self.farm_ssl[farm]].level



    def use_equipment(self, period, farm, x):
        i=1
        for equipment in self.config_rate:
            equipment_rate = min(1.25*self.config_rate[equipment],max(1/10*self.config_rate[equipment],np.random.normal(self.config_rate[equipment],1/5*self.config_rate[equipment])))
            if equipment == 'press':
                self.press_rate.append(equipment_rate)
            if equipment == 'chopper':
                self.chopper_rate.append(equipment_rate)
            if equipment == 'bagger':
                self.bagger_rate.append(equipment_rate)
            if equipment == 'module_former':
                self.former_rate.append(equipment_rate)
            with self.ssl[self.farm_ssl[farm]][i].request() as req:
                yield req
                yield self.env.timeout(x/(equipment_rate*self.equip_in_ssl[self.farm_ssl[farm]][i]))
            i=i+1
            yield self.env.timeout(.25)
    


    def moniter_ssl(self):
        for period in range(self.m):      
            for ssl in range(self.num_ssl):
                if self.ssl_transport_schedule[period][ssl] !=0:
                    self.env.process(self.refinery_transport(ssl, period))
                else:
                    pass
            yield self.env.timeout(self.work_week)


            
    def refinery_transport(self, ssl, period):
        whats_left = self.ssl_transport_schedule[period][ssl]
        while whats_left != 0:
            #if self.ssl_container[ssl].level == 0 and self.before_ssl[ssl] == 0:
                #break
            if self.ssl_container[ssl].level > 0:
                y=min(whats_left,self.ssl_container[ssl].level)
                self.ssl_container[ssl].get(y)
                if 'module_hauler' in self.configuration:
                    with self.ssl[ssl][0].request() as req:
                        yield req
                        yield self.env.timeout(y/(self.equip_in_ssl[ssl][0]*self.loadout_rate_module_new))
                    self.refinery.put(y)
                    whats_left = whats_left - y
                else:
                    with self.ssl[ssl][0].request() as req:
                        yield req
                        yield self.env.timeout(y/(self.equip_in_ssl[ssl][0]*self.loadout_rate_standard_new))
                    self.refinery.put(y)
                    whats_left = whats_left - y
            else:
                pass
            yield self.env.timeout(1)

        '''if self.ssl_container[ssl].level > 0:
            z = self.ssl_container[ssl].level
            self.ssl_container[ssl].get(z)
            if 'module_hauler' in self.configuration:
                with self.ssl[ssl][0].request() as req:
                    yield req
                    yield self.env.timeout(z/(self.equip_in_ssl[ssl][0]*self.loadout_rate_module_new))
            else:
                with self.ssl[ssl][0].request() as req:
                    yield req
                    yield self.env.timeout(z/(self.equip_in_ssl[ssl][0]*self.loadout_rate_standard_new))
            self.refinery.put(z)'''
    


    def JIT_delivery(self, period, farm):
        y = min(self.jit_farm_transport[period][farm],self.farms[farm].level)
        if y > 0:
            self.farms[farm].get(y)
            if self.configuration[0] == 'whole_stalk':
                yield self.env.timeout(y/self.config_rate['chopper'])
            yield self.env.timeout(y/(self.equip_in_ssl[self.farm_ssl[farm]][0]*self.loadout_rate_standard_new))
            self.refinery.put(y)
        else:
            pass



    def create_loadout_rate(self):
        for period in range(self.m):
            if 'module_hauler' in self.configuration:
                self.loadout_rate_module_new = min(1.25*self.loadout_rate_module,max(1/10*self.loadout_rate_module,np.random.normal(self.loadout_rate_module, 1/5*self.loadout_rate_module)))
                self.loadout_rates_module.append(self.loadout_rate_module_new)
            self.loadout_rate_standard_new = min(1.25*self.loadout_rate_standard,max(1/10*self.loadout_rate_standard,np.random.normal(self.loadout_rate_standard, 1/5*self.loadout_rate_standard)))
            self.loadout_rates_standard.append(self.loadout_rate_standard_new)
            yield self.env.timeout(self.work_week)



    def degradation_field(self): 
        x = 0
        y = 0
        for period in range(self.m):
            yield self.env.timeout(self.work_week-1)
            for farm in range(self.n):
                if self.farms[farm].level > 0:
                    if self.sysnum in [0,1,2,3,4,5,6,7]:
                        degradation_amount = self.farms[farm].level/9
                        self.degraded_field.put(degradation_amount)
                    if self.sysnum in [8,9,10,11,12,13,14,15]:
                        degradation_amount = self.farms[farm].level/5
                        self.degraded_field.put(degradation_amount)
                else:
                    pass
                if self.farm_inventory[period][farm] > 0:
                    if self.sysnum in [0,1,2,3,4,5,6,7]:
                        degradation_amount = self.farm_inventory[period][farm]/9
                        x=x+degradation_amount
                    if self.sysnum in [8,9,10,11,12,13,14,15]:
                        degradation_amount = self.farm_inventory[period][farm]/5
                        x=x+degradation_amount
                else:
                    pass
            y=y+x
            x=0
            self.degradation_farm_expected.append(y)
            yield self.env.timeout(1)                        
       


    def degradation_ensiled(self):
        x=0
        y=0
        for period in range(self.m):
            yield self.env.timeout(self.work_week-1)
            for ssl in self.ssl_container:
                if self.ssl_container[ssl].level > 0:
                    if self.sysnum in [0,4,8,12]:
                        degradation_amount = self.ssl_container[ssl].level/5
                        self.degraded_ensiled.put(degradation_amount)
                    if self.sysnum in [1,5,9,13]:
                        degradation_amount = self.ssl_container[ssl].level/100
                        self.degraded_ensiled.put(degradation_amount)
                    if self.sysnum in [2,6,10,14]:
                        degradation_amount = self.ssl_container[ssl].level/80
                        self.degraded_ensiled.put(degradation_amount)
                    if self.sysnum in [3,7,11,15]:
                        pass
                else:
                    pass
                if self.ssl_inventory[period][int(ssl)] > 0:
                    if self.sysnum in [0,4,8,12]:
                        degradation_amount = self.ssl_inventory[period][int(ssl)]/5
                        x=x+degradation_amount
                    if self.sysnum in [1,5,9,13]:
                        degradation_amount = self.ssl_inventory[period][int(ssl)]/100
                        x=x+degradation_amount
                    if self.sysnum in [2,6,10,14]:
                        degradation_amount = self.ssl_inventory[period][int(ssl)]/80
                        x=x+degradation_amount               
            y=y+x
            x=0
            self.degradation_ensiled_expected.append(y)
            yield self.env.timeout(1)


    '''
    Data Collection and Reset
    '''


    def schedules(self):
        total2 = 0
        self.refinery_total = 0
        total6 = 0
        total4 = 0
        total8 = 0
        for period in range(self.m):
            for farm in range(self.n):
                total2 = total2 + self.harvest_schedule[period][farm] 
                total6 = total6 + self.farm_transport_schedule[period][farm]
                self.refinery_total = self.refinery_total + self.jit_farm_transport[period][farm]
                total8 = total8 + self.farm_inventory[period][farm]
            self.hypothetical_farm.append(total8)
            self.harvest_hypothetical.append(total2)
            for ssl in self.ssl_container:
                self.refinery_total = self.refinery_total + self.ssl_transport_schedule[period][ssl] 
                total4 = total4 + self.ssl_inventory[period][ssl]
            self.hypothetical_ssl.append(total4)
            self.refinery_hypothetical.append(self.refinery_total)
            total4 = 0
            total8 = 0
        self.refinery_graph = np.mean(self.all_refinery_actual, axis=0)
        self.ssl_graph = np.mean(self.all_ssl_actual, axis=0)
        self.farm_graph = np.mean(self.all_farm_level, axis=0)
        self.harvest_actual = np.mean(self.harvest_actual, axis=0)
        #print(self.harvest_actual)

    def record_data(self):
        total = 0
        total5 = 0
        total7 = 0
        #yield self.env.timeout(self.work_week)
        for period in range(self.m):
            for farm in range(self.n):   
                total = total + self.harvest_actual[period][farm]
            self.total_harvest.append(total)
            yield self.env.timeout(self.work_week)
            for farm in range(self.n):
                total7 = total7 + self.farms[farm].level
            for ssl in self.ssl_container:
                total5 = total5 + self.ssl_container[ssl].level
            self.actual_farm.append(total7)
            self.actual_ssl.append(total5)
            self.degradation_ensiled_actual.append(self.degraded_ensiled.level)
            self.degradation_farm_actual.append(self.degraded_field.level)
            self.refinery_actual.append(self.refinery.level)
            #print('harvested amount @ ',self.env.now,'acutal: ', total, '   hypothetical: ', total2)
            #print('total ssl inventory @  ',self.env.now, '   acutal: ', total5, '   hypothetical: ', total4)
            #print('refinery level @ ',self.env.now, '  ', self.refinery.level)
            total5 = 0
            total7 = 0
        self.all_farm_level.append(self.actual_farm)
        self.all_refinery_actual.append(self.refinery_actual)
        self.all_ssl_actual.append(self.actual_ssl)
        self.all_degradation_ensiled_actual.append(self.degradation_ensiled_actual)
        self.all_degradation_farm_actual.append(self.degradation_farm_actual)
        


    def graphs(self):
        X = np.linspace(0,1080,27)
        
        print('\nRefinery Inventory level v.s. Time')
        plt.plot(X, self.refinery_hypothetical, color="blue", linewidth=1.0, linestyle="-", label='scheduled refinery inventory')
        plt.plot(X, self.refinery_graph, color="red", linewidth=1.0, linestyle="-", label='actual refinery inventory')
        plt.xlim(0,1080)
        plt.ylim(0,230000)
        plt.xticks(np.linspace(0,1080,10,endpoint=True))
        plt.yticks(np.linspace(0,230000,12,endpoint=True))
        plt.legend(loc='upper left', frameon=False)
        plt.show()
        

    def trial_reset(self):           
        self.farms = []
        # create farms
        for farm in range(self.n):
            self.farms.append(simpy.Container(self.env, 10000000, init=0)) # creates all the farm containers
        self.refinery = simpy.Container(self.env, capacity=100000000, init=0) # creates refinery containers
        self.degraded_ensiled = simpy.Container(self.env, capacity=100000000, init=0) # degradation containers
        self.degraded_field = simpy.Container(self.env, capacity=100000000, init=0)
        
        self.farm_transport_schedule = np.zeros((self.m,self.n)).tolist()
        self.harvest_actual = np.zeros((self.m,self.n)).tolist()
        self.jit_farm_transport = np.zeros((self.m,self.n)).tolist()  
        self.farm_inventory = np.zeros((self.m,self.n)).tolist()

        self.ssl_route = [] # distance from ssl to orgin (refinery)
        for coord in self.coord_s:
            self.ssl_route.append(math.sqrt(self.coord_s[coord][1]**(2)+self.coord_s[coord][0]**(2)))

        self.ssl = {}
        self.equip_in_ssl = {} # dictionary for ssl configuration
        self.before_ssl = {}
        self.ssl_container = {} # dictionary relating ssl site location to container with proper capacity
        self.ssl_location = {} # x,y location of ssl
        for solution in self.solutions:
            aa = solution[0]
            cc = solution[1]
            bb = re.split('\W', aa)
            if bb[0] == 'ssl_configuration_selection':
                i=1
                z = len(self.ssl_configurations[int(bb[2])])-1
                self.ssl[int(bb[1])] = []
                for number in range(z):
                    self.ssl[int(bb[1])].append(simpy.Resource(self.env, capacity=1))
                    i=i+1
                self.equip_in_ssl[int(bb[1])] = self.ssl_configurations[int(bb[2])][1:]
                self.before_ssl[int(bb[1])] = simpy.Container(self.env, capacity=self.ssl_configurations[int(bb[2])][0], init=0)
                self.ssl_container[int(bb[1])] = simpy.Container(self.env, capacity=self.ssl_configurations[int(bb[2])][0], init=0)
                self.ssl_location[int(bb[1])] = self.coord_s[int(bb[1])]
            else:
                pass    

        self.ssl_level_actual = np.zeros((self.m,self.num_ssl)).tolist()
        self.ssl_transport_schedule = np.zeros((self.m+1,self.num_ssl)).tolist()
        self.ssl_inventory = np.zeros((self.m,self.num_ssl)).tolist()
          
        self.farm_ssl = {} # shows which farm corresponds to using which ssl      
        for solution in self.solutions:
            aa = solution[0]
            cc = solution[1]
            bb = re.split('\W', aa)
            if bb[0] == 'farm_to_ssl':
                self.farm_ssl.update({int(bb[1]):int(bb[2])})
            if bb[0] == 'shipped_farm_ssl':  # populate the farm transport schedule from algorithm solution
                self.farm_transport_schedule[int(bb[1])][int(bb[2])] = cc
            if bb[0] == 'shipped_ssl_refinery':   # populate the ssl transportation schedule from algorithm solution
                self.ssl_transport_schedule[int(bb[1])][int(bb[2])] = cc
            if bb[0] == 'shipped_jit':
                self.jit_farm_transport[int(bb[1])][int(bb[2])] = cc
            if bb[0] == 'inventory_level_ssl':
                self.ssl_inventory[int(bb[1])][int(bb[2])] = cc
            if bb[0] == 'inventory_level_farm':
                self.farm_inventory[int(bb[1])][int(bb[2])] = cc       
            else:
                pass

        self.degradation_farm_expected = []
        self.degradation_ensiled_expected = []  
        self.total_harvest = []
        self.refinery_actual = []
        self.actual_ssl = []
        self.degradation_ensiled_actual = []
        self.degradation_farm_actual = []
        self.actual_farm = []



    def round_conf_int(self):
        for dic in self.sim_results:
            if dic == 'demand':
                pass
            elif self.sim_results[dic]['conf int'] != 0:
                x = list(self.sim_results[dic]['conf int'])
                x[0] = round(x[0], 2)
                x[1] = round(x[1], 2)
                self.sim_results[dic]['conf int'] = x
            else:
                pass