<template>
  <div class="about">
    <div class="d-flex">
      <b-button href="/" class="mb-3 mr-3"> Go back </b-button>
      <h4>See other people's conversations</h4>
    </div>
    <!-- filter -->
    <b-form @submit="filter_conversation">
      <div class="row">
        <div class="col-md-3">
          <b-form-group label="" label-for="language-select-all">
            <b-form-select
              id="language-select-all"
              :options="language_options"
              v-model="formData.lan_code"
              >I'm learning:</b-form-select
            >
          </b-form-group>
        </div>
        <div class="col-md-6">
          <b-form-group label="" label-for="keyword-input">
            <div class="input-group">
              <b-form-input
                id="keyword-input"
                placeholder="Enter keyword"
              ></b-form-input>
              <div class="input-group-append">
                <b-button type="submit">Search</b-button>
              </div>
            </div>
          </b-form-group>
        </div>
      </div>
    </b-form>
    <hr />
    <b-row>
      <b-col
        v-for="conversation in all_conversations"
        :key="conversation.conversation_id"
        class="col-4"
      >
        <b-card class="mb-4">
          <template #header>
            <h4>{{ conversation.topic }}</h4>
            <p>{{ conversation.date }}</p>
          </template>
          <template #default>
            <div>
              <div
                v-for="(message, index) in conversation.conversations"
                :key="index"
              >
                <p>{{ message.sender }}: {{ message.content }}</p>
              </div>
            </div>
          </template>
          <template #footer>
            <!-- action alerts -->
            <b-alert
              :show="is_copied && copied_index === conversation.conversation_id"
              class="m-3 alert-success"
              >Copied!</b-alert
            >
            <b-button
              variant="primary"
              class="mr-2"
              @click="copy_btn(conversation)"
            >
              Copy</b-button
            >
            <b-button variant="primary" class="mr-2">Translate</b-button>
            <b-button variant="primary">Save</b-button>
          </template>
        </b-card>
      </b-col>
    </b-row>
  </div>
</template>
<script>
import axios from "axios";
export default {
  props: {
    get_conversations: {
      type: Function,
    },
  },
  data() {
    return {
      copied_index: null,
      is_copied: false,
      all_conversations: [],
      language_options: [
        { value: "nl", text: "Dutch" },
        { value: "es", text: "Spanish" },
        { value: "ja", text: "Japanese" },
        { value: "all", text: "all" },
      ],
      formData: {
        lan_code: "nl",
      },
    };
  },
  methods: {
    filter_conversation() {},
    copy_btn(conversation) {
      const tempElement = document.createElement("textarea");
      this.copied_index = conversation.conversation_id;
      let text = "";
      for (let i = 0; i < conversation.conversations.length; i++) {
        text += conversation.conversations[i].content;
      }
      tempElement.value = text;
      document.body.appendChild(tempElement);
      tempElement.select();
      document.execCommand("copy");
      document.body.removeChild(tempElement);
      this.is_copied = true;
      setTimeout(() => {
        this.is_copied = false;
      }, 2000);
    },
  },
  created() {
    axios.get("http://127.0.0.1:5000/get-all-conversations").then((res) => {
      console.log(res);
      this.all_conversations = res.data.data;
    });
  },
};
</script>
<style></style>
