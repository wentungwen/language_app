<template>
  <div>
    <b-button variant="primary" v-b-toggle.sidebar-1 class="m-2 mr-0">
      <b-icon-list></b-icon-list
    ></b-button>
    <b-sidebar id="sidebar-1" :title="sidebar_title" shadow>
      <b-col class="flex-grow-1">
        <div v-if="is_logged_in">
          <ul class="nav nav-pills flex-column mb-auto">
            <div v-if="conversations">
              <li
                class="nav-item"
                v-for="conversation in conversations"
                :key="conversation.conversation_id"
              >
                <b-link
                  href="#"
                  @click="
                    $emit('load_conversation', conversation.conversation_id)
                  "
                  class="text-white text-decoration-none"
                  active
                >
                  <div class="nav-link active mb-2" aria-current="page">
                    <b-link
                      @click="
                        delete_conversations(conversation.conversation_id)
                      "
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
        </div>
      </b-col>
    </b-sidebar>
  </div>
</template>
<script>
import axios from "axios";
export default {
  name: "SideBar",
  data() {
    return {
      sidebar_title: "Your conversations",
      token: this.get_cookie("token"),
    };
  },
  props: {
    conversations: {
      type: Array,
    },
    user_id: {
      type: Number,
    },
    get_conversations: {
      required: true,
      type: Function,
    },
  },
  methods: {
    delete_conversations(conversation_id) {
      if (this.token) {
        const config = {
          headers: {
            Authorization: this.token,
          },
          data: {
            conversation_id: conversation_id,
          },
        };
        axios
          .delete("http://127.0.0.1:5000/delete-conversation", config)
          .then((res) => {
            if (res.status === 200) {
              this.get_conversations();
            }
          })
          .catch((err) => {
            console.log(err);
          });
      } else {
        console.log("no token");
      }
    },
  },
};
</script>
<style>
.sidebar {
  height: 100vh;
  width: 200px;
}
.input-group-text {
  width: 120px;
}
a {
  text-decoration: none !important;
}
</style>
