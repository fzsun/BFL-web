<template>
<div class="section">
    <h1 class="title">Sorghum BFLS</h1>
    <div id="s_bfl" class="container">
        <div class="is-size-4">
            A tool for decision makers to determine the most cost effective
            way to produce and transport sorghum for use in biofuels. The tool itself
            is an optimization algorithm and simulization that work in tandem to find
            and test an optimial solution. To learn more about the algorithm
            <a>see here.</a>
        </div>
        <br>
        <div class="panel-body">
            <form>
                <vue-form-generator :schema="schema" :model="model" :options="formOptions">
                </vue-form-generator>
            </form>
            <button v-on:click="optimize">Optimize</button>
        </div>
        <div class="map_div">
            <Map ref="map"> </Map>
        </div>
    </div>
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
        "input_format": "paper",
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
      schema: {
        fields: [{
          type: "input",
          inputType: "text",
          label: "input_format",
          model: "input_format",
        },  {
          type: "input",
          inputType: "text",
          label: "moisture",
          model: "moisture",
        }, {
          type: "input",
          inputType: "text",
          label: "ssl_sizes",
          model: "ssl_sizes",
        }, {
          type: "input",
          inputType: "text",
          label: "field.dry_yield",
          model: "field.dry_yield",
        }, {
          type: "input",
          inputType: "text",
          label: "field.radius",
          model: "field.radius",
        },{
          type: "input",
          inputType: "text",
          label: "field - proportion devoted",
          model: "field.proportion_devoted",
        },{
          type: "input",
          inputType: "text",
          label: "price",
          model: "price",
        },{
          type: "input",
          inputType: "text",
          label: "interest rate",
          model: "interest_rate",
        },{
          type: "input",
          inputType: "text",
          label: "tax rate",
          model: "tax_rate",
        },{
          type: "input",
          inputType: "text",
          label: "cost.equipment.loadout",
          model: "cost.equipment.loadout",
        },{
          type: "input",
          inputType: "text",
          label: "cost.equipment.press",
          model: "cost.equipment.press",
        },{
          type: "input",
          inputType: "text",
          label: "cost.equipment.chopper",
          model: "cost.equipment.chopper",
        },{
          type: "input",
          inputType: "text",
          label: "cost.equipment.bagger",
          model: "cost.equipment.bagger",
        },{
          type: "input",
          inputType: "text",
          label: "cost.equipment.module_former",
          model: "cost.equipment.module_former",
        },{
          type: "input",
          inputType: "text",
          label: "cost.equipment.module_hauler",
          model: "cost.equipment.module_hauler",
        },{
          type: "input",
          inputType: "text",
          label: "cost.bunker_annual_own",
          model: "cost.bunker_annual_own",
        },{
          type: "input",
          inputType: "text",
          label: "cost.ssl_annual_own",
          model: "cost.ssl_annual_own",
        },{
          type: "input",
          inputType: "text",
          label: "cost.base_infield",
          model: "cost.base_infield",
        },{
          type: "input",
          inputType: "text",
          label: "cost.base_highway",
          model: "cost.base_highway",
        },{
          type: "input",
          inputType: "text",
          label: "cost.transport_coef.compressed",
          model: "cost.transport_coef.compressed",
        },{
          type: "input",
          inputType: "text",
          label: "cost.transport_coef.whole_stalk",
          model: "cost.transport_coef.whole_stalk",
        },{
          type: "input",
          inputType: "text",
          label: "cost.transport_coef.in_module",
          model: "cost.transport_coef.in_module",
        },{
          type: "input",
          inputType: "text",
          label: "degrade.whole_stalk",
          model: "degrade.whole_stalk",
        },{
          type: "input",
          inputType: "text",
          label: "degrade.chopped",
          model: "degrade.chopped",
        },{
          type: "input",
          inputType: "text",
          label: "degrade.in_bunker",
          model: "degrade.in_bunker",
        },{
          type: "input",
          inputType: "text",
          label: "degrade.in_bag",
          model: "degrade.in_bag",
        },{
          type: "select",
          label: "configurations",
          model: "configurations",
        }
        ]
      },

      formOptions: {
        validateAfterLoad: true,
        validateAfterChanged: true
      }
    };
  },
  methods: {
    optimize(event) {
      var mapInfo = this.$refs.map.submitLocations();

      if (mapInfo == "Refinery Missing") {
        alert("Need Refinery");
      } else {
        this.model.Coord_f = mapInfo.Coord_f;
        this.model.Coord_s = mapInfo.Coord_s;
        this.model.mode = mapInfo.mode;
        this.model.refinery_location = mapInfo.refinery_location;
        axios
          .post('http://localhost:5000/s-bfls/', this.model)
          .then(response => {
              this.response = response.data;
              console.log("Optimization Results: ");
              console.log(this.response);
          })
      }
    }
  }
}
</script>

<style>
fieldset {
  padding: 1rem;
}
</style>
