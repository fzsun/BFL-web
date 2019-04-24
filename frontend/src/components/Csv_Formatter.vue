<template>
<vue-json-to-csv :json-data="op_response_csv"
csv-title="s_bfl_optimization"
:labels="{
   0: { title: '' },
   1: { title: '' },
   2: { title: '' },
   3: { title: '' },
   4: { title: '' },
   5: { title: '' },
   6: { title: '' },
   7: { title: '' },
   8: { title: '' },
   9: { title: '' },
   10: { title: '' },
   11: { title: '' },
   12: { title: '' },
   13: { title: '' },
   14: { title: '' },
   15: { title: '' },
   16: { title: '' },
   17: { title: '' },
   18: { title: '' },
   19: { title: '' },
   20: { title: '' },
   21: { title: '' },
   22: { title: '' },
   23: { title: '' },
   24: { title: '' },
   25: { title: '' },
   26: { title: '' },
   27: { title: '' },
   28: { title: '' },
   29: { title: '' },
   30: { title: '' },
   31: { title: '' }
    }">
<button id="optimization_csv_button" class="button is-success" hidden="true">
    Download Full Results
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
            this.op_response_csv[csv_index++] = ["sysnum",
                                                 "configuration",
                                                 "seed",
                                                 "refinery lat",
                                                 "refinery lng"];
            this.op_response_csv[csv_index++] = [sysnum,
                                                 configuration,
                                                 (seed == null) ? "undefined" : seed,
                                                 refinery_location[0],
                                                 refinery_location[1]];


            this.op_response_csv[csv_index++] = [];
            this.op_response_csv[csv_index++] = [];



            //penalty, operating cost, farm_holding_cost, ssl_holding_cost chart
            this.op_response_csv[csv_index++] = ["penalty ($/Mg)",
                                                 "operating cost ($/Mg)",
                                                 "farm holding cost ($/Mg/week)",
                                                 "ssl holding cost ($/Mg/week)"];
            this.op_response_csv[csv_index++] = [penalty_per_Mg,
                                                 operating_cost,
                                                 farm_holding_cost,
                                                 ssl_holding_cost];


            this.op_response_csv[csv_index++] = [];
            this.op_response_csv[csv_index++] = [];



            //harvested + demand
            this.op_response_csv[csv_index++] = ["",
                                                 "week 0",
                                                 "week 1",
                                                 "week 2",
                                                 "week 3",
                                                 "week 4",
                                                 "week 5",
                                                 "week 6",
                                                 "week 7",
                                                 "week 8",
                                                 "week 9",
                                                 "week 10",
                                                 "week 11",
                                                 "week 12",
                                                 "week 13",
                                                 "week 14",
                                                 "week 15",
                                                 "week 16",
                                                 "week 17",
                                                 "week 18",
                                                 "week 19",
                                                 "week 20",
                                                 "week 21",
                                                 "week 22",
                                                 "week 23",
                                                 "week 24",
                                                 "week 25",
                                                 "week 26"];

            var total_index = csv_index;
            var n;

            for (n = 0; n < harvested[0].length; n++) {
                this.op_response_csv[csv_index] = ["farm " + n];
                var q;
                for (q = 0; q < harvested.length; q++) {
                    this.op_response_csv[csv_index][q + 1] = harvested[q][n];
                }
                csv_index++;
            }

            this.op_response_csv[csv_index] = ["week total: "];
            var m;
            for (m = 1; m <= 27; m++) {
                var p;
                var total = 0;
                for (p = total_index; p < csv_index; p++) {
                    var biomass = this.op_response_csv[p][m];
                    total += (biomass == null) ? 0 : parseInt(biomass);
                }
                this.op_response_csv[csv_index][m] = total;
            }
            csv_index++;


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

                    ssl_configs[ssl_configs.length] = [ssl, config, ssl_configs.length];
                } else if (solution_parts[0] == "farm_to_ssl") {
                    if (farm_ssl) {
                        this.op_response_csv[csv_index++] = [];
                        this.op_response_csv[csv_index++] = [];

                        this.op_response_csv[csv_index++] = ["farm num",
                                                             "farm lat",
                                                             "farm lng",
                                                             "ssl num",
                                                             "farm to ssl cost ($/Mg)",
                                                             "week 1 (Mg)",
                                                             "week 2",
                                                             "week 3",
                                                             "week 4",
                                                             "week 5",
                                                             "week 6",
                                                             "week 7",
                                                             "week 8",
                                                             "week 9",
                                                             "week 10",
                                                             "week 11",
                                                             "week 12",
                                                             "week 13",
                                                             "week 14",
                                                             "week 15",
                                                             "week 16",
                                                             "week 17",
                                                             "week 18",
                                                             "week 19",
                                                             "week 20",
                                                             "week 21",
                                                             "week 22",
                                                             "week 23",
                                                             "week 24",
                                                             "week 25",
                                                             "week 26"];
                        farm_ssl = false;
                        farm_index = csv_index;
                    }

                    var inner_parts = solution_parts[1].split(",");
                    var farm = parseInt(inner_parts[0]);
                    var ssl = parseInt(inner_parts[1].split("]")[0]);
                    this.op_response_csv[csv_index++] = [farm,
                                                         coord_farms[farm][0],
                                                         coord_farms[farm][1],
                                                         ssl,
                                                         farm_ssl_trans_cost[farm][ssl]];


                } else if (solution_parts[0] == "shipped_farm_ssl") {

                    var inner_parts = solution_parts[1].split(",");
                    var week = parseInt(inner_parts[0]);
                    var farm = parseInt(inner_parts[1]);
                    this.op_response_csv[farm_index + farm][week + 4] =
                        solution[solution_index][1];

                } else if (solution_parts[0] == "shipped_ssl_refinery") {
                    if (ssl_ref) {
                        this.op_response_csv[csv_index++] = [];
                        this.op_response_csv[csv_index++] = [];

                        this.op_response_csv[csv_index++] = ["ssl num",
                                                             "ssl lat",
                                                             "ssl lng",
                                                             "ssl to ref cost ($/Mg)",
                                                             "cost to build ssl ($)",
                                                             "ssl type",
                                                             "week 1 (Mg)",
                                                             "week 2",
                                                             "week 3",
                                                             "week 4",
                                                             "week 5",
                                                             "week 6",
                                                             "week 7",
                                                             "week 8",
                                                             "week 9",
                                                             "week 10",
                                                             "week 11",
                                                             "week 12",
                                                             "week 13",
                                                             "week 14",
                                                             "week 15",
                                                             "week 16",
                                                             "week 17",
                                                             "week 18",
                                                             "week 19",
                                                             "week 20",
                                                             "week 21",
                                                             "week 22",
                                                             "week 23",
                                                             "week 24",
                                                             "week 25",
                                                             "week 26"];
                        ssl_ref = false;
                        ssl_index = csv_index;

                        var n;
                        for (n = 0; n < ssl_configs.length; n++) {
                            this.op_response_csv[csv_index++] = [ssl_configs[n][0],
                                 coord_ssls[n][0],
                                 coord_ssls[n][1],
                                 ssl_refinery_trans_cost[n],
                                 fixed_cost_ssl[ssl_configs[n][0]][ssl_configs[n][1]], 
                                 ssl_configs[n][1]];
                        }
                    }
                    var inner_parts = solution_parts[1].split(",");
                    var week = parseInt(inner_parts[0]);
                    var ssl = parseInt(inner_parts[1].split("]")[0]);
                    var m;
                    for (m = 0; m < ssl_configs.length; m++) {
                        if (ssl_configs[m][0] == ssl) { ssl = ssl_configs[m][2]; break; }
                    }

                    this.op_response_csv[ssl_index + ssl][week + 5] =
                        solution[solution_index][1];
                }
            }
            
            this.op_response_csv[csv_index] = ["","","","","","demand: "];
            for (n = 1; n < demand.length; n++) {
               this.op_response_csv[csv_index][n + 5] = demand[n]; 
            }
            csv_index++;

            this.op_response_csv[csv_index++] = [];
            this.op_response_csv[csv_index++] = [];


            //upperbounds
 
            this.op_response_csv[csv_index++] = ["ssl type",
                                                 "max storage (Mg)",
                                                 "max equip proc rate ($/Mg)"];
            var saved_configs = [];
            for (n = 0; n < ssl_configs.length; n++) {
                var ind_ssl = ssl_configs[n];
                if (!saved_configs.includes(ind_ssl[1])) {
                    saved_configs[saved_configs.length] = ind_ssl[1];
                    this.op_response_csv[csv_index++] = [ind_ssl[1],
                        upperbound_inventory[ind_ssl[1]],
                        upperbound_equip_proc_rate[ind_ssl[1]]];
                }
            }

            this.op_response_csv[csv_index++] = [];
            this.op_response_csv[csv_index++] = [];



            
            //SUMMARY
            var summary = data.summary;
            var cost = summary.cost;
            var per_dry_Mg = summary.per_dry_Mg;

            //cost (total and per Mg)

            this.op_response_csv[csv_index++] = ["cost component",
                                                 "cost ($)",
                                                 "cost ($/Mg)"];
            this.op_response_csv[csv_index++] = ["farm holding cost",
                                                 cost.farm_inventory,
                                                 per_dry_Mg.farm_inventory];
            this.op_response_csv[csv_index++] = ["ssl holding",
                                                 cost.ssl_inventory,
                                                 per_dry_Mg.ssl_inventory];
            this.op_response_csv[csv_index++] = ["location ownership",
                                                 cost.loc_own,
                                                 per_dry_Mg.loc_own];
            this.op_response_csv[csv_index++] = ["operation",
                                                 cost.operation,
                                                 per_dry_Mg.operation];
            this.op_response_csv[csv_index++] = ["farm to ssl trans",
                                                 cost.tran_farms_ssl,
                                                 per_dry_Mg.tran_farms_ssl];
            this.op_response_csv[csv_index++] = ["ssl to ref trans",
                                                 cost.tran_ssl_refinery,
                                                 per_dry_Mg.tran_ssl_refinery];
            this.op_response_csv[csv_index++] = ["total (upper bound)",
                                                 cost.total_ub,
                                                 per_dry_Mg.total_ub];
            this.op_response_csv[csv_index++] = [];
            var other = summary.others;
            this.op_response_csv[csv_index++] = ["gap", other.gap];            


            this.op_response_csv[csv_index++] = [];
            this.op_response_csv[csv_index++] = [];

            this.fill_undefined();
            document.getElementById('optimization_csv_button').hidden = false;
        },
        fill_undefined() {
            var k;
            for (k = 0; k < this.op_response_csv.length; k++) {
                var m;
                for (m = 0; m < 32; m++) {
                    if (this.op_response_csv[k][m] == null)
                        this.op_response_csv[k][m] = "";
                }
                var obj = {};
                for (m = 0; m < 32; m++) {
                    obj[m] = this.op_response_csv[k][m];
                }
                this.op_response_csv[k] = obj;

            }
        }
    }
};
</script>
