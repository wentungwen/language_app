import Vue from "vue";
import VueRouter from "vue-router";
import HomeView from "../views/HomeView.vue";
import AllConversationView from "../views/AllConversationView.vue";
import CustomListeningView from "../views/CustomListeningView.vue";
Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "home",
    component: HomeView,
  },
  {
    path: "/all-conversations",
    name: "all-conversations",
    component: AllConversationView,
  },
  {
    path: "/custom-listening",
    name: "custom-listening",
    component: CustomListeningView,
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

export default router;
