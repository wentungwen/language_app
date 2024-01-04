<template>
  <b-container>
    <b-row class="justify-content-center sticky-row bg-light">
      <!-- filter -->
      <b-col cols="8">
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
        <b-row class="justify-content-center" v-if="is_filtered_alert_shown">
          <p>nothing here, try other keywords</p>
          <b-img
            :src="require('@/assets/nothing.png')"
            style="max-width: 300px"
          ></b-img>
        </b-row>
      </b-col>
    </b-row>
    <!-- view control start -->
    <b-row class="p-3 bg-white" v-if="!is_filtered_alert_shown">
      <b-col
        ><b-btn-toolbar aria-label="Toolbar with button groups">
          <b-btn-group role="group" aria-label="view-group">
            <b-button variant="dark" disabled>view</b-button>
            <b-button
              variant="outline-dark"
              :disabled="col_view < 3"
              @click="adjust_col_view(-1)"
            >
              <b-icon-dash></b-icon-dash>
            </b-button>
            <b-button
              variant="outline-dark"
              :disabled="col_view > 5"
              @click="adjust_col_view(1)"
            >
              <b-icon-plus></b-icon-plus>
            </b-button>
          </b-btn-group> </b-btn-toolbar
      ></b-col>
    </b-row>
    <!-- view control end -->
    <!-- displayed conversation cards -->
    <b-row class="p-3 bg-white" v-if="!is_filtered_alert_shown">
      <b-col
        v-for="conversation in displayed_conversation"
        :key="conversation.conversation_id"
        :cols="col_view"
      >
        <b-card class="mb-4" @click="open_card_modal(conversation)">
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
              </div>
            </div>
          </template>
        </b-card>
      </b-col>
    </b-row>
    <!-- modal start -->
    <b-modal id="conv-modal" v-model="is_popup_open" hide-footer>
      <template #modal-title>
        {{ modal_conversation.topic }}
      </template>
      <!-- message start -->
      <div
        v-for="(message, index) in modal_conversation.conversations"
        :key="index"
      >
        <Transition name="slide-fade">
          <div>
            <p>{{ message.sender }}: {{ message.content }}</p>
            <p
              class="badge bg-secondary"
              v-if="modal_conversation.is_translation_shown"
              v-html="decode_HTML_entities(message.translation)"
            ></p>
          </div>
        </Transition>
      </div>
      <!-- messages end -->

      <!-- action alerts -->
      <b-alert :show="is_copied" class="m-3 alert-success">Copied!</b-alert>
      <!-- buttons start-->
      <b-button
        class="mr-2 btn-secondary btn-sm"
        @click="copy_btn(modal_conversation)"
      >
        <b-icon-clipboard></b-icon-clipboard>
        Copy</b-button
      >
      <b-button
        class="mr-2 btn-secondary btn-sm"
        @click="translate_btn(modal_conversation)"
      >
        <b-icon-translate></b-icon-translate>
        Translate</b-button
      >
      <!-- button end -->
    </b-modal>
    <!-- modal end -->
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
      col_view: 3,
      is_copied: false,
      is_translation_shown: false,
      translated_conversations: [],
      all_conversations: [],
      is_popup_open: false,
      modal_conversation: {},
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
    open_card_modal(conv) {
      this.is_popup_open = true;
      this.modal_conversation = conv;
    },
    adjust_col_view(num) {
      this.col_view += num;
    },
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
    decode_HTML_entities(text) {
      const element = document.createElement("textarea");
      element.innerHTML = text;
      return element.value;
    },
    copy_btn(conversation) {
      let text = "";
      for (let i = 0; i < conversation.conversations.length; i++) {
        text += `${conversation.conversations[i].content}\n`;
      }
      navigator.clipboard.writeText(text);
      this.is_copied = true;
      setTimeout(() => {
        this.is_copied = false;
      }, 1000);
    },
    translate_btn(conversation) {
      if (conversation.conversations[0].translation) {
        conversation.is_translation_shown = !conversation.is_translation_shown;
      } else {
        const lan_code = conversation.lan_code;
        const conversations = conversation.conversations;
        const translate_to_lan_code = conversation.lan_code;
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
      this.all_conversations = res.data.data.map((conversation) => ({
        ...conversation,
        is_translation_shown: false,
      }));
    });
  },
};
</script>
<style>
.card {
  box-shadow: 3px 3px 6px #00000040;
  border: none !important;
  overflow: hidden;
}
.card-header {
  background-color: rgb(209, 242, 250) !important;
}
</style>
<style scoped lang="scss">
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

.card-footer {
  visibility: hidden;
  transition: transform 0.3s;
}

.card {
  overflow: hidden;
  height: 300px;
  &:hover {
    box-shadow: 1rem 1rem 3rem rgba(0, 0, 0, 0.2);
    cursor: pointer;
    .card-footer {
      visibility: visible;
    }
  }
}
.card_extend {
  overflow: visible;
  height: fit-content;
  min-height: 300px;
}

.sticky-row {
  position: sticky;
  top: 0;
  z-index: 1;
}
</style>
