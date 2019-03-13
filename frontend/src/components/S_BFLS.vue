<template>
<div class="section wrap">
    <h1 class="title">Sorghum - Logistics Support</h1>
    <Map class="map" v-model="mapInfo" ref="map"></Map>
    <div class="paramDescription title is-4">Optimization Parameters</div>
    <div class="params">
      <div class="field">
        <label class="label">Moisture</label>
        <div class="control">
          <input class="input" type="text" v-model="model.moisture">
        </div>
      </div>
      <div class="field">
        <label class="label">Demand (Mg)</label>
        <div class="control">
          <input class="input" type="text" v-model="model.demand">
        </div>
      </div>
      <div class="field">
        <label class="label">Horizon (weeks)</label>
        <div class="control">
          <input class="input" type="text" v-model="model.horizon">
        </div>
      </div>
      <!-- <div class="field">
        <label class="label">Number Farms</label>
        <div class="control">
          <input class="input" type="text" v-model="model.num_fields">
        </div>
      </div>
      <div class="field">
        <label class="label">Number SSL</label>
        <div class="control">
          <input class="input" type="text" v-model="model.demand">
        </div>
      </div> -->
      <div class="field">
        <label class="label">SSL Sizes [small, medium, large]</label>
        <div class="control">
          <input class="input" type="text" v-model="model.ssl_sizes">
        </div>
      </div>
      <div class="field">
        <label class="label">Harvest Progress</label>
        <div class="control">
          <input class="input" type="text" v-model="model.harvest_progress">
        </div>
      </div>
      <div class="field">
        <label class="label">Field - Dry Yield</label>
        <div class="control">
          <input class="input" type="text" v-model="model.field.dry_yield">
        </div>
      </div>
      <div class="field">
        <label class="label">Field - Radius</label>
        <div class="control">
          <input class="input" type="text" v-model="model.field.radius">
        </div>
      </div>
      <div class="field">
        <label class="label">Field - Proportion Devoted</label>
        <div class="control">
          <input class="input" type="text" v-model="model.field.proportion_devoted">
        </div>
      </div>
      <div class="field">
        <label class="label">Field - Area Ratio</label>
        <div class="control">
          <input class="input" type="text" v-model="model.field.area_ratio">
        </div>
      </div>
      <div class="field">
        <label class="label">Price per Mg</label>
        <div class="control">
          <input class="input" type="text" v-model="model.price">
        </div>
      </div>
      <div class="field">
        <label class="label">Interest Rate</label>
        <div class="control">
          <input class="input" type="text" v-model="model.interest_rate">
        </div>
      </div>
      <div class="field">
        <label class="label">Insurance Rate</label>
        <div class="control">
          <input class="input" type="text" v-model="model.insurance_rate">
        </div>
      </div>
      <div class="field">
        <label class="label">Tax Rate</label>
        <div class="control">
          <input class="input" type="text" v-model="model.tax_rate">
        </div>
      </div>
      <div class="field">
        <label class="label">Equipment Loadout Cost</label>
        <div class="control">
          <input class="input" type="text" v-model="model.cost.equipment.loadout">
        </div>
      </div>
      <div class="field">
        <label class="label">Equipment Press Cost</label>
        <div class="control">
          <input class="input" type="text" v-model="model.cost.equipment.press">
        </div>
      </div>
      <div class="field">
        <label class="label">Equipment Chopper Cost</label>
        <div class="control">
          <input class="input" type="text" v-model="model.cost.equipment.chopper">
        </div>
      </div>
      <div class="field">
        <label class="label">Equipment Bagger Cost</label>
        <div class="control">
          <input class="input" type="text" v-model="model.cost.equipment.bagger">
        </div>
      </div>
      <div class="field">
        <label class="label">Equipment Module Former Cost</label>
        <div class="control">
          <input class="input" type="text" v-model="model.cost.equipment.module_former">
        </div>
      </div>
      <div class="field">
        <label class="label">Equipment Module Hauler Cost</label>
        <div class="control">
          <input class="input" type="text" v-model="model.cost.equipment.module_hauler">
        </div>
      </div>
      <div class="field">
        <label class="label">Bunker Annual Ownership Cost</label>
        <div class="control">
          <input class="input" type="text" v-model="model.cost.bunker_annual_own">
        </div>
      </div>
      <div class="field">
        <label class="label">SSL Annual Ownership Cost</label>
        <div class="control">
          <input class="input" type="text" v-model="model.cost.ssl_annual_own">
        </div>
      </div>
      <div class="field">
        <label class="label">Base Infield Cost</label>
        <div class="control">
          <input class="input" type="text" v-model="model.cost.base_infield">
        </div>
      </div>
      <div class="field">
        <label class="label">Base Highway Cost</label>
        <div class="control">
          <input class="input" type="text" v-model="model.cost.base_highway">
        </div>
      </div>
      <div class="field">
        <label class="label">Transportation Coefficient - Compressed</label>
        <div class="control">
          <input class="input" type="text" v-model="model.cost.transport_coef.compressed">
        </div>
      </div>
      <div class="field">
        <label class="label">Transportation Coefficient - Whole Stalk</label>
        <div class="control">
          <input class="input" type="text" v-model="model.cost.transport_coef.whole_stalk">
        </div>
      </div>
      <div class="field">
        <label class="label">Transportation Coefficient - In Module</label>
        <div class="control">
          <input class="input" type="text" v-model="model.cost.transport_coef.in_module">
        </div>
      </div>
      <div class="field">
        <label class="label">Whole Stalk Degrade</label>
        <div class="control">
          <input class="input" type="text" v-model="model.degrade.whole_stalk">
        </div>
      </div>
      <div class="field">
        <label class="label">Chopped Degrade</label>
        <div class="control">
          <input class="input" type="text" v-model="model.degrade.chopped">
        </div>
      </div>
      <div class="field">
        <label class="label">In Bunker Degrade</label>
        <div class="control">
          <input class="input" type="text" v-model="model.degrade.in_bunker">
        </div>
      </div>
      <div class="field">
        <label class="label">In Bag Degrade</label>
        <div class="control">
          <input class="input" type="text" v-model="model.degrade.in_bag">
        </div>
      </div>
    </div> 
    <button 
      class="button optimize is-primary" 
      v-on:click="optimize"
    >
      Optimize
    </button>
</div>
</template>

<script>
/* eslint-disable */
import { validators, component as VueFormGenerator } from 'vue-form-generator'
import axios from 'axios'
import Map from './Map'

export default {
  components: {
      VueFormGenerator,
      'Map' : Map
  },
  data() {
    return {
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
      response: [],
      mapInfo: {},
    };
  },
  methods: {
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
              this.parseApplyRoutes(this.response);
          })
      }
    }
  }
}
</script>

<style>
/* fieldset {
  padding: 1rem;
} */

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

.wrap {
    display: grid;
    margin: 0;
    grid-template-columns: 1fr;
    grid-template-rows: auto;
    grid-template-areas: "title" "map" "paramDescription" "params" "optimize";
}

.params {
  display: flex;
  justify-content: space-around;
  flex-wrap: wrap;
}

.params .input {
  width: 20rem;
}

.optimize {
  grid-area: optimize;
  width: 110px;
  float: right;
}
</style>
