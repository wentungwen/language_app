<template>
  <div>
    <b-row class="justify-content-center">
      <b-col class="generate-form" cols="3">
        <b-card> <GenerateForm :user_id="user_id" /></b-card>
      </b-col>
      <b-col class="picture-block">
        <!-- <b-card class="mt-2"> -->
        <ConversationBlock
          :loaded_conversation="loaded_conversation"
          :conversation="conversations[active_conversation]"
          @save_btn_clicked="get_conversations"
        />
        <!-- </b-card> -->
        <!-- <b-card> <PictureBlock /></b-card> -->
      </b-col>
    </b-row>
  </div>
</template>
<script>
import GenerateForm from "@/components/GenerateForm.vue";
import ConversationBlock from "@/components/ConversationBlock.vue";
// import PictureBlock from "@/components/PictureBlock.vue";

export default {
  components: {
    GenerateForm,
    ConversationBlock,
    // PictureBlock,
  },
  data() {
    return {
      user_id: null,
      username: null,
      loading: false,
      active_conversation: 1,
      conversations: [],
    };
  },
  props: {
    get_conversations: Function,
    loaded_conversation: Object,
  },
  methods: {
    save_btn_clicked() {
      this.get_conversations();
    },
  },
  mounted() {
    this.get_conversations();
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
