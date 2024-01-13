import Vue from "vue";
import VueRouter from "vue-router";
import GeneratorView from "../views/GeneratorView.vue";
import AllConversationView from "../views/AllConversationView.vue";
import CustomListeningView from "../views/CustomListeningView.vue";
import UserSettingView from "../views/UserSettingView.vue";
Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "generator",
    component: GeneratorView,
    meta: {
      ShowSidebar: true,
    },
  },
  {
    path: "/all-conversations",
    name: "all-conversations",
    component: AllConversationView,
    meta: {
      ShowSidebar: false,
    },
  },
  {
    path: "/custom-listening",
    name: "custom-listening",
    component: CustomListeningView,
    meta: {
      ShowSidebar: true,
    },
  },
  {
    path: "/user-setting",
    name: "user-setting",
    component: UserSettingView,
    meta: {
      ShowSidebar: true,
    },
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

export default router;
