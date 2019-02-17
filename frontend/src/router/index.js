import Vue from 'vue'
import Router from 'vue-router'

const routerOptions = [
  { path: '/', component: 'Home' },
  { path: '/s-bfls', name: 'S_BFLS', component: 'S_BFLS' },
  { path: '/about', name: 'About', component: 'About' },
  { path: '/map', name: 'Map', component: 'Map' }
]

const routes = routerOptions.map(route => {
  return {
    ...route,
    component: () => import(`@/components/${route.component}.vue`)
  }
})

Vue.use(Router)

export default new Router({
  routes,
  mode: 'history'
})
