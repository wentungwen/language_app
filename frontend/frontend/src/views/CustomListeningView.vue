<template>
  <b-container class="custom-listening-container">
    <b-row class="justify-content-center mx-2">
      <b-col cols="10">
        <b-row>
          <h2>Custom listening test</h2>
          <b-col cols="3">
            <b-form-select
              v-model="form_data.lan_code"
              :options="language_options"
            ></b-form-select>
          </b-col>
          <b-col class="d-flex align-items-center">
            <b-button @click="openModal">Edit testing sentences</b-button>

            <b-form-checkbox
              class="ml-2"
              v-model="is_random"
              name="check-button"
              switch
            >
              random
            </b-form-checkbox>
            <b-form-checkbox
              class="ml-2"
              v-model="is_sentence_shown"
              name="check-button"
              switch
            >
              show sentences
            </b-form-checkbox>
          </b-col>
        </b-row>
        <!-- save as hard sentence -->
        <b-row>
          <b-card class="mt-3">
            <b-button @click="play_btn" variant="primary" class="mr-2">
              <b-icon-play-fill></b-icon-play-fill>Play (space)
            </b-button>
            <b-button
              @click="is_important = !is_important"
              :class="is_important ? 'btn-primary' : 'btn-secondary'"
            >
              <b-icon-star v-if="!is_important"></b-icon-star>
              <b-icon-star-fill v-else></b-icon-star-fill>
              Save as Hard sentence
            </b-button>
            <hr />
            <div class="wrapper" :style="is_blurred ? 'filter: blur(5px)' : ''">
              <h3>{{ tested_sentence.sentence }}</h3>
              <p>{{ tested_sentence.translation }}</p>
            </div>
          </b-card>
        </b-row>
        <!-- answer -->
        <b-row>
          <b-card class="mt-3">
            <b-form-group>
              <h4>Answer</h4>
              <div class="d-flex">
                <div
                  class="d-flex mr-2"
                  v-for="(word, idx) in tested_sentence.sentence.split(' ')"
                  :key="idx"
                >
                  <b-form-input
                    :style="{ width: word.length + 6 + 'ch' }"
                    :maxlength="word.length"
                  ></b-form-input>
                </div>
              </div>
            </b-form-group>
          </b-card>
        </b-row>
        <br />
        <b-row class="d-flex justify-content-end">
          <b-button variant="primary" style="width: 100px">Show</b-button>
        </b-row>

        <!-- sentence editing modal -->
        <b-modal
          v-model="is_modal_open"
          title="Practice sentences"
          @ok="sentences_submit"
        >
          <b-row class="m-3">
            <b-form-textarea
              class="w-100 h-75"
              rows="10"
              placeholder="Enter the sentences you want to practice line by line."
              v-model="all_sentences_text"
            ></b-form-textarea>
          </b-row>
        </b-modal>
      </b-col>
    </b-row>
  </b-container>
</template>
<script>
export default {
  data() {
    return {
      is_blurred: false,
      is_important: false,
      is_random: false,
      is_sentence_shown: false,
      is_modal_open: false,
      all_sentences_text:
        "Waarom bent u met de bus gekomen? \nHello, hebben jullie naar het museum geweest?",
      form_data: {
        lan_code: "nl",
        level: null,
        sentence_num: null,
        topic: null,
      },
      language_options: [
        { value: "nl", text: "Dutch" },
        { value: "es", text: "Spanish" },
        { value: "ja", text: "Japanese" },
      ],
    };
  },
  methods: {
    sentences_submit() {
      // this.all_sentences_array = this.all_sentences_text
      //   .split("\n")
      //   .filter((sentence) => sentence !== "");
      console.log(this.all_sentences_array);
    },
    openModal() {
      this.is_modal_open = true;
    },
    play_btn() {},
  },
  computed: {
    tested_sentence() {
      return {
        sentence: this.all_sentences_array[0],
        translation: this.all_sentences_array[0],
      };
    },
    all_sentences_array() {
      return this.all_sentences_text
        .split("\n")
        .filter((sentence) => sentence !== "");
    },
  },
};
</script>
<style scoped>
.form-control {
  width: auto;
}
input {
  text-align: center;
}
.custom-listening-container {
  height: 100%;
}
</style>
