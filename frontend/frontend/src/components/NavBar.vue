<template>
  <div>
    <b-navbar toggleable="lg" type="dark" variant="primary">
      <b-navbar-brand class="pl-2" href="/">Language Helper</b-navbar-brand>
      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav v-for="route in routes" :key="route.path">
          <b-nav-item :to="route.path" class="nav-decoration"
            ><b-icon :icon="route.icon" class="mr-1"></b-icon
            >{{ route.name }}</b-nav-item
          >
        </b-navbar-nav>

        <!-- Right aligned nav items -->
        <b-navbar-nav class="ml-auto">
          <b-nav-item to="/user-setting">
            <b-icon-person-circle></b-icon-person-circle>
            <strong>
              {{ username ? "Welcome, " + username : "Please login" }}!</strong
            >
          </b-nav-item>

          <!-- Sign up/ login/logout link  -->
          <b-nav-item v-if="!is_logged_in" v-b-modal.modal-signup
            >Sign up</b-nav-item
          >
          <b-nav-item v-if="!is_logged_in" v-b-modal.modal-login
            >Login</b-nav-item
          >
          <b-nav-item v-if="is_logged_in" @click="logout_submit()"
            >Logout</b-nav-item
          >
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>
    <!-- signup modal -->
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
    <!-- Login modal  -->
    <b-modal id="modal-login" title="login" @ok="login_submit">
      <b-form ref="login-form">
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
        <p class="text-danger" v-if="login_warning !== null">
          {{ login_warning }}
        </p>
      </b-form>
    </b-modal>
  </div>
</template>
<script>
import axios from "axios";
export default {
  name: "NavBar",
  data() {
    return {
      username: localStorage.getItem("username"),
      routes: [
        { path: "/", name: "Conversation generator", icon: "box" },
        {
          path: "/all-conversations",
          name: "See other's conversation",
          icon: "people",
        },
        {
          path: "/custom-listening",
          name: "Custom Listening Test",
          icon: "book",
        },
      ],
      login_warning: null,
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
  methods: {
    login_submit(event) {
      event.preventDefault();
      if (this.login_data.email === "" || this.login_data.password === "") {
        this.login_warning = "Please enter email and password";
      } else {
        axios
          .post("http://127.0.0.1:5000/login", this.login_data)
          .then((res) => {
            this.set_cookie("token", res.data.token);
            localStorage.setItem("username", res.data.username);
            window.location.reload();
          })
          .catch((err) => {
            if (err.response && err.response.status === 404) {
              this.login_warning = "Wrong email or password.";
            } else {
              this.login_warning = "Something went wrong";
            }
          });
      }
      setTimeout(() => {
        this.login_warning = null;
      }, 2000);
    },
    signup_submit() {
      axios
        .post("http://127.0.0.1:5000/signup", this.signup_data)
        .then((res) => {
          this.set_cookie("token", res.data.token);
          localStorage.setItem("username", res.data.username);
          window.location.reload();
        })
        .catch((err) => {
          console.log(err);
        });
    },
    logout_submit() {
      localStorage.removeItem("username");
      this.delete_cookie("token");
      window.location.reload();
    },
  },
};
</script>
<style>
.nav-decoration a {
  position: relative;
  display: inline-block;
  padding-right: 10px;
}

.nav-decoration a::after {
  content: "";
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 2px;
  background-color: #ffffff;
  transform: scaleX(0);
  transition: transform 0.2s ease-in-out;
}

.nav-decoration a:hover::after,
.nav-decoration a.router-link-exact-active::after {
  transform: scaleX(0.5);
}
.nav-decoration a.router-link-exact-active {
  color: #ffffff !important;
}
.nav-link {
  color: rgba(255, 255, 255, 0.6) !important;
}
</style>
