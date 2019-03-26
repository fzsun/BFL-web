<template>
<div class="section wrap">
    <h1 class="title">Sorghum - Logistics Support</h1>
    <Map class="map" v-model="mapInfo" ref="map"></Map>
    <div class="paramDescription">
      <div class="title is-size-4">Optimization Parameters</div>
      <button 
        class="button is-primary floatLeft"
        v-on:click="showOptimize()"
      >
        Accept Default Configuration
      </button>
      <button 
        class="button is-link floatLeft"
        v-on:click="customFormTrue()"
      >
        Customize Optimization Parameters
      </button>
      <button 
        class="button is-danger floatLeft"
        v-on:click="customFormFalse()"
        v-if="customForm"
      >
        Cancel
      </button>
    </div>
    <div class="params">
      <OptimizationForm 
        v-if="customForm"
        ref = "opForm"
        v-on:formChange='model = $event'
        v-bind:model='model'
      ></OptimizationForm>
    </div> 
    <button 
      class="button optimize is-warning" 
      v-on:click="optimize"
      v-if="showOptButton"
    >
      Optimize
    </button>
</div>
</template>

<script>
import { validators, component as VueFormGenerator } from 'vue-form-generator'
import axios from 'axios'
import Map from './Map'
import OptimizationForm from './OptimizationForm'

export default {
  components: {
      VueFormGenerator,
      'Map' : Map,
      'OptimizationForm' : OptimizationForm,
  },
  data() {
    return {
      response: [],
      mapInfo: {},
      customForm: false,
      showOptButton: false,
      model: {
        "moisture": 0.7,
        "demand": 200000,
        "horizon": 26,
        "num_fields": 120,
        "num_ssls": 60,
        "ssl_sizes": [2500, 5000, 10000],
        "harvest_progress": [5, 5, 6, 7, 10, 11, 12, 11, 9, 8, 6, 5, 5],
        "field": {
        "dry_yield": 21,
        "radius": 32,
        "proportion_devoted": 0.03,
        "area_ratio": [1, 10]},
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
    };
  },
  methods: {
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
        // routes.append(route);
      }
    },
    optimize(event) {
      var mapInfo = this.$refs.map.submitLocations();

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
              this.response = response.data;
              console.log("Allocation Farm: ", response.data.summary.allocation_from_farm);
              console.log("Allocation ssl: ", response.data.summary.allocation_to_ssl);
              this.parseApplyRoutes(this.response);
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
}

.wrap {
    display: grid;
    margin: 0;
    grid-template-columns: 1fr;
    grid-template-rows: auto;
    grid-template-areas: "title" "map" "paramDescription" "params" "optimize";
}

.optimize {
  grid-area: optimize;
  width: 110px;
  float: right;
}
</style>
