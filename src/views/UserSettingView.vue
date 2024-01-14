<template>
  <div>
    <b-row class="justify-content-center mb-3">
      <b-col cols="10">
        <b-card-group>
          <b-card class="flex-row">
            <div>
              <h1>@{{ user_input_data.origin_data.username }}</h1>
              <p>{{ user_input_data.origin_data.email }}</p>
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
              sm="6"
              md="4"
              lg="3"
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
    <!-- edit userdata modal start -->
    <b-modal
      id="modal-setting"
      title="Edit your data"
      class="d-flex flex-row justify-content-center align-items-center"
      size="md"
      v-model="is_edit_modal_shown"
      @ok="user_edit_submit"
    >
      <b-row>
        <!-- <b-col cols="4">
          <img class="img-fluid" src="../assets/user_modal.png" alt="" />
        </b-col> -->
        <b-col class="d-flex flex-column justify-content-center">
          <form ref="signup-form" class="mx-2">
            <!-- username input -->
            <b-input-group class="mb-4">
              <template #prepend>
                <b-input-group-text> Username</b-input-group-text>
              </template>
              <b-form-input
                id="setting-username-input"
                type="text"
                required
                v-model="user_input_data.new_data.username"
              ></b-form-input>
            </b-input-group>
            <!-- email input -->
            <b-input-group class="mb-4">
              <template #prepend>
                <b-input-group-text>Email</b-input-group-text>
              </template>
              <b-form-input
                id="setting-email-input"
                type="email"
                required
                v-model="user_input_data.new_data.email"
              ></b-form-input>
            </b-input-group>
            <div v-if="!is_changing_password">
              <b-button class="float-right" @click="change_password_btn">
                <a href="">change password</a></b-button
              >
            </div>

            <div v-else>
              <!-- original password input -->
              <b-input-group class="mb-4">
                <template #prepend>
                  <b-input-group-text>Old Password</b-input-group-text>
                </template>
                <b-form-input
                  id="setting-old_password-input"
                  type="password"
                  required
                  v-model="user_input_data.origin_data.password"
                ></b-form-input>
              </b-input-group>
              <!-- new password input -->
              <b-input-group>
                <template #prepend>
                  <b-input-group-text>New Password</b-input-group-text>
                </template>
                <b-form-input
                  id="setting-new_password-input"
                  type="password"
                  required
                  v-model="user_input_data.new_data.password"
                ></b-form-input>
              </b-input-group>

              <div class="text-danger" v-if="is_alert_shown">
                {{ alert_msg }}
              </div>
            </div>
          </form>
        </b-col>
      </b-row>
    </b-modal>
    <!-- edit userdata modal end -->
  </div>
</template>
<script>
import AuthMixins from "@/mixins/AuthMixins";
import axios from "axios";
// import { ListGroupPlugin } from "bootstrap-vue";
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
      is_changing_password: false,
      is_edit_modal_shown: false,
      is_updating: false,
      is_alert_shown: false,
      alert_msg: "",
      all_conversations: [],
      user_input_data: {
        user_id: "",
        origin_data: {
          username: "",
          email: "",
          password: "",
        },
        new_data: {
          username: "",
          email: "",
          password: "",
        },
      },
    };
  },
  methods: {
    user_edit_submit(evt) {
      evt.preventDefault();
      const n_data = this.user_input_data.new_data;
      const o_data = this.user_input_data.origin_data;
      // check if email or username is empty
      if (n_data.username.trim() === "" || n_data.email.trim() === "") {
        this.is_alert_shown = true;
        this.alert_msg = "The username or email is empty. Please fill in!";
      }
      // check if email is valid
      else if (this.is_valid_email(n_data.email)) {
        this.is_alert_shown = true;
        this.alert_msg = "The email is invalid.";
      }
      // check if changing password but one of the password input is empty
      else if (
        this.is_changing_password &&
        (n_data.password.trim() === "" || o_data.password.trim() === "")
      ) {
        console.log("pro");
        this.is_alert_shown = true;
        this.alert_msg = "The password input is empty. Please fill in!";
      }
      // send the data to backend
      else {
        const payload = this.user_input_data;
        console.log("payload", payload);
        axios
          .post(`${process.env.VUE_APP_API_BASE_URL}/update-user-data`, payload)
          .then((res) => {
            console.log(res);
            let old_data = this.user_input_data.origin_data;
            old_data.username = res.data.username;
            old_data.email = res.data.email;
            this.is_edit_modal_shown = false;
          })
          .catch((err) => {
            console.error(err);
            this.is_alert_shown = true;
            this.alert_msg = "Failed to update user data. Please try again.";
          });
      }
    },
    is_valid_email(email) {
      // Regular expression pattern for email validation
      const email_pattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      return email_pattern.test(email);
    },
    change_password_btn(evt) {
      evt.preventDefault();
      this.is_changing_password = true;
    },
    edit_btn() {
      this.is_edit_modal_shown = true;
    },
  },
  mounted() {
    if (this.is_logged_in) {
      this.get_conversations();
      const user_data = JSON.parse(localStorage.getItem("lan_user_data"));
      this.user_input_data.origin_data.username = user_data.username;
      this.user_input_data.origin_data.email = user_data.email;
      this.user_input_data.new_data.username = user_data.username;
      this.user_input_data.new_data.email = user_data.email;
      this.user_input_data.user_id = user_data.user_id;
      console.log(this.user_input_data);
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
