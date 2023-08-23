<template>
  <div
    class="dialog-block mt-4 bg-light pb-3"
    aria-label="Toolbar with button groups"
  >
    <!-- Toolbar -->
    <b-button-toolbar class="toolbar">
      <b-button-group class="">
        <b-button
          @click="translate_btn(received_data)"
          variant="secondary"
          :disabled="is_editing"
          >Translate</b-button
        >
        <b-button @click="copy_btn" variant="secondary" :disabled="is_editing"
          >Copy</b-button
        >
        <b-button @click="edit_btn" variant="secondary">Edit</b-button>
        <b-button @click="save_btn" variant="secondary" :disabled="is_editing"
          >Save</b-button
        >
      </b-button-group>
    </b-button-toolbar>
    <!-- action alerts -->
    <b-alert :show="is_copied" class="m-3 alert-success">Copied!</b-alert>
    <b-alert :show="is_saved" class="m-3 alert-success">Saved!</b-alert>
    <!-- conversation editing block -->
    <div v-if="is_editing" class="dialog-content m-3">
      <p v-for="(msg, idx) in edited_conversations" :key="idx">
        <b>{{ msg.sender }}:</b>
        <b-form-input
          id="topic-input"
          v-model="msg.content"
          :required="true"
        ></b-form-input>
      </p>
      <b-button @click="edit_submit_btn" variant="secondary">Save</b-button>
    </div>
    <!-- conversation -->
    <div v-else class="dialog-content m-3" ref="copy_conversations">
      <div v-if="is_translation_shown">
        <p
          v-for="(msg, idx) in translated_conversations.conversations"
          :key="idx"
        >
          <b>{{ msg.sender }}:</b>
          {{ msg.content }}
        </p>
      </div>
      <div v-else>
        <div v-if="received_data">
          <p v-for="(msg, idx) in received_data.conversations" :key="idx">
            <b>{{ msg.sender }}:</b>
            {{ msg.content }}
          </p>
        </div>
        <div v-else-if="this.loaded_conversation">
          <p v-for="(msg, idx) in loaded_conversation.conversations" :key="idx">
            <b>{{ msg.sender }}:</b>
            {{ msg.content }}
          </p>
        </div>
        <div v-else>
          <p class="text-secondary">Please generate conversations</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { eventBus } from "@/main";
import axios from "axios";
export default {
  data() {
    return {
      is_copied: false,
      is_saved: false,
      is_translation_shown: false,
      is_editing: false,
      translate_to_lan_code: "en",
      edited_conversations: [],
      translated_conversations: [],
      received_data: null,
    };
  },
  props: {
    conversation: {
      type: Object,
    },
    loaded_conversation: {
      type: Object,
    },
  },
  methods: {
    save_btn() {
      const payload = {
        data: this.received_data,
      };
      axios
        .post(`http://127.0.0.1:5000/save/${this.user_id}`, payload)
        .then((res) => {
          if (res.status === 200) {
            this.is_saved = true;
            this.$emit("save_btn_clicked");
            setTimeout(() => {
              this.is_saved = false;
            }, 2000);
          }
        })
        .catch((err) => {
          console.log(err);
        });
    },
    edit_btn() {
      this.edited_conversations = this.received_data.conversations;
      this.is_editing = true;
    },
    edit_submit_btn() {
      this.received_data.conversations = this.edited_conversations;
      this.is_editing = false;
      this.is_translation_shown = false;
      this.translated_conversations = [];
    },
    translate_btn(received_data) {
      if (this.translated_conversations.length === 0) {
        this.translate_content(
          received_data.lan_code,
          received_data.conversations,
          this.translate_to_lan_code
        );
      } else {
        this.is_translation_shown = !this.is_translation_shown;
      }
    },
    translate_content(lan_code, conversations, translate_to_lan_code) {
      const payload = {
        lan_code,
        conversations,
        translate_to_lan_code,
      };
      // send to backend to translate
      axios
        .post("http://127.0.0.1:5000/translate", payload)
        .then((res) => {
          this.is_translation_shown = !this.is_translation_shown;
          this.translated_conversations = res.data;
        })
        .catch((err) => {
          console.log(err);
        });
    },
    copy_btn() {
      const conversationsDiv = this.$refs.copy_conversations;
      const range = document.createRange();
      range.selectNode(conversationsDiv);

      // Create a selection to work with the range
      const selection = window.getSelection();
      selection.removeAllRanges();
      selection.addRange(range);

      document.execCommand("copy");
      selection.removeAllRanges();
      this.is_copied = true;
      setTimeout(() => {
        this.is_copied = false;
      }, 2000);
    },
  },
  watch: {
    loaded_conversation(loaded_data) {
      console.log("loaded_data", loaded_data);
      if (loaded_data) {
        this.received_data = loaded_data;
        eventBus.$emit("received_data", this.received_data);
      }
    },
  },
  mounted() {
    eventBus.$on("generated_data", (data) => {
      if (data) {
        this.received_data = data;
        this.received_data.translated_conversations =
          this.translated_conversations;

        eventBus.$emit("received_data", this.received_data);
        this.translated_conversations = [];
        this.edited_conversations = [];
        this.is_editing = false;
      }
    });
  },
};
</script>

<style>
.toolbar {
  display: flex;
  justify-content: space-between;
  padding: 10px;
  border-bottom: 1px solid #ccc;
}
</style>
