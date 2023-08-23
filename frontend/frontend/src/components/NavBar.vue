<template>
  <div>
    <b-button v-b-toggle.sidebar-1 class="m-2 mr-0 btn-light"
      ><b-icon-list></b-icon-list
    ></b-button>
    <b-sidebar id="sidebar-1" :title="sidebar_title" shadow>
      <b-col class="flex-grow-1" v-if="is_logged_in">
        <hr />
        <b-icon-bank></b-icon-bank>
        <span class="pl-2">Saved conversations</span>
        <hr />
        <ul class="nav nav-pills flex-column mb-auto">
          <div v-if="conversations">
            <li
              class="nav-item"
              v-for="conversation in conversations"
              v-bind:key="conversation.uuid"
            >
              <b-link
                href="#"
                @click="$emit('load_conversation', conversation.uuid)"
                class="text-white text-decoration-none"
                active
              >
                <div class="nav-link active mb-2" aria-current="page">
                  <b-link
                    @click="delete_conversations(conversation.uuid)"
                    class="text-white"
                  >
                    <b-icon-x-circle-fill></b-icon-x-circle-fill>
                  </b-link>
                  <span class="pl-2">{{ conversation.topic }}</span>
                </div>
              </b-link>
            </li>
          </div>
          <div v-else>Add conversations</div>
        </ul>
      </b-col>
      <!-- user photo and username -->
      <b-col class="position-absolute bottom-0">
        <b-link
          href="#"
          class="d-flex align-items-center link-dark text-decoration-none"
          id="dropdownUser2"
        >
          <hr />
          <img
            src="https://as1.ftcdn.net/v2/jpg/05/53/79/60/1000_F_553796090_XHrE6R9jwmBJUMo9HKl41hyHJ5gqt9oz.jpg"
            alt=""
            width="32"
            height="32"
            class="rounded-circle mr-2"
          />
          <strong>Welcome, User!</strong>
        </b-link>
        <hr />

        <!-- Sign up and login  -->
        <div class="signup_login_block" v-if="!is_logged_in">
          <b-link v-b-modal.modal-signup>Sign up</b-link>
          <b-modal id="modal-signup" title="Signup" @ok="signup_submit">
            <form ref="signup-form">
              <b-input-group class="mb-4">
                <template #prepend>
                  <b-input-group-text>Username</b-input-group-text>
                </template>
                <b-form-input
                  id="username-input"
                  type="text"
                  required
                  v-model="signup_data.username"
                ></b-form-input>
              </b-input-group>
              <b-input-group class="mb-4">
                <template #prepend>
                  <b-input-group-text>Email</b-input-group-text>
                </template>
                <b-form-input
                  id="email-input"
                  type="email"
                  required
                  v-model="signup_data.email"
                ></b-form-input>
              </b-input-group>
              <b-input-group>
                <template #prepend>
                  <b-input-group-text>Password</b-input-group-text>
                </template>
                <b-form-input
                  id="password-input"
                  type="password"
                  required
                  v-model="signup_data.password"
                ></b-form-input>
              </b-input-group>
            </form>
          </b-modal>
          <br />
          <!-- Login  -->
          <b-link v-b-modal.modal-login>Login</b-link>
          <b-modal id="modal-login" title="login" @ok="login_submit">
            <form ref="login-form">
              <b-input-group class="mb-4">
                <template #prepend>
                  <b-input-group-text>Email</b-input-group-text>
                </template>
                <b-form-input
                  id="email-input"
                  type="email"
                  required
                  v-model="login_data.email"
                ></b-form-input>
              </b-input-group>
              <b-input-group>
                <template #prepend>
                  <b-input-group-text>Password</b-input-group-text>
                </template>
                <b-form-input
                  id="password-input"
                  type="password"
                  required
                  v-model="login_data.password"
                ></b-form-input>
              </b-input-group>
            </form>
          </b-modal>
        </div>
        <!-- Logout  -->
        <div class="logout-block" v-if="is_logged_in">
          <b-link @click="logout_submit(user_id)">Logout</b-link>
        </div>
      </b-col>
    </b-sidebar>
  </div>
</template>
<script>
import axios from "axios";
export default {
  name: "NavBar",
  data() {
    return {
      token: localStorage.getItem("token"),
      sidebar_title: "Language Helper",
      signup_data: {
        username: "",
        email: "",
        password: "",
      },
      login_data: {
        email: "",
        password: "",
      },
    };
  },
  props: {
    conversations: {
      type: Array,
    },
    user_id: {
      type: Number,
    },
  },
  methods: {
    delete_conversations(id) {
      const url = "http://127.0.0.1:5000/delete_conversation/" + id;
      axios
        .delete(url)
        .then((res) => {
          if (res.status === 200) {
            this.$emit("conversation_deleted");
          }
        })
        .catch((err) => {
          console.log(err);
        });
    },
    login_submit() {
      axios
        .post("http://127.0.0.1:5000/login", this.login_data)
        .then((res) => {
          console.log("res", res);
          localStorage.setItem("token", res.data.token);
          window.location.reload();
        })
        .catch((err) => {
          console.log(err);
        });
    },
    signup_submit() {
      axios
        .post("http://127.0.0.1:5000/signup", this.signup_data)
        .then((res) => {
          localStorage.setItem("token", res.data.token);
          window.location.reload();
        })
        .catch((err) => {
          console.log(err);
        });
    },
    logout_submit(user_id) {
      axios
        .post(
          "http://127.0.0.1:5000/logout",
          { user_id: user_id },
          {
            headers: {
              Authorization: "Bearer " + this.token,
            },
          }
        )
        .then(() => {
          localStorage.removeItem("token");
          window.location.reload();
        })
        .catch((err) => {
          console.log(err);
        });
    },
  },
  computed: {
    is_logged_in() {
      return this.token !== null;
    },
  },
};
</script>
<style>
.sidebar {
  height: 100vh;
  width: 200px;
}
</style>
