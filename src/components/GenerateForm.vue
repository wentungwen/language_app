<template>
  <div class="mt-3">
    <h3>Conversation Generator</h3>
    <br />
    <b-form @submit="submit_form">
      <!-- language: select -->
      <b-form-group label="I'm learning:" label-for="language-select">
        <b-form-select
          id="language-select"
          :options="language_options"
          v-model="formData.lan_code"
        >
          <p>I'm learning:</p></b-form-select
        >
      </b-form-group>
      <!-- hardness level: range -->
      <b-form-group label="Choose a hard level" label-for="level-select">
        <b-form-select
          id="level-select"
          :options="levelOptions"
          v-model="formData.level"
          placeholder="Choose a level"
        ></b-form-select>
      </b-form-group>
      <!-- sentence numbers: number -->
      <b-form-group
        :label="'How many sentences: ' + formData.sentence_num"
        label-for="sentence-num-input"
      >
        <b-form-input
          id="sentence-num-input"
          placeholder="5"
          v-model="formData.sentence_num"
          type="range"
          min="2"
          max="10"
          step="1"
        ></b-form-input>
      </b-form-group>
      <!-- topic: text input -->
      <b-form-group label="Which topic:" label-for="topic-input">
        <b-form-input
          id="topic-input"
          placeholder="topic"
          v-model="formData.topic"
          :required="true"
        ></b-form-input>
      </b-form-group>
      <!-- Submit Button -->
      <b-button
        :variant="is_loading ? 'dark w-100' : 'primary w-100'"
        @submit="submit_form"
        type="submit"
      >
        <template v-if="!is_loading">Generate!</template>
        <template v-else>
          <span class="loading-text">
            Generating <span class="ellipsis">......</span></span
          >
        </template>
      </b-button>
    </b-form>
  </div>
</template>

<script>
import axios from "axios";
import { eventBus } from "@/main";
export default {
  data() {
    return {
      is_loading: false,
      formData: {
        lan_code: "nl",
        topic: "home",
        sentence_num: 2,
        level: "A1",
      },
      language_options: [
        { value: "nl", text: "Dutch" },
        { value: "es", text: "Spanish" },
        { value: "ja", text: "Japanese" },
        { value: "fr", text: "French" },
        { value: "de", text: "German" },
        { value: "it", text: "Italian" },
        { value: "ar", text: "Arabic" },
        { value: "hi", text: "Hindi" },
        { value: "zh-TW", text: "Chinese" },
      ],
      levelOptions: ["A1", "A2", "B1", "B2"],
      generated_data: {
        topic: null,
        conversations: [],
        lan_code: null,
      },
    };
  },
  props: {
    user_id: {
      type: Number,
    },
  },
  methods: {
    generate_conversation(payload) {
      axios
        .post(
          `${process.env.VUE_APP_API_BASE_URL}/generate-conversation`,
          payload
        )
        .then((res) => {
          console.log("res", res);
          this.generated_data.conversations = res.data;
          this.generated_data.lan_code = this.formData.lan_code;
          this.generated_data.topic = this.formData.topic;
          eventBus.$emit("generated_data", this.generated_data);
          this.is_loading = false;
        })
        .catch((err) => {
          console.log(err);
        });
    },
    submit_form(evt) {
      evt.preventDefault();
      this.is_loading = true;
      this.generate_conversation(this.formData);
    },
  },
};
</script>
<style>
.loading-text {
  position: relative;
  white-space: nowrap;
}
.ellipsis {
  display: inline-block;
  overflow: hidden;
  width: 0.5rem;
  animation: ellipsis 3s infinite ease-in-out;
}

@keyframes ellipsis {
  0%,
  100% {
    width: 0;
  }
  50% {
    width: 2rem;
  }
}
</style>
