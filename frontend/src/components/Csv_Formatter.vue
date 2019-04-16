<template>
<vue-json-to-csv :json-data="op_response_csv"
:labels="{
    col_a: { title: '--' },
    col_b: { title: '--' },
    col_c: { title: '--' },
    col_d: { title: '--' },
    col_e: { title: '--' },
    col_f: { title: '--' },
    col_1: { title: '--' },
    col_2: { title: '--' },
    col_3: { title: '--' },
    col_4: { title: '--' },
    col_5: { title: '--' },
    col_6: { title: '--' },
    col_7: { title: '--' },
    col_8: { title: '--' },
    col_9: { title: '--' },
    col_10: { title: '--' },
    col_11: { title: '--' },
    col_12: { title: '--' },
    col_13: { title: '--' },
    col_14: { title: '--' },
    col_15: { title: '--' },
    col_16: { title: '--' },
    col_17: { title: '--' },
    col_18: { title: '--' },
    col_19: { title: '--' },
    col_20: { title: '--' },
    col_21: { title: '--' },
    col_22: { title: '--' },
    col_23: { title: '--' },
    col_24: { title: '--' },
    col_25: { title: '--' },
    col_26: { title: '--' }
    }">
<button id="optimization_csv_button" hidden="true">
    <b>Download Full Results</b>
  </button>
</vue-json-to-csv>
</template>

<script>
import VueJsonToCsv from 'vue-json-to-csv'

export default {
    components: {
        'vueJsonToCsv' : VueJsonToCsv
    },
    data() {
        return {
           op_response_csv: [], 
        }
    },
    methods: {
        generateCsv(data, refinery_location) {
            console.log(data);
            
            var csv_index = 0;

            //PARAMS
            var params = data.params;
            var configuration = params.Configuration;
            var coord_farms = params.Coord_farms;
            var coord_ssls = params.Coord_ssls;
            var coord_ref = null;
            var seed = params.Seed;
            var sysnum = params.Sysnum;
            var penalty_per_Mg = params.c_pen;
            var demand = params.demand;
            var farm_holding_cost = params.farm_holding_cost;
            var farm_ssl_trans_cost = params.farm_ssl_trans_cost;
            var fixed_cost_ssl = params.fixed_cost_ssls;
            var harvested = params.harvested;
            var operating_cost = params.operating_cost;
            var operating_cost_jit = params.operating_cost_jit;
            var ssl_configurations = params.SSL_configuration;
            var ssl_holding_cost = params.ssl_holding_cost;
            var ssl_refinery_trans_cost = params.ssl_refinery_trans_cost;
            var ssl_refinery_trans_cost_jit = params.ssl_refinery_jit_trans_cost;
            var upperbound_equip_proc_rate = params.upperbound_equip_proc_rate;
            var upperbound_equip_proc_rate_jit = params.upperbound_equip_proc_rate_jit;
            var upperbound_inventory = params.upperbound_inventory;

            //sysnum, configuration, seed, refinery coords chart
            this.op_response_csv[csv_index++] = {col_a: "sysnum",
                                                 col_b: "configuration",
                                                 col_c: "seed",
                                                 col_d: "refinery lat",
                                                 col_e: "refinery lng"};
            this.op_response_csv[csv_index++] = {col_a: sysnum,
                                                 col_b: configuration,
                                                 col_c: (seed == null) ? "undefined" : seed,
                                                 col_d: refinery_location[0],
                                                 col_e: refinery_location[1]};


            this.op_response_csv[csv_index++] = {};
            this.op_response_csv[csv_index++] = {};



            //penalty, operating cost (+ jit), farm_holding_cost, ssl_holding_cost chart
            this.op_response_csv[csv_index++] = {col_a: "penalty",
                                                 col_b: "operating cost",
                                                 col_c: "operating cost jit",
                                                 col_d: "farm holding cost",
                                                 col_e: "ssl holding cost"};
            this.op_response_csv[csv_index++] = {col_a: penalty_per_Mg,
                                                 col_b: operating_cost,
                                                 col_c: operating_cost_jit,
                                                 col_d: farm_holding_cost,
                                                 col_e: ssl_holding_cost};


            this.op_response_csv[csv_index++] = {};
            this.op_response_csv[csv_index++] = {};



            //harvested + demand
            this.op_response_csv[csv_index++] = {col_1: "week 1",
                                                 col_2: "week 2",
                                                 col_3: "week 3",
                                                 col_4: "week 4",
                                                 col_5: "week 5",
                                                 col_6: "week 6",
                                                 col_7: "week 7",
                                                 col_8: "week 8",
                                                 col_9: "week 9",
                                                 col_10: "week 10",
                                                 col_11: "week 11",
                                                 col_12: "week 12",
                                                 col_13: "week 13",
                                                 col_14: "week 14",
                                                 col_15: "week 15",
                                                 col_16: "week 16",
                                                 col_17: "week 17",
                                                 col_18: "week 18",
                                                 col_19: "week 19",
                                                 col_20: "week 20",
                                                 col_21: "week 21",
                                                 col_22: "week 22",
                                                 col_23: "week 23",
                                                 col_24: "week 24",
                                                 col_25: "week 25",
                                                 col_26: "week 26"};

            var n;
            this.op_response_csv[csv_index] = {};
            for (n = 0; n < demand.length; n++) {
               this.op_response_csv[csv_index]["col_" + (n + 1)] = demand[n]; 
            }
            this.op_response_csv[csv_index++]["col_f"] = "demand";

            for (n = 0; n < harvested[0].length; n++) {
                this.op_response_csv[csv_index] = {};
                var q;
                for (q = 0; q < harvested.length; q++) {
                    this.op_response_csv[csv_index]["col_" + (q + 1)] = harvested[q][n];
                }
                this.op_response_csv[csv_index++]["col_f"] = "farm " + n;
            }


            //SOLUTION
            var solution = data.solution;
            var solution_index;

            var solution_parts; 
            var ssl_configs = [];
            var farm_ssl = true;
            var ssl_ref = true;
            var farm_index = 0;
            var ssl_index = 0;
            for (solution_index = 0; solution_index < solution.length; solution_index++) { 
                solution_parts = solution[solution_index][0].split("[");
                if(solution_parts[0] == "ssl_configuration_selection") {
                    var inner_parts = solution_parts[1].split(",");
                    var ssl = inner_parts[0];
                    var config = inner_parts[1].split("]")[0];

                    ssl_configs[ssl_configs.length] = [ssl, config];
                } else if (solution_parts[0] == "farm_to_ssl") {
                    if (farm_ssl) {
                        this.op_response_csv[csv_index++] = {};
                        this.op_response_csv[csv_index++] = {};

                        this.op_response_csv[csv_index++] = {col_a: "farm num",
                                                             col_b: "farm lat",
                                                             col_c: "farm lng",
                                                             col_d: "ssl num",
                                                             col_e: "farm to ssl cost",
                                                             col_1: "week 1",
                                                             col_2: "week 2",
                                                             col_3: "week 3",
                                                             col_4: "week 4",
                                                             col_5: "week 5",
                                                             col_6: "week 6",
                                                             col_7: "week 7",
                                                             col_8: "week 8",
                                                             col_9: "week 9",
                                                             col_10: "week 10",
                                                             col_11: "week 11",
                                                             col_12: "week 12",
                                                             col_13: "week 13",
                                                             col_14: "week 14",
                                                             col_15: "week 15",
                                                             col_16: "week 16",
                                                             col_17: "week 17",
                                                             col_18: "week 18",
                                                             col_19: "week 19",
                                                             col_20: "week 20",
                                                             col_21: "week 21",
                                                             col_22: "week 22",
                                                             col_23: "week 23",
                                                             col_24: "week 24",
                                                             col_25: "week 25",
                                                             col_26: "week 26"};
                        farm_ssl = false;
                        farm_index = csv_index;
                    }

                    var inner_parts = solution_parts[1].split(",");
                    var farm = parseInt(inner_parts[0]);
                    var ssl = parseInt(inner_parts[1].split("]")[0]);
                    this.op_response_csv[csv_index++] = {col_a: farm,
                                                         col_b: coord_farms[farm][0],
                                                         col_c: coord_farms[farm][1],
                                                         col_d: ssl,
                                                         col_e: farm_ssl_trans_cost[farm][ssl]};


                } else if (solution_parts[0] == "shipped_farm_ssl") {

                    var inner_parts = solution_parts[1].split(",");
                    var week = parseInt(inner_parts[0]);
                    var farm = parseInt(inner_parts[1]);
                    this.op_response_csv[farm_index + farm]["col_" + week] =
                        solution[solution_index][1];

                } else if (solution_parts[0] == "shipped_ssl_refinery") {
                    if (ssl_ref) {
                        this.op_response_csv[csv_index++] = {};
                        this.op_response_csv[csv_index++] = {};

                        this.op_response_csv[csv_index++] = {col_a: "ssl num",
                                                             col_b: "ssl lat",
                                                             col_c: "ssl lng",
                                                             col_d: "ssl to ref cost (jit)",
                                                             col_e: "cost to build ssl",
                                                             col_f: "ssl configuration number",
                                                             col_1: "week 1",
                                                             col_2: "week 2",
                                                             col_3: "week 3",
                                                             col_4: "week 4",
                                                             col_5: "week 5",
                                                             col_6: "week 6",
                                                             col_7: "week 7",
                                                             col_8: "week 8",
                                                             col_9: "week 9",
                                                             col_10: "week 10",
                                                             col_11: "week 11",
                                                             col_12: "week 12",
                                                             col_13: "week 13",
                                                             col_14: "week 14",
                                                             col_15: "week 15",
                                                             col_16: "week 16",
                                                             col_17: "week 17",
                                                             col_18: "week 18",
                                                             col_19: "week 19",
                                                             col_20: "week 20",
                                                             col_21: "week 21",
                                                             col_22: "week 22",
                                                             col_23: "week 23",
                                                             col_24: "week 24",
                                                             col_25: "week 25",
                                                             col_26: "week 26"};
                        ssl_ref = false;
                        ssl_index = csv_index;

                        var n;
                        for (n = 0; n < ssl_configs.length; n++) {
                            this.op_response_csv[csv_index++] = {col_a: ssl_configs[n][0],
                                 col_b: coord_ssls[n][0],
                                 col_c: coord_ssls[n][1],
                                 col_d: ssl_refinery_trans_cost[n] + " (" + ssl_refinery_trans_cost_jit[n] + ")",
                                 col_e: fixed_cost_ssl[ssl_configs[n][0]][ssl_configs[n][1]], 
                                 col_f: ssl_configs[n][1]};
                        }
                    }

                    var inner_parts = solution_parts[1].split(",");
                    var week = parseInt(inner_parts[0]);
                    var ssl = parseInt(inner_parts[1].split("]")[0]);
                    this.op_response_csv[ssl_index + ssl]["col_" + week] =
                        solution[solution_index][1];


                }
            }
            

            this.op_response_csv[csv_index++] = {};
            this.op_response_csv[csv_index++] = {};


            //upperbounds
 
            this.op_response_csv[csv_index++] = {col_a: "ssl config num",
                                                 col_b: "max storage",
                                                 col_c: "max equip proc rate (jit)"};
            var saved_configs = [];
            for (n = 0; n < ssl_configs.length; n++) {
                var ind_ssl = ssl_configs[n];
                if (!saved_configs.includes(ind_ssl[1])) {
                    saved_configs[saved_configs.length] = ind_ssl[1];
                    this.op_response_csv[csv_index++] = {col_a: ind_ssl[1],
                        col_b: upperbound_inventory[ind_ssl[1]],
                        col_c: upperbound_equip_proc_rate[ind_ssl[1]] +
                        " (" + upperbound_equip_proc_rate_jit[ind_ssl[1]] + ")"};
                }
            }

            this.op_response_csv[csv_index++] = {};
            this.op_response_csv[csv_index++] = {};



            
            //SUMMARY
            var summary = data.summary;
            var cost = summary.cost;
            var per_dry_Mg = summary.per_dry_Mg;

            //cost (total and per Mg)

            this.op_response_csv[csv_index++] = {col_a: "part",
                                                 col_b: "cost",
                                                 col_c: "cost per dry mg"};
            this.op_response_csv[csv_index++] = {col_a: "farm holding cost",
                                                 col_b: cost.farm_inventory,
                                                 col_c: per_dry_Mg.farm_inventory};
            this.op_response_csv[csv_index++] = {col_a: "ssl holding",
                                                 col_b: cost.ssl_inventory,
                                                 col_c: per_dry_Mg.ssl_inventory};
            this.op_response_csv[csv_index++] = {col_a: "location ownership",
                                                 col_b: cost.loc_own,
                                                 col_c: per_dry_Mg.loc_own};
            this.op_response_csv[csv_index++] = {col_a: "operation",
                                                 col_b: cost.operation,
                                                 col_c: per_dry_Mg.operation};
            this.op_response_csv[csv_index++] = {col_a: "farm to ssl trans",
                                                 col_b: cost.tran_farms_ssl,
                                                 col_c: per_dry_Mg.tran_farms_ssl};
            this.op_response_csv[csv_index++] = {col_a: "ssl to ref trans",
                                                 col_b: cost.tran_ssl_refinery,
                                                 col_c: per_dry_Mg.tran_ssl_refinery};
            this.op_response_csv[csv_index++] = {col_a: "total (upper bound)",
                                                 col_b: cost.total_ub,
                                                 col_c: per_dry_Mg.total_ub};
            


            this.op_response_csv[csv_index++] = {};
            this.op_response_csv[csv_index++] = {};

            this.fill_undefined();
            console.log(this.op_response_csv);
            document.getElementById('optimization_csv_button').hidden = false;
        },
        fill_undefined() {
            var k;
            for (k = 0; k < this.op_response_csv.length; k++) {
                if (this.op_response_csv[k]["col_a"] == null)
                    this.op_response_csv[k]["col_a"] = "";
                if (this.op_response_csv[k]["col_b"] == null)
                    this.op_response_csv[k]["col_b"] = "";
                if (this.op_response_csv[k]["col_c"] == null)
                    this.op_response_csv[k]["col_c"] = "";
                if (this.op_response_csv[k]["col_d"] == null)
                    this.op_response_csv[k]["col_d"] = "";
                if (this.op_response_csv[k]["col_e"] == null)
                    this.op_response_csv[k]["col_e"] = "";
                if (this.op_response_csv[k]["col_f"] == null)
                    this.op_response_csv[k]["col_f"] = "";
                var m;
                for ( m = 1; m <= 26; m++) {
                    if (this.op_response_csv[k]["col_" + m] == null)
                        this.op_response_csv[k]["col_" + m] = "";
                }
            }
        }
    }
};
</script>







