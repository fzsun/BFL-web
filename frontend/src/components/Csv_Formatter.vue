<template>
<vue-json-to-csv :json-data="op_response_csv"
:labels="{
    farm: { title: 'Farm' },
    ssl: { title: 'SSL' },
    week_1: { title: 'week 1' },
    week_1: { title: 'week 1' },
    week_2: { title: 'week 2' },
    week_3: { title: 'week 3' },
    week_4: { title: 'week 4' },
    week_5: { title: 'week 5' },
    week_6: { title: 'week 6' },
    week_7: { title: 'week 7' },
    week_8: { title: 'week 8' },
    week_9: { title: 'week 9' },
    week_10: { title: 'week 10' },
    week_11: { title: 'week 11' },
    week_12: { title: 'week 12' },
    week_13: { title: 'week 13' },
    week_14: { title: 'week 14' },
    week_15: { title: 'week 15' },
    week_16: { title: 'week 16' },
    week_17: { title: 'week 17' },
    week_18: { title: 'week 18' },
    week_19: { title: 'week 19' },
    week_20: { title: 'week 20' },
    week_21: { title: 'week 21' },
    week_22: { title: 'week 22' },
    week_23: { title: 'week 23' }
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
        generateCsv(data) {
			console.log(data);
            var k = 0;
            var i;
            for (i = 0; i < data.length; i++) {
                var parts = data[i][0].split("[");
                if (parts[0] == "farm_to_ssl")  {
                    var inner_parts = parts[1].split(",");
                    this.op_response_csv[k++] = {farm: inner_parts[0],
                                                 ssl: inner_parts[1].split("]")[0]};
                } else if (parts[0] == "shipped_farm_ssl") {
                    var inner_parts = parts[1].split(",");
                    this.op_response_csv[parseInt(inner_parts[1])]["week_" + inner_parts[0]] = data[i][1];
                }
            }
            console.log(this.op_response_csv);
            document.getElementById('optimization_csv_button').hidden = false;
        }
    }
};
</script>







