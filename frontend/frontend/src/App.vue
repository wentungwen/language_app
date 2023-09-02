<template>
  <div class="d-flex flex-column wrapper bg-light">
    <div id="app">
      <b-row v-if="loading">
        <b-img
          style="max-width: 300px"
          :src="require('@/assets/loading.gif')"
          center
        ></b-img>
      </b-row>
      <b-row v-else>
        <b-row class="col-auto">
          <NavBar
            :conversations="conversations"
            :user_id="user_id"
            :get_conversations="get_conversations"
            @load_conversation="load_conversation"
        /></b-row>
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
import NavBar from "@/components/NavBar.vue";
import FooterBlock from "@/components/FooterBlock.vue";
import axios from "axios";
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
  },
  methods: {
    load_conversation(conversation_id) {
      this.loaded_conversation = this.conversations.find(
        (conversation) => conversation.conversation_id === conversation_id
      );
    },
    get_conversations() {
      const token = localStorage.getItem("token");
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
html {
  height: 100vh !important;
}
#app,
body {
  height: 100% !important;
  margin: 0;
}
.wrapper {
  height: 100%;
}
</style>
