import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import { BootstrapVue, IconsPlugin } from "bootstrap-vue";
// import axios from "axios";
import authMixin from "./mixins/AuthMixins";

import "bootstrap/dist/css/bootstrap.css";
import "bootstrap-vue/dist/bootstrap-vue.css";
import "./assets/css/bootstrap3.min.css";
Vue.mixin(authMixin);

Vue.use(BootstrapVue);
Vue.use(IconsPlugin);
Vue.config.productionTip = false;

export const eventBus = new Vue();

new Vue({
  router,
  render: (h) => h(App),
}).$mount("#app");
