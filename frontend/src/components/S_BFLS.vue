<template>
<div class="section wrap">
    <h1 class="title">Sorghum - Logistics Support</h1>
    <Map class="map" v-model="mapInfo" ref="map"></Map>
    <div class="paramDescription">
      <div class="title is-4">Optimization Parameters</div>
      <div class="subtitle is-6">Note: if parameter unspecified default value is accepted</div>
    </div>
    
    <div class="params">
        <div class="field">
            <label class="label">Projected Demand (Mg)</label>
            <div class="control">
                <input class="input" type="text" v-model="model.demand" @change="changeProportion">
            </div>
        </div>
        <div class="field">
            <label class="label">Length Planning Horizon (wk)</label>
            <div class="control">
                <input class="input" type="text" v-model="model.horizon">
            </div>
        </div>
        <div class="field">
          <div class="control">
            <label class="label">Equipment Configuration</label>  
            <div class="select">
              <select
                v-model="model.sysnum"
              >
                <option 
                  v-bind:key=index
                  v-for="(config, index) in configurations"
                  v-bind:value="index"
                >{{config}}</option>
              </select>
            </div>
          </div>
        </div>
        <ListInput 
          v-bind:list='model.ssl_sizes' 
          v-on:listChange='model.ssl_sizes = $event'
          v-bind:label="'SSL Sizes'"
          v-bind:placeHolders="placeHolders.sslSizes"
        ></ListInput>
        <ListInput 
          v-bind:list='model.harvest_progress' 
          v-on:listChange='model.harvest_progress = $event'
          v-bind:label="'Harvest Progress'"
          v-bind:placeHolders="placeHolders.harvestProgress"
        ></ListInput>
      <div class="advancedParams">
        <div v-if="advancedOptions">
          <div class="title is-size-5">Additional Parameters</div>
          <OptimizationForm 
            ref = "opForm"
            v-on:formChange='customModel = $event'
            v-bind:model='model'
          ></OptimizationForm>
        </div>
      </div>
    </div> 
    <div class="buttons">
      <button
        v-if="advancedOptions"
        class="advancedOptions button is-link"
        v-on:click="showAdvancedOptions()"
      >
        Hide Advanced Options
      </button>
      <button
        v-else 
        class="advancedOptions button is-link"
        v-on:click="showAdvancedOptions()"
      >
        Show Advanced Options
      </button>
      <button 
        class="button optimize is-warning" 
        v-on:click="optimize()"
      >
        Optimize
      </button>
      <button 
        class="button show_input is-warning" 
        v-on:click="show_input()"
		v-if="showInput"
      >
        Show Input
      </button>
    </div>
    <br>
    <div 
      class="results"
      v-if="showSolution"
    >
      <div class="title is-size-3">Results</div>
      <div class="title is-5">Cost Breakdown</div>
      <div class="costChart">
          <pie-chart 
            prefix="$" 
            :data="chart_data"
            class="pieChart" 
            width="48%"
          ></pie-chart>
          <div class="list is-hoverable" width="40%">
            <div class="list-item">Farm to SSL Cost: ${{chart_info['farm_ssl_trans_cost']}}</div>
            <div class="list-item">SSL to Refinery Cost: ${{chart_info['ssl_ref_trans_cost']}}</div>
            <div class="list-item">Farm Holding Cost: ${{chart_info['farm_holding_cost']}}</div>
            <div class="list-item">SSL Holding Cost: ${{chart_info['ssl_holding_cost']}}</div>
            <div class="list-item">Local Ownership Cost: ${{chart_info['local_ownership']}}</div>
            <div class="list-item">Operation Cost: ${{chart_info['operation_cost']}}</div>
            <div class="list-item is-active">Total Cost: ${{chart_info['total_cost']}}</div>
          </div>
      </div>
      
      <div class="title is-5">Simulation Statistics</div>
      <div class="subtitle is-6">Based on 100 Replications</div> 
      <div class="simResults">
        <div>
          <div>Configuration: {{configurations[model.sysnum]}}</div>
          <div>90% of demand met {{sim_response['demand']['conf']['90']}}% of the time</div>
          <div>95% of demand met {{sim_response['demand']['conf']['95']}}% of the time</div>
          <div>Average amount of demand met {{sim_response['demand']['percent']}}%</div>
        </div>
        <table class="table is-striped">
          <tr>
            <th class="table is-hoverable">Descriptive Statistics</th>
            <th class="table is-hoverable">Mean</th>
            <th class="table is-hoverable">Std. Dev</th>
            <th class="table is-hoverable">SE Mean</th>
            <th class="table is-hoverable">95% CI</th>
            <th class="table is-hoverable">Range (min,max)</th>
          </tr>
          <tr>
            <td class="table is-hoverable">Demand</td>
            <td class="table is-hoverable" v-html="sim_response['demand']['average'] + ' Mg'"></td>
            <td class="table is-hoverable" v-html="sim_response['demand']['stdev'] + ' Mg'"></td>
            <td class="table is-hoverable" v-html="sim_response['demand']['sem'] + ' Mg'"></td>
            <td class="table is-hoverable" v-html="sim_response['demand']['conf int']"></td>
            <td class="table is-hoverable" v-html="'(' + sim_response['demand']['range'][0] + ', ' + sim_response['demand']['range'][1] + ')' + ' Mg'"></td>
          </tr>
           <tr>
            <td class="table is-hoverable">Telehandler</td>
            <td class="table is-hoverable" v-html="sim_response['telehandler rate']['average'] + ' Mg/hr'"></td>
            <td class="table is-hoverable" v-html="sim_response['telehandler rate']['stdev'] + ' Mg/hr'"></td>
            <td class="table is-hoverable" v-html="sim_response['telehandler rate']['sem'] + ' Mg/hr'"></td>
            <td class="table is-hoverable" v-html="sim_response['telehandler rate']['conf int'] + ' Mg/hr'"></td>
            <td class="table is-hoverable" v-html="'(' + sim_response['telehandler rate']['range'][0] + ', ' + sim_response['telehandler rate']['range'][1] + ')' + ' Mg/hr'"></td>
          </tr>
          <tr>
            <td class="table is-hoverable">Forage Chopper</td>
            <td class="table is-hoverable" v-html="sim_response['chopper rate']['average'] + ' Mg/hr'"></td>
            <td class="table is-hoverable" v-html="sim_response['chopper rate']['stdev'] + ' Mg/hr'"></td>
            <td class="table is-hoverable" v-html="sim_response['chopper rate']['sem'] + ' Mg/hr'"></td>
            <td class="table is-hoverable" v-html="sim_response['chopper rate']['conf int'] + ' Mg/hr'"></td>
            <td class="table is-hoverable" v-html="'(' + sim_response['chopper rate']['range'][0] + ', ' + sim_response['chopper rate']['range'][1] + ')' + ' Mg/hr'"></td>

          </tr>
          <tr>
            <td class="table is-hoverable">Press</td>
            <td class="table is-hoverable" v-html="sim_response['press rate']['average'] + ' Mg/hr'"></td>
            <td class="table is-hoverable" v-html="sim_response['press rate']['stdev'] + ' Mg/hr'"></td>
            <td class="table is-hoverable" v-html="sim_response['press rate']['sem'] + ' Mg/hr'"></td>
            <td class="table is-hoverable" v-html="sim_response['press rate']['conf int'] + ' Mg/hr'"></td>
            <td class="table is-hoverable" v-html="'(' + sim_response['press rate']['range'][0] + ', ' + sim_response['press rate']['range'][1] + ')' + ' Mg/hr'"></td>

          </tr>
          <tr>
            <td class="table is-hoverable">Bagger</td>
            <td class="table is-hoverable" v-html="sim_response['bagger rate']['average'] + ' Mg/hr'"></td>
            <td class="table is-hoverable" v-html="sim_response['bagger rate']['stdev'] + ' Mg/hr'"></td>
            <td class="table is-hoverable" v-html="sim_response['bagger rate']['sem'] + ' Mg/hr'"></td>
            <td class="table is-hoverable" v-html="sim_response['bagger rate']['conf int'] + ' Mg/hr'"></td>
            <td class="table is-hoverable" v-html="'(' + sim_response['bagger rate']['range'][0] + ', ' + sim_response['bagger rate']['range'][1] + ')' + ' Mg/hr'"></td>

          </tr>
          <tr>
            <td class="table is-hoverable">Module Former</td>
            <td class="table is-hoverable" v-html="sim_response['module former rate']['average'] + ' Mg/hr'"></td>
            <td class="table is-hoverable" v-html="sim_response['module former rate']['stdev'] + ' Mg/hr'"></td>
            <td class="table is-hoverable" v-html="sim_response['module former rate']['sem'] + ' Mg/hr'"></td>
            <td class="table is-hoverable" v-html="sim_response['module former rate']['conf int'] + ' Mg/hr'"></td>
            <td class="table is-hoverable" v-html="'(' + sim_response['module former rate']['range'][0] + ', ' + sim_response['module former rate']['range'][1] + ')' + ' Mg/hr'"></td>

          </tr>
          <tr>
            <td class="table is-hoverable">Module Hauler</td>
            <td class="table is-hoverable" v-html="sim_response['module hauler rate']['average'] + ' Mg'"></td>
            <td class="table is-hoverable" v-html="sim_response['module hauler rate']['stdev'] + ' Mg'"></td>
            <td class="table is-hoverable" v-html="sim_response['module hauler rate']['sem'] + ' Mg'"></td>
            <td class="table is-hoverable" v-html="sim_response['module hauler rate']['conf int'] + ' Mg'"></td>
            <td class="table is-hoverable">({{sim_response['module hauler rate']['range'][0]}} , {{sim_response['module hauler rate']['range'][1]}}) Mg/hr</td>
          </tr>
        </table>
      </div>
    </div>
    <Csv_Formatter class="csv_download" ref="csv_download"></Csv_Formatter>
</div>
</template>

<script>
import { validators, component as VueFormGenerator } from 'vue-form-generator'
import axios from 'axios'
import Map from './Map'
import Csv_Formatter from './Csv_Formatter'
import OptimizationForm from './OptimizationForm'
import ListInput from './ListInput'
import NProgress from 'nprogress'

export default {
  components: {
      VueFormGenerator,
      'Map' : Map,
      'Csv_Formatter' : Csv_Formatter,
      'ListInput' : ListInput,
      'OptimizationForm' : OptimizationForm,
  },
  data() {
    return {
      response: [],
      placeHolders: {
        sslSizes: ["small (Mg)", "medium (Mg)", "large (Mg)"],
        harvestProgress: [
          "% demand harvested week 1",
          "% demand harvested week 2",
          "% demand harvested week 3",
          "% demand harvested week 4",
          "% demand harvested week 5",
          "% demand harvested week 6",
          "% demand harvested week 7",
          "% demand harvested week 8",
          "% demand harvested week 9",
          "% demand harvested week 10",
          "% demand harvested week 11",
          "% demand harvested week 12",
          "% demand harvested week 13",
        ],
      },
      configurations: [
            "[whole_stalk, loadout, chopper]",
            "[whole_stalk, loadout, chopper, bagger]",
            "[whole_stalk, loadout, chopper, bunker]",
            "[whole_stalk, loadout, chopper, module_former, module_hauler]",
            "[whole_stalk, loadout, chopper, press]",
            "[whole_stalk, loadout, chopper, press, bagger]",
            "[whole_stalk, loadout, chopper, press, bunker]",
            "[whole_stalk, loadout, chopper, press, module_former, module_hauler]",
            "[forage_chop, loadout]",
            "[forage_chop, loadout, bagger]",
            "[forage_chop, loadout, bunker]",
            "[forage_chop, loadout, module_former, module_hauler]",
            "[forage_chop, loadout, press]",
            "[forage_chop, loadout, press, bagger]",
            "[forage_chop, loadout, press, bunker]",
            "[forage_chop, loadout, press, module_former, module_hauler]"
        ],
      mapInfo: {},
      showSolution: false,
      showInput: false,
      customForm: false,
      showOptButton: false,
      customModel: {},
      chart_data: [],
      chart_info: {},
      advancedOptions: false,
      model: {
        "sysnum": 0,
        "moisture": 0.7,
        "demand": 20000,
        "horizon": 26,
        "num_fields": 120,
        "num_ssls": 60,
        "ssl_sizes": [2500, 5000, 10000],
        "harvest_progress": [5, 5, 6, 7, 10, 11, 12, 11, 9, 8, 6, 5, 5],
        "field": {
        "dry_yield": 21,
        "radius": 32,
        "proportion_devoted": .003,
        "area_ratio": [1, 10]
        },
        "price": 65,
        "interest_rate": 0.05,
        "insurance_rate": 0.008,
        "tax_rate": 0.01,
        "cost": {
            "equipment": {
            "loadout": [94000, 5, 28200, 0.37, 847],
            "press": [300000, 5, 120000, 0.1374, 908],
            "chopper": [22000, 5, 8800, 0, 9240],
            "bagger": [50000, 5, 20000, 0.7, 2000],
            "module_former": [450000, 5, 217234, 1.0319, 800],
            "module_hauler": [375000, 8, 73530, 0.2766, 3620]
            },
            "bunker_annual_own": 5600,
            "ssl_annual_own": 0.36,
            "base_infield": 0.58,
            "base_highway": 0.1,
            "transport_coef": {
                "compressed": 0.8,
                "whole_stalk": 1.1,
                "in_module": 0.7
            }
            },
        "degrade": {
            "whole_stalk": 9,
            "chopped": 5,
            "in_bunker": 80,
            "in_bag": 100
        },
        "configurations": [
            ["whole_stalk", "loadout", "chopper"],
            ["whole_stalk", "loadout", "chopper", "bagger"],
            ["whole_stalk", "loadout", "chopper", "bunker"],
            ["whole_stalk", "loadout", "chopper", "module_former", "module_hauler"],
            ["whole_stalk", "loadout", "chopper", "press"],
            ["whole_stalk", "loadout", "chopper", "press", "bagger"],
            ["whole_stalk", "loadout", "chopper", "press", "bunker"],
            ["whole_stalk", "loadout", "chopper", "press", "module_former", "module_hauler"],
            ["forage_chop", "loadout"],
            ["forage_chop", "loadout", "bagger"],
            ["forage_chop", "loadout", "bunker"],
            ["forage_chop", "loadout", "module_former", "module_hauler"],
            ["forage_chop", "loadout", "press"],
            ["forage_chop", "loadout", "press", "bagger"],
            ["forage_chop", "loadout", "press", "bunker"],
            ["forage_chop", "loadout", "press", "module_former", "module_hauler"]
          ]
        
      },
      new_input: true,
      op_response: {},
      sim_response: {
            "demand": {
              "percent": 0, 
              "average": 0, 
              "stdev":0, 
              "sem":0, 
              "conf int":"N/a", 
              'range':[0,0], 
              "conf":{'90':0, '95':0}
              }, 
          "telehandler rate":{
              "average": 0, 
              "stdev":0, 
              "sem":0, 
              "conf int":0, 
              "range":[0,0]
              }, 
          "press rate":{
              "average": 0, 
              "stdev":0, 
              "sem":0, 
              "conf int":0, 
              "range":[0,0]
              }, 
          "chopper rate":{
              "average": 0, 
              "stdev":0, 
              "sem":0, 
              "conf int":0, 
              "range":[0,0]
              }, 
          "bagger rate":{
              "average": 0, 
              "stdev":0, 
              "sem":0, 
              "conf int":0, 
              "range":[0,0]
              }, 
          "module former rate":{
              "average": 0, 
              "stdev":0, 
              "sem":0, 
              "conf int":0, 
              "range":[0,0]
              }, 
          "module hauler rate":{
            "average": 0, 
            "stdev":0, 
            "sem":0, 
            "conf int":0, 
            "range":[0,0]
            }
          }
    };
  },
  methods: {
    useDefault() {
      this.model = this.model;
      this.showOptimize();
      this.customForm = false;
    },
    showAdvancedOptions() {
      this.advancedOptions = !this.advancedOptions;
    },
    showOptimize() {
      this.showOptButton = true;
    },
    customFormTrue() {
      this.customForm = true;
      this.showOptButton = true;
    },
    customFormFalse() {
      this.customForm = false;
      this.showOptButton = false;
    },
    parseApplyRoutes(response) {
      var len = response.summary.allocation_from_farm.length;
      var refinery = {"lat": this.model.refinery_location[0], "lng": this.model.refinery_location[1]}
      var routes = [];
      var i;
      this.$refs.map.removeRoutes();
      for (i=0; i < len; i++){
        var route = [];
        var f_id = response.summary.allocation_from_farm[i];
        var s_id = response.summary.allocation_to_ssl[i];
        var farm = this.model.Coord_f[f_id];
        var ssl = this.model.Coord_s[s_id];
        route.push(farm);
        route.push(ssl);
        route.push(refinery);
        this.$refs.map.addRoutes(route);
      }
    },
    optimize(event) {
      NProgress.start();
      var mapInfo = this.$refs.map.submitLocations();
      NProgress.start()

      if (mapInfo == "Refinery Missing") {
        alert("Need Refinery");
      } else {
        this.model.Coord_f = mapInfo.Coord_f;
        this.model.Coord_s = mapInfo.Coord_s;
        this.model.input_format = mapInfo.mode;
        this.model.refinery_location = mapInfo.refinery_location;
        this.model.new_input = this.new_input;
        console.log(this.model);
        axios
          .post('http://localhost:5000/s-bfls/', this.model)
          .then(response => {
              NProgress.done();
              var r = response.data
              this.op_response = r.op_response;
              this.$refs.csv_download.generateCsv(this.op_response.solution);
			        this.sim_response = r.sim_response;
              this.showSolution = true;
		          this.showInput = true;
              this.parseApplyRoutes(this.op_response);
              this.show_results(this.op_response["summary"]["cost"]);
              console.log("summary ",this.op_response["summary"]["cost"])
          })
        this.new_input = false;

      }
    },
    show_results(data) {
			this.chart_info = {}; this.showing_options = [];

            this.showing_options = false;
            this.chart_info['farm_ssl_trans_cost'] = Math.round(data.tran_farms_ssl);
            this.chart_info['ssl_ref_trans_cost'] = Math.round(data.tran_ssl_refinery);
            this.chart_info['farm_holding_cost'] = Math.round(data.farm_inventory);
            this.chart_info['ssl_holding_cost'] = Math.round(data.ssl_inventory);
            this.chart_info['local_ownership'] = Math.round(data.loc_own);
            this.chart_info['operation_cost'] = Math.round(data.operation);
            this.chart_info['total_cost'] = Math.round(data.total_ub);

            this.chart_data[0] = ['farm to ssl', Math.round(data.tran_farms_ssl)];
            this.chart_data[1] = ['ssl to refinery', Math.round(data.tran_ssl_refinery)];
            this.chart_data[2] = ['farm holding', Math.round(data.farm_inventory)];
            this.chart_data[3] = ['ssl holding', Math.round(data.ssl_inventory)];
            this.chart_data[4] = ['local ownership', Math.round(data.loc_own)];
            this.chart_data[5] = ['operations', Math.round(data.operation)];
    },
    show_input() {
        this.showInput = false;
		this.$refs.map.hide_results();
    },
    changeProportion() {
        this.model.field.proportion_devoted = (this.model.demand * 1.0) / 6666666;
    }
  }
}
</script>

<style>
div {
  text-align: left
}

.title {
  text-align: left;
}

.subtitle {
  margin-bottom: 1rem;
}

.map {
  grid-area: map;
}

.mapDescription {
  grid-area: mapDescription;
}

.paramDescription {
  grid-area: paramDescription; 
}

.params {
  grid-area: params;
  display: flex;
  justify-content: flex-start;
  flex-wrap: wrap;
}

.params .input {
  width: 18rem;
  margin-right: 1rem;
}

.buttons {
  grid-area: buttons;
  margin-top: 1rem;
}

.advancedOptions {
  width: 15rem;
  grid-area: optimize;
}

.wrap {
    display: grid;
    margin: 0;
    grid-template-columns: 1fr;
    grid-template-rows: auto;
    grid-template-areas: "title" "map" "paramDescription" "params" "buttons" "results";
}

.optimize {
  width: 110px;
}

.costChart {
  display: flex;
}

.pieChart {
  position: relative;
  width: 48%;
  float: right;
  display: inline;
}

.results {
  display: flex;
  flex-direction: column
}
</style>
