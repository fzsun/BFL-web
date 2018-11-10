<template>
<div>
    <div id="s_bfl" class="container">
        <div class="is-size-4">
            A tool for decision makers to determine the most cost effective 
            way to produce and transport sorghum for use in biofuels. The tool itself
            is an optimization algorithm and simulization that work in tandem to find 
            and test an optimial solution. To learn more about the algorithm 
            <a>see here.</a> 
        </div>
        <br>
        <div class="is-size-4">
            Because this is a large optimization model with many inputs, we have 
            created an excel template for users to input the details of their 
            specific problem into the model we have developed.
        </div><br>
        <tabs>
            <tab name="Step 1" :selected="true">
              <div class="is-size-5">
                To input the specifics of your problem please click download
                to get an excel template for inputting your data.
              </div>
              <br>
              <button @click="download" class="button">Download</button>
            </tab>
            <tab name="Step 2">
              <div class="is-size-5">
                Upload a csv file of your filled out template
              </div>
              <br>
              <input type="file" @change="updateFile">
            </tab>
            <tab name="Step 3">
              <div class="is-size-5">
                So you don't have to leave the browser open for an hour
                so that our optimization can have time to run. Please 
                provide your email below so that we can send you the results.
              </div>
              <input 
                class="input" 
                type="email" 
                placeholder="Enter your email here"
                v-model="email"
              >
              <button @click="optimize" class="button">Email me the optimial results</button>
            </tab>
        </tabs>
    </div>
</div>
</template>

// <script>

// Vue.component('tabs', {
//   template: `
//   <div>
//     <div class="tabs is-boxed">
//       <ul>
//         <li v-for="tab in tabs" v-bind:class="{'is-active': tab.isActive}">
//           <a @click="selectTab(tab)">
//             {{ tab.name }}
//           </a>
//          </li>
//       </ul>
//     </div>
//     <div class="tab-details">
//       <slot></slot>
//     </div>
//   </div>
// `,
//   data() {
//     return {
//       tabs: [],
//     }
//   },
//   created() {
//     this.tabs = this.$children;
//   },
//   methods: {
//     selectTab(selectedTab) {
//      this.tabs.forEach(
//       function(tab){
//         tab.isActive = (selectedTab.name == tab.name)
//       }
//      ) 
//     }
//   }
// });

// Vue.component('tab', {
//   template: `
//     <div v-show="isActive">
//       <slot>
//       </slot>
//     </div>
// `,
//   props: {
//     name: {
//       required: true,
//     },
//     selected: {
//       default: false
//     }
//   },
//   data() {
//     return {
//       isActive: false
//     }
//   },
//   mounted() {
//     this.isActive = this.selected;
//   }
// });

// new Vue({
//     el: '#s_bfl',
//     data: {
//         email: "",
//         selectedfile: null,
//         response: []
//     },
//     methods: {
//       updateFile(event){
//         this.selectedfile = event.target.files[0];
//       },
//       optimize(event){
//         let csvToJson = require('convert-csv-to-json');
//         console.log("Optimizing")
//         fd = new FormData();
//         fd.append('optimizationInput', this.selectedfile, this.selectedfile.name);

//         let jsonInputData = csvToJson.getJsonFromCsv(this.selectedfile);

//         console.log(jsonInputData);

//         // axios.post('http://localhost:5000/upload/', this.selectedfile).then(response => {
//         //     this.response = response.data;
//         //     console.log(this.response);
//         // })
//       },
//       download(event){
//         console.log("Running Download");
//         axios({
//           url: 'http://localhost:5000/download/',
//           method: 'GET',
//           responseType: 'blob',
//           headers: {
//             'Accept': 'application/vnd.openxmlformats-officedocument'
//            + '.spreadsheetml.sheet',
//           }
//         }).then((response) => {
//           const url = window.URL.createObjectURL(new Blob([response.data], ));
//           const link = document.createElement('a');
//           link.href = url;
//           link.setAttribute('download', 'template.xlsx');
//           document.body.appendChild(link);
//           link.click();
//           link.parentNode.removeChild(link);
//         })
//       }
//     }
// })
// </script>
