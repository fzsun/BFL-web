<template>
<div class="section wrap">
    <h1 class="title">Sorghum - Logistics Support</h1>
    <Map class="map" v-model="mapInfo" ref="map"></Map>
    <div class="paramDescription title is-size-4">Optimization Parameters</div>
    <div class="params">
      <div class="requiredParams">
        <div class="field defaultWidth">
            <label class="label">Projected Demand (Mg)</label>
            <div class="control">
                <input class="input" type="text" v-model="model.demand">
            </div>
        </div>
        <div class="field defaultWidth">
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
      </div>
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
    </div>
    <br>
    <div 
      class="results"
      v-if="showSolution"
    >
      <div class="title is-size-3">Simulation Results</div>
      <div class="sim_results">
        <div class="title is-size-5" v-html="'Percent of demand met: ' + sim_response['demand']['percent'] + '%'"></div>
        <table class="table1">
          <tr>
            <th class="table_header">Descriptive Statistics</th>
            <th class="table_header">Mean</th>
            <th class="table_header">Standard Deviation</th>
            <th class="table_header">SE Mean</th>
            <th class="table_header">95% Confidence Interval</th>
          </tr>
          <tr>
            <td class="table_row">Demand</td>
            <td class="table_row" v-html="sim_response['demand']['average'] + ' Mg'"></td>
            <td class="table_row" v-html="sim_response['demand']['stdev'] + ' Mg'"></td>
            <td class="table_row" v-html="sim_response['demand']['sem'] + ' Mg'"></td>
            <td class="table_row" v-html="sim_response['demand']['conf int'] + ' Mg'"></td>
          </tr>
           <tr>
            <td class="table_row">Telehandler</td>
            <td class="table_row" v-html="sim_response['telehandler rate']['average'] + ' Mg/hr'"></td>
            <td class="table_row" v-html="sim_response['telehandler rate']['stdev'] + ' Mg/hr'"></td>
            <td class="table_row" v-html="sim_response['telehandler rate']['sem'] + ' Mg/hr'"></td>
            <td class="table_row" v-html="sim_response['telehandler rate']['conf int'] + ' Mg/hr'"></td>
          </tr>
          <tr>
            <td class="table_row">Forage Chopper</td>
            <td class="table_row" v-html="sim_response['chopper rate']['average'] + ' Mg/hr'"></td>
            <td class="table_row" v-html="sim_response['chopper rate']['stdev'] + ' Mg/hr'"></td>
            <td class="table_row" v-html="sim_response['chopper rate']['sem'] + ' Mg/hr'"></td>
            <td class="table_row" v-html="sim_response['chopper rate']['conf int'] + ' Mg/hr'"></td>
          </tr>
          <tr>
            <td class="table_row">Press</td>
            <td class="table_row" v-html="sim_response['press rate']['average'] + ' Mg/hr'"></td>
            <td class="table_row" v-html="sim_response['press rate']['stdev'] + ' Mg/hr'"></td>
            <td class="table_row" v-html="sim_response['press rate']['sem'] + ' Mg/hr'"></td>
            <td class="table_row" v-html="sim_response['press rate']['conf int'] + ' Mg/hr'"></td>
          </tr>
          <tr>
            <td class="table_row">Bagger</td>
            <td class="table_row" v-html="sim_response['bagger rate']['average'] + ' Mg/hr'"></td>
            <td class="table_row" v-html="sim_response['bagger rate']['stdev'] + ' Mg/hr'"></td>
            <td class="table_row" v-html="sim_response['bagger rate']['sem'] + ' Mg/hr'"></td>
            <td class="table_row" v-html="sim_response['bagger rate']['conf int'] + ' Mg/hr'"></td>
          </tr>
          <tr>
            <td class="table_row">Module Former</td>
            <td class="table_row" v-html="sim_response['module former rate']['average'] + ' Mg'"></td>
            <td class="table_row" v-html="sim_response['module former rate']['stdev'] + ' Mg'"></td>
            <td class="table_row" v-html="sim_response['module former rate']['sem'] + ' Mg'"></td>
            <td class="table_row" v-html="sim_response['module former rate']['conf int'] + ' Mg'"></td>
          </tr>
          <tr>
            <td class="table_row">Module Hauler</td>
            <td class="table_row" v-html="sim_response['module hauler rate']['average'] + ' Mg'"></td>
            <td class="table_row" v-html="sim_response['module hauler rate']['stdev'] + ' Mg'"></td>
            <td class="table_row" v-html="sim_response['module hauler rate']['sem'] + ' Mg'"></td>
            <td class="table_row" v-html="sim_response['module hauler rate']['conf int'] + ' Mg'"></td>
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
      customForm: false,
      showOptButton: false,
      customModel: {},
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
        "proportion_devoted": 0.03,
        "area_ratio": [1, 10]
        },
        "price": 65,
        "interest_rate": 0.05,
        "insurance_rate": 0.008,
        "tax_rate": 0.01,
        "cost": {
            "equipment": {
            "loadout": [94000, 5, 28200, 0.37, 84700],
            "press": [300000, 5, 120000, 0.1374, 90800],
            "chopper": [22000, 5, 8800, 0, 924000],
            "bagger": [50000, 5, 20000, 0.7, 200000],
            "module_former": [450000, 5, 217234, 1.0319, 80000],
            "module_hauler": [375000, 8, 73530, 0.2766, 362000]
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
      op_response: {},
      sim_response: {
        "demand": {
          "percent": 0, 
          "average": 0, 
          "stdev":0, 
          "sem":0, 
          "conf int":0
        }, 
        "telehandler rate":{
          "average": 0, 
          "stdev": 0, 
          "sem": 0, 
          "conf int": 0
        }, 
        "press rate":{
          "average": 0, 
          "stdev": 0, 
          "sem": 0, 
          "conf int": 0
        }, 
        "chopper rate":{
          "average": 0, 
          "stdev": 0, 
          "sem": 0, 
          "conf int": 0
        }, 
        "bagger rate":{
          "average": 0, 
          "stdev": 0, 
          "sem": 0, 
          "conf int":0
        }, 
        "module former rate": {
          "average": 0, 
          "stdev": 0, 
          "sem":0, 
          "conf int": 0
        }, 
        "module hauler rate":{
          "average": 0, 
          "stdev": 0, 
          "sem": 0, 
          "conf int": 0
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
      var mapInfo = this.$refs.map.submitLocations();
      NProgress.start()

      if (mapInfo == "Refinery Missing") {
        alert("Need Refinery");
      } else {
        this.model.Coord_f = mapInfo.Coord_f;
        this.model.Coord_s = mapInfo.Coord_s;
        this.model.input_format = mapInfo.mode;
        this.model.refinery_location = mapInfo.refinery_location;
        axios
          .post('http://localhost:5000/s-bfls/', this.model)
          .then(response => {
              NProgress.done()
              var r = response.data
              this.op_response = r.op_response;
              this.$refs.csv_download.generateCsv(this.op_response);
			        this.sim_response = r.sim_response;
              this.showSolution = true;
              this.parseApplyRoutes(this.op_response);
              this.$refs.map.show_results(this.op_response["summary"]["cost"]);
          })
      }
    }
  }
}
</script>

<style>

.title {
  grid-area: title;
  text-align: left;
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
  flex-grow: 1;
  justify-content: flex-start;
  flex-wrap: wrap;
}

.requiredParams {
  grid-area: params;
  display: flex;
  flex-grow: 1;
  justify-content: flex-start;
  flex-wrap: wrap;
}

.requiredParams .input {
  margin-right: 1rem;
}

.defaultWidth {
  width: 15rem;
}

.buttons {
  grid-area: buttons
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

.results {
  grid-area: results;
  text-align: left;
}

.table1 {
  grid-area: table1;
  border-collapse: collapse;
  border: 1px solid #0000FF;
  width: 75%;
}

.table_header {
  grid-area: table_header;
  padding-top: 12px;
  padding-bottom: 12px;
  text-align: left;
  background-color: rgb(76, 127, 175);
  color: white;
  text-align: center;
  border: 1px solid #000000;
}

.table_row {
  grid-area: table_row;
  border: 1px solid #0000FF;
  text-align: center;
}
</style>
