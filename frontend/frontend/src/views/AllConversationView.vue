<template>
  <b-container>
    <b-row class="justify-content-center">
      <!-- filter -->
      <b-row>
        <h4>See other people's conversations</h4>
        <b-form class="mb-3">
          <div class="row">
            <div class="col-md-3">
              <b-form-group label="" label-for="language-select-all">
                <b-form-select
                  id="language-select-all"
                  :options="language_options"
                  v-model="form_data.lan_code"
                ></b-form-select>
              </b-form-group>
            </div>
            <div class="col-md-6">
              <b-form-group label="" label-for="keyword-input">
                <div class="input-group">
                  <b-form-input
                    id="keyword-input"
                    placeholder="Enter keyword"
                    v-model="form_data.keyword"
                  ></b-form-input>
                </div>
              </b-form-group>
            </div>
          </div>
        </b-form>
        <b-row class="justify-content-center">
          <b-img
            v-if="is_filtered_alert_shown"
            :src="require('@/assets/nothing.png')"
            style="max-width: 300px"
          ></b-img>
          <hr />
          <!-- <h2>{{ form_data.lan_code }}</h2> -->
          <h2>{{ form_data.lan_text }}</h2>
        </b-row>
      </b-row>
      <b-row>
        <b-col
          v-for="conversation in displayed_conversation"
          :key="conversation.conversation_id"
          class="col-4"
        >
          <b-card class="mb-4">
            <template #header>
              <div class="d-flex justify-content-between align-items-center">
                <h4 class="mt-2">{{ conversation.topic }}</h4>
                <span class="badge bg-white text-dark">{{
                  conversation.date
                }}</span>
              </div>
            </template>
            <template #default>
              <div>
                <div
                  v-for="(message, index) in conversation.conversations"
                  :key="index"
                >
                  <p>{{ message.sender }}: {{ message.content }}</p>
                  <Transition name="slide-fade">
                    <div v-if="conversation.is_translation_shown">
                      <p
                        class="badge bg-secondary"
                        v-html="decode_HTML_entities(message.translation)"
                      ></p>
                    </div>
                  </Transition>
                </div>
              </div>
            </template>
            <template #footer>
              <!-- action alerts -->
              <b-alert
                :show="
                  is_copied && copied_index === conversation.conversation_id
                "
                class="m-3 alert-success"
                >Copied!</b-alert
              >
              <!-- button here -->

              <b-button
                class="mr-2 btn-secondary"
                @click="copy_btn(conversation)"
              >
                <b-icon-clipboard></b-icon-clipboard>
                Copy</b-button
              >
              <b-button
                class="mr-2 btn-secondary"
                @click="translate_btn(conversation)"
              >
                <b-icon-translate></b-icon-translate>
                Translate</b-button
              >
              <b-button
                variant="primary"
                @click="save_conversation(conversation)"
                >Save</b-button
              >
            </template>
          </b-card>
        </b-col>
      </b-row>
    </b-row>
  </b-container>
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
      is_translation_shown: false,
      translated_conversations: [],
      all_conversations: [],
      language_options: [
        { value: "nl", text: "Dutch" },
        { value: "es", text: "Spanish" },
        { value: "ja", text: "Japanese" },
      ],
      form_data: {
        lan_code: "nl",
        keyword: "",
        lan_text: "Dutch",
      },
      filtered_conversations: [],
      is_filtered_alert_shown: false,
    };
  },
  methods: {
    filter_conversation() {
      this.is_filtered_alert_shown = false;
      const target_lan = this.form_data.lan_code;
      const target_keyword = this.form_data.keyword;

      if (!target_lan && !target_keyword) {
        // Both language and keyword are empty
        alert("Please enter a language or keyword");
        return;
      }

      this.filtered_conversations = this.all_conversations.filter(
        (conversation) => {
          if (target_lan && target_keyword) {
            return (
              conversation.lan_code === target_lan &&
              conversation.conversations.some((conv) =>
                conv.content.includes(target_keyword)
              )
            );
          } else {
            return conversation.lan_code === target_lan;
          }
        }
      );

      if (this.filtered_conversations.length === 0) {
        // No conversations match the filter
        this.is_filtered_alert_shown = true;
      }
    },
    save_conversation(conversation) {
      console.log(conversation);
      const token = localStorage.getItem("token");
      const config = {
        headers: {
          Authorization: token,
        },
      };
      const payload = {
        data: conversation,
      };
      axios.post("http://127.0.0.1:5000/save", payload, config).then((res) => {
        console.log(res);
      });
    },
    decode_HTML_entities(text) {
      const element = document.createElement("textarea");
      element.innerHTML = text;
      return element.value;
    },
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
    translate_btn(conversation) {
      if (conversation.conversations[0].translation) {
        conversation.is_translation_shown = !conversation.is_translation_shown;
      } else {
        const lan_code = conversation.lan_code;
        const conversations = conversation.conversations;
        const translate_to_lan_code = this.translate_to_lan_code;
        const payload = {
          lan_code,
          conversations,
          translate_to_lan_code,
        };
        axios
          .post("http://127.0.0.1:5000/translate", payload)
          .then((res) => {
            conversation.is_translation_shown = true;
            conversation.conversations.forEach((message, idx) => {
              message.translation = res.data.conversations[idx].content;
            });
          })
          .catch((err) => {
            console.log(err);
          });
      }
    },
  },
  computed: {
    displayed_conversation() {
      if (this.filtered_conversations.length > 0) {
        return this.filtered_conversations;
      } else {
        return this.all_conversations.filter((conversation) => {
          return conversation.lan_code === this.form_data.lan_code;
        });
      }
    },
  },
  watch: {
    form_data: {
      deep: true,
      handler() {
        this.filter_conversation();
      },
    },
    "form_data.lan_code"(new_value) {
      this.form_data.lan_text = this.language_options.find(
        (option) => option.value === new_value
      ).text;
    },
  },
  created() {
    axios.get("http://127.0.0.1:5000/get-all-conversations").then((res) => {
      console.log(res);
      this.all_conversations = res.data.data.map((conversation) => ({
        ...conversation,
        is_translation_shown: false,
      }));
    });
  },
};
</script>
<style>
.slide-fade-enter-active {
  transition: all 0.3s ease-out;
}

.slide-fade-leave-active {
  transition: all 0.4s cubic-bezier(1, 0.5, 0.8, 1);
}

.slide-fade-enter-from,
.slide-fade-leave-to {
  transform: translateX(20px);
  opacity: 0;
}
.card {
  box-shadow: 3px 3px 6px #00000040;
  border: none !important;
  overflow: hidden;
}
.card-footer {
  transform: translateY(50%);
  visibility: hidden;
  transition: transform 0.3s;
}

.card:hover .card-footer {
  transform: translateY(0);
  visibility: visible;
}
</style>
