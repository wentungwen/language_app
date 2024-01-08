<template>
  <div>
    <b-row class="justify-content-center mb-3">
      <b-col cols="10">
        <b-card-group>
          <b-card class="flex-row">
            <div>
              <h1>username</h1>
              <p>email@gmial.com</p>
            </div>

            <template #footer>
              <b-button type="button" variant="primary" @click="edit_btn">
                <b-icon-pen></b-icon-pen>
                Edit
              </b-button>
            </template>
          </b-card>
        </b-card-group>
      </b-col>
    </b-row>
    <b-row class="justify-content-center mb-3">
      <b-col cols="10">
        <b-card class="px-2">
          <b-row class="flex-wrap">
            <h2>Your conversations</h2>
            <hr />
            <b-col
              cols="4"
              v-for="(conversation, idx) in conversations"
              :key="idx"
            >
              <b-card class="mb-4">
                <template #header>
                  <div
                    class="d-flex justify-content-between align-items-center"
                  >
                    <h4 class="mt-2">{{ conversation.topic }}</h4>
                    <div>
                      <!-- <span class="badge bg-white text-dark mr-1">{{
                        conversation.date
                      }}</span> -->
                      <span class="badge bg-white text-dark">{{
                        conversation.lan_code
                      }}</span>
                    </div>
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
              </b-card>
            </b-col>
          </b-row>
        </b-card>
      </b-col>
    </b-row>

    <b-modal
      id="modal-setting"
      title="Edit modal"
      class="d-flex flex-row justify-content-center align-items-center"
      size="lg"
      v-model="is_edit_modal_shown"
      @ok="user_edit_submit"
    >
      <b-row>
        <b-col cols="4">
          <img class="img-fluid" src="../assets/user_modal.png" alt="" />
        </b-col>
        <b-col cols="8" class="d-flex flex-column justify-content-center">
          <form ref="signup-form" class="mx-2">
            <b-input-group class="mb-4">
              <template #prepend>
                <b-input-group-text>Username</b-input-group-text>
              </template>
              <b-form-input
                id="setting-username-input"
                type="text"
                required
                v-model="user_input_data.username"
              ></b-form-input>
            </b-input-group>
            <b-input-group class="mb-4">
              <template #prepend>
                <b-input-group-text>Email</b-input-group-text>
              </template>
              <b-form-input
                id="setting-email-input"
                type="email"
                required
                v-model="user_input_data.email"
              ></b-form-input>
            </b-input-group>
            <b-input-group>
              <template #prepend>
                <b-input-group-text>Password</b-input-group-text>
              </template>
              <b-form-input
                id="setting-password-input"
                type="password"
                required
                v-model="user_input_data.password"
              ></b-form-input>
            </b-input-group>
          </form>
        </b-col>
      </b-row>
    </b-modal>
  </div>
</template>
<script>
import AuthMixins from "@/mixins/AuthMixins";
// import axios from "axios";
export default {
  name: "UserSettingView",
  mixins: [AuthMixins],
  props: {
    get_conversations: Function,
    conversations: Array,
    username: {
      type: String,
      default: "",
    },
  },
  data() {
    return {
      is_edit_modal_shown: false,
      all_conversations: [],
      user_input_data: {
        username: "",
        email: "",
        password: "",
      },
    };
  },
  methods: {
    user_edit_submit() {
      console.log("edit");
    },
    edit_btn() {
      console.log(this.is_edit_modal_shown);
      this.is_edit_modal_shown = true;
    },
  },
  mounted() {
    if (this.is_logged_in) {
      this.get_conversations();
      const username = localStorage.getItem("username");
      this.user_input_data.username = username;
    }
  },
};
</script>
<style scoped>
.card-footer {
  display: flex;
  justify-content: center;
  align-items: center;
}
.card-footer {
  border-top: none;
}
</style>
<style></style>
