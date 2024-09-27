import Vue from 'vue'
import App from './App.vue'
import axios from 'axios'
import config from './config'

Vue.config.productionTip = false

axios.defaults.baseURL = config.baseURL

Vue.prototype.$axios = axios

new Vue({
  render: h => h(App),
}).$mount('#app')
