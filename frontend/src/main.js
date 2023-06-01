import Vue from 'vue'
import App from './App.vue'
import router from "./router";
import Argon from "./plugins/argon-kit";
// import request from './api/request';

import axios from 'axios';


import {Message, Tabs, TabPane, Table, TableColumn, Input, Icon, Select, Option, Form, FormItem, Card, Pagination } from 'element-ui';
import lang from 'element-ui/lib/locale/lang/en'
import locale from 'element-ui/lib/locale'
locale.use(lang)

Vue.use(Tabs);
Vue.use(TabPane);
Vue.use(Table);
Vue.use(TableColumn);
Vue.use(Input);
Vue.use(Icon);
Vue.use(Select);
Vue.use(Option);
Vue.use(Form);
Vue.use(FormItem);
Vue.use(Card);
Vue.use(Pagination);


Vue.prototype.$message = Message;
import VueApexCharts from 'vue-apexcharts'
Vue.use(VueApexCharts)

Vue.component('apexchart', VueApexCharts)
axios.defaults.baseURL = 'http://bakatat.pythonanywhere.com/'
axios.defaults.headers.post['Content-Type'] = 'application/x-www-from-urlencoded'
// Vue.prototype.$http = request;
Vue.prototype.$axios = axios;
Vue.config.productionTip = false

Vue.use(Argon);
Vue.filter("currency", (n) => {
  if (typeof n !=="number") {
    return n;
  }
    const formatter = new Intl.NumberFormat('en-UK',{
      style: 'currency',
      currency: 'GBP',
      minimumFractionDigits: 0,
    });
    return formatter.format(n);
});
new Vue({
  render: h => h(App),
  router
}).$mount('#app')
