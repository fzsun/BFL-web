// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import VueFormGenerator from "vue-form-generator"
import S_BFLS from "./components/S_BFLS";
import './../node_modules/bulma/css/bulma.css';

Vue.config.productionTip = false

Vue.use(VueFormGenerator)
/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { 
    App,
    VueFormGenerator
  },
  template: '<App/>'
})
