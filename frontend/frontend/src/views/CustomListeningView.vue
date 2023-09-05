<template>
  <b-container class="custom-listening-container">
    <b-row class="justify-content-center mx-2">
      <b-col cols="10">
        <b-row>
          <h2>Custom listening test</h2>
        </b-row>
        <b-row>
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
              v-model="always_show_text"
              name="check-button"
              switch
            >
              hide sentences
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
              <h3>{{ testing_sentence.sentence }}</h3>
              <p>{{ testing_sentence.translation }}</p>
            </div>
          </b-card>
        </b-row>
        <!-- answer -->
        <b-row>
          <b-card class="mt-3">
            <b-form-group>
              <h4>Answer</h4>
              <div class="d-flex flex-wrap">
                <div
                  class="d-flex mr-2"
                  v-for="(word, idx) in testing_sentence.trimmed_sentence_arr"
                  :key="idx"
                >
                  <b-form-input
                    class="my-2"
                    v-if="word.trim() !== ''"
                    :ref="`word${idx}`"
                    :style="{
                      width: trim_punctuation(word).length + 6 + 'ch',
                    }"
                    :maxlength="trim_punctuation(word).length"
                    @keydown="handle_keydown(idx, $event)"
                  ></b-form-input>
                </div>
              </div>
            </b-form-group>
          </b-card>
        </b-row>
        <br />
        <b-row class="d-flex justify-content-end">
          <b-button
            variant="primary"
            style="width: 100px"
            @click="show_btn"
            v-show="condition == 'show'"
            >Show</b-button
          >
          <b-button
            variant="primary"
            style="width: 100px"
            @click="next_btn"
            v-show="condition == 'next'"
            >Next</b-button
          >
        </b-row>

        <!-- sentence editing modal -->
        <b-modal v-model="is_modal_open" title="Practice sentences">
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
      condition: "show",
      always_show_text: true,
      is_blurred: true,
      is_important: false,
      is_random: false,
      is_modal_open: false,
      current_idx: 0,
      all_sentences_text:
        "Mijn zus heeft vanochtend een auto gekocht. \nDe kat heeft in de zon gelegen. \nWaar hebben jullie vanavond gegeten? \n Wie heb je in het park gezien?\nWij zijn vandaag thuis gebleven ",
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
      speak_text_data: {
        rate: 0.8,
        volumn: 100,
      },
    };
  },
  methods: {
    next_btn() {
      this.condition = "show";
      console.log(this.condition);
      const sentences = this.all_sentences_text.split("\n");
      if (this.current_idx < sentences.length - 1) {
        this.is_blurred = this.always_show_text ? true : false;
        this.current_idx += 1;
      } else {
        console.log("end");
      }
    },
    show_btn() {
      this.is_blurred = false;
      this.condition = "next";
      console.log(this.condition);
    },
    speak_text(text, lan_code, rate, volumn) {
      const speech_utterance = new SpeechSynthesisUtterance(text);
      speech_utterance.lang = lan_code;
      speech_utterance.rate = rate;
      speech_utterance.volume = volumn;
      window.speechSynthesis.speak(speech_utterance);
    },
    handle_keydown(idx, event) {
      if (event.key === "ArrowRight" || event.key === "ArrowLeft") {
        const nextIdx = event.key === "ArrowRight" ? idx + 1 : idx - 1;
        const nextInput = this.$refs[`word${nextIdx}`]?.[0];
        if (nextInput) {
          nextInput.focus();
        }
      }
    },
    trim_punctuation(word) {
      const punctuationRegex = /[!"#$%&()*+,\-./:;<=>?@[\]^_`{|}~]/g;
      return word.replace(punctuationRegex, "");
    },
    // sentences_submit() {
    //   console.log(this.all_sentences_array);
    // },
    openModal() {
      this.is_modal_open = true;
    },
    play_btn() {
      this.speak_text(
        this.testing_sentence.sentence,
        this.form_data.lan_code,
        this.speak_text_data.rate,
        this.speak_text_data.volumn
      );
    },
  },
  computed: {
    testing_sentence() {
      const target_sentence = this.all_sentences_text
        .split("\n")
        .filter((sentence) => sentence !== "")[this.current_idx];
      const target_sentence_arr = target_sentence
        .split(" ")
        .map((word) => {
          return this.trim_punctuation(word);
        })
        .filter((word) => word !== "");
      return {
        sentence: target_sentence,
        trimmed_sentence_arr: target_sentence_arr,
        translation: "translation",
      };
    },
  },
  watch: {
    always_show_text(new_value) {
      this.is_blurred = new_value;
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
