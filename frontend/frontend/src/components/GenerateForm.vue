<template>
  <div class="mt-3">
    <b-form @submit="submitForm">
      <!-- language: select -->
      <b-form-group label="I'm learning:" label-for="language-select">
        <b-form-select
          id="language-select"
          :options="language_options"
          v-model="formData.lan_code"
          >I'm learning:</b-form-select
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
      <b-button @submit="submitForm" type="submit" variant="primary w-100"
        >Generate!</b-button
      >
    </b-form>
  </div>
</template>

<script>
import axios from "axios";
import { eventBus } from "@/main";
export default {
  data() {
    return {
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
        .post(`http://127.0.0.1:5000/generate-conversation`, payload)
        .then((res) => {
          this.generated_data.conversations = JSON.parse(res.data);
          this.generated_data.lan_code = this.formData.lan_code;
          this.generated_data.topic = this.formData.topic;
          eventBus.$emit("generated_data", this.generated_data);
        })
        .catch((err) => {
          console.log(err);
        });
    },
    submitForm(evt) {
      evt.preventDefault();
      this.generate_conversation(this.formData);
    },
  },
};
</script>
