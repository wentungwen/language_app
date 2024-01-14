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
        <SideBar
          :conversations="conversations"
          :user_id="user_id"
          :get_conversations="get_conversations"
          @load_conversation="load_conversation"
          v-if="$route.meta.ShowSidebar"
        />
        <RouterView
          :conversations="conversations"
          :loaded_conversation="loaded_conversation"
          :get_conversations="get_conversations"
          @to_next_conversation="handle_next_conversation"
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
export default {
  data() {
    return {
      user_id: null,
      loading: false,
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
    handle_next_conversation(conv_id) {
      const target_id = this.conversations.findIndex(
        (conv) => conv.conversation_id === conv_id
      );
      const next_conv = this.conversations[target_id + 1];
      this.loaded_conversation = next_conv;
    },
    load_conversation(conversation_id) {
      if (this.loaded_conversation) {
        this.loaded_conversation = this.conversations.find(
          (conversation) => conversation.conversation_id === conversation_id
        );
      }
    },
    get_conversations() {
      const token = this.get_cookie("token");
      const config = {
        headers: {
          Authorization: token,
        },
      };
      axios
        .get(`${process.env.VUE_APP_API_BASE_URL}/get-conversations`, config)
        .then((res) => {
          if (res.data) {
            this.conversations = res.data["data"];
            this.loaded_conversation = this.conversations[0];
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
