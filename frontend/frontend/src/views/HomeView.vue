<template>
  <b-row>
    <b-col class="col-4">
      <GenerateForm :user_id="user_id" />
      <ConversationBlock
        :loaded_conversation="loaded_conversation"
        :conversation="conversations[active_conversation]"
        @save_btn_clicked="get_conversations"
      />
    </b-col>
    <b-col class="col picture-block">
      <PictureBlock />
    </b-col>
  </b-row>
</template>
<script>
import GenerateForm from "@/components/GenerateForm.vue";
import ConversationBlock from "@/components/ConversationBlock.vue";
import PictureBlock from "@/components/PictureBlock.vue";

export default {
  components: {
    GenerateForm,
    ConversationBlock,
    PictureBlock,
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
</style>
