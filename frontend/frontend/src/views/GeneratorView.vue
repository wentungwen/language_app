<template>
  <div>
    <b-row class="justify-content-center">
      <b-col class="generate-form col-12 col-md-3 mb-3">
        <b-card> <GenerateForm :user_id="user_id" /></b-card>
      </b-col>
      <b-col class="picture-block col-12 col-md">
        <ConversationBlock
          :loaded_conversation="computed_loaded_conversation"
          :conversation="conversations[active_conversation]"
          @save_btn_clicked="get_conversations"
        />
      </b-col>
    </b-row>
  </div>
</template>
<script>
import GenerateForm from "@/components/GenerateForm.vue";
import ConversationBlock from "@/components/ConversationBlock.vue";
import { eventBus } from "@/main";

export default {
  components: {
    GenerateForm,
    ConversationBlock,
  },
  data() {
    return {
      user_id: null,
      username: null,
      loading: false,
      active_conversation: 1,
      conversations: [],
      local_loaded_conversation: null,
    };
  },
  props: {
    get_conversations: Function,
    loaded_conversation: Object,
  },
  computed: {
    computed_loaded_conversation: function () {
      if (this.local_loaded_conversation) {
        return this.local_loaded_conversation;
      } else {
        return this.loaded_conversation;
      }
    },
  },
  methods: {
    save_btn_clicked() {
      this.get_conversations();
    },
  },
  mounted() {
    this.get_conversations();
    eventBus.$on("generated_data", (data) => {
      this.local_loaded_conversation = data;
    });
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
.generate-form {
  max-width: 700px;
}
</style>
