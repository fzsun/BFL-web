// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import VueFormGenerator from 'vue-form-generator'

require('./mystyles.scss');

Vue.config.productionTip = false;

Vue.use(VueFormGenerator)
new Vue({
  el: '#app',
  router,
  components: {
    App,
    VueFormGenerator
  },
  template: '<App/>'
})
