<template>
  <div id="app">
    <b-row v-if="loading">
      <b-img
        style="max-width: 300px"
        :src="require('@/assets/loading.gif')"
        center
      ></b-img>
    </b-row>
    <b-row v-else>
      <b-col class="col-auto">
        <NavBar
          :conversations="conversations"
          :user_id="user_id"
          :get_conversations="get_conversations"
          @conversation_deleted="get_conversations"
          @load_conversation="load_conversation"
      /></b-col>
      <b-col class="col-4">
        <GenerateForm :user_id="user_id" />
        <ConversationBlock
          :loaded_conversation="loaded_conversation"
          :conversation="conversations[active_conversation]"
          @save_btn_clicked="get_conversations"
        />
      </b-col>
      <b-col class="col picture-block">
        <PictureBlock />
      </b-col>
    </b-row>
  </div>
</template>
<script>
import NavBar from "@/components/NavBar.vue";
import GenerateForm from "./components/GenerateForm.vue";
import ConversationBlock from "./components/ConversationBlock.vue";
import PictureBlock from "./components/PictureBlock.vue";
import axios from "axios";

export default {
  components: {
    NavBar,
    GenerateForm,
    ConversationBlock,
    PictureBlock,
  },
  data() {
    return {
      user_id: null,
      username: null,
      loading: false,
      active_conversation: 1,
      conversations: [],
      loaded_conversation: null,
    };
  },
  methods: {
    load_conversation(conversation_id) {
      // Find the conversation with the matching conversation_id
      this.loaded_conversation = this.conversations.find(
        (conversation) => conversation.conversation_id === conversation_id
      );
    },
    save_btn_clicked() {
      this.get_conversations();
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
  mounted() {
    this.get_conversations();
  },
};
</script>

<style scoped>
#app {
  height: 100vh;
}
body {
  min-height: 100vh;
}
.picture-block {
  max-width: 700px;
}
</style>
