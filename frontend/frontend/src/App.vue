<template>
  <div class="d-flex flex-column wrapper bg-light">
    <div id="app">
      <NavBar />
      <b-row v-if="loading">
        <b-img
          style="max-width: 300px"
          :src="require('@/assets/loading.gif')"
          center
        ></b-img>
      </b-row>
      <b-row v-else>
        <b-col class="col-auto">
          <SideBar
            :conversations="conversations"
            :user_id="user_id"
            :get_conversations="get_conversations"
            @load_conversation="load_conversation"
        /></b-col>
        <RouterView
          :conversations="conversations"
          :loaded_conversation="loaded_conversation"
          :get_conversations="get_conversations"
        />
      </b-row>
    </div>
    <FooterBlock />
  </div>
</template>
<script>
import { RouterView } from "vue-router";
import FooterBlock from "@/components/FooterBlock.vue";
import NavBar from "@/components/NavBar.vue";
import SideBar from "@/components/SideBar.vue";
import axios from "axios";
// import { BIconSortNumericDown } from "bootstrap-vue";
export default {
  data() {
    return {
      user_id: null,
      loading: false,
      active_conversation: 1,
      conversations: [],
      loaded_conversation: null,
    };
  },
  components: {
    RouterView,
    NavBar,
    FooterBlock,
    SideBar,
  },
  methods: {
    load_conversation(conversation_id) {
      this.loaded_conversation = this.conversations.find(
        (conversation) => conversation.conversation_id === conversation_id
      );
    },
    get_conversations() {
      const token = this.get_cookie("token");
      const config = {
        headers: {
          Authorization: token,
        },
      };
      axios
        .get(`http://127.0.0.1:5000/get-conversations`, config)
        .then((res) => {
          if (res.data) {
            this.conversations = res.data["data"];
          } else {
            this.conversations = [];
          }
        })
        .catch(() => {
          this.conversations = [];
        })
        .finally(() => {
          this.loading = false;
        });
    },
  },
};
</script>

<style>
html,
#app,
body {
  min-height: calc(100vh - 3rem) !important;
  margin: 0;
  overflow-x: hidden;
}
.wrapper {
  height: 100%;
}
</style>
