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
              v-model="current_conversation.lan_code"
              :options="language_options"
            ></b-form-select>
          </b-col>
          <b-col class="d-flex align-items-center">
            <b-form-checkbox
              class="mx-2"
              v-model="always_show_text"
              name="check-button"
              switch
            >
              hide sentences
            </b-form-checkbox>
            <b-button @click="open_modal">Edit testing sentences</b-button>
          </b-col>
        </b-row>
        <!-- questions demonstration start -->
        <b-row class="my-3">
          <!-- final score and wrong answers -->
          <b-card v-if="is_test_end">
            <h2>
              Correct:
              {{
                testing_sentence.sentences_arr.length - wrong_senteces.length
              }}
              /
              {{ testing_sentence.sentences_arr.length }}
            </h2>
            <!-- <h2>
              Correct:
              {{ wrong_senteces }}
              /
              {{ testing_sentence.sentences_arr }}
            </h2> -->
            <p v-if="wrong_senteces.length === 0">You got everyhting right!</p>
            <div v-else>
              <b>These are senteces you got wrong, time to practice:)</b>
              <ul>
                <li v-for="(sentence, idx) in wrong_senteces" :key="idx">
                  {{ sentence }}
                </li>
              </ul>
            </div>
            <div class="float-right">
              <b-button @click="test_again_btn" class="mr-2"
                >Test again</b-button
              >
              <b-button @click="next_conversation_btn" variant="primary"
                >next one</b-button
              >
            </div>
          </b-card>
          <!-- testing questions-->
          <b-card v-else>
            <p class="float-right">
              Question
              {{
                testing_sentence.sentences_arr.length -
                testing_sentence.curr_sentence_idx
              }}
              of {{ testing_sentence.sentences_arr.length }}
            </p>
            <b-button @click="play_btn" variant="primary" class="mr-2">
              <b-icon-play-fill></b-icon-play-fill>Play
            </b-button>

            <hr />
            <div class="wrapper" :style="is_blurred ? 'filter: blur(5px)' : ''">
              <h3>{{ testing_sentence.curr_sentence }}</h3>
              <p>{{ testing_sentence.translation }}</p>
            </div>
          </b-card>
        </b-row>
        <!-- questions demonstration end -->

        <!-- answer start -->
        <b-row class="my-3" v-if="!is_test_end">
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
                    class="my-2 input-answer"
                    v-if="word.trim() !== ''"
                    :ref="`word${idx}`"
                    :style="{
                      width: trim_punctuation(word).length + 6 + 'ch',
                    }"
                    :maxlength="trim_punctuation(word).length"
                    @keydown="handle_key(idx, $event)"
                  ></b-form-input>
                </div>
              </div>
            </b-form-group>
          </b-card>
        </b-row>
        <div v-show="is_last_conversation" class="my-3 alert alert-primary">
          It seems this is the last conversation, please add more in the
          generator. Enjoy your learning!
        </div>
        <!-- answer end -->
        <!-- check and next button start-->
        <b-row class="d-flex justify-content-end" v-if="!is_test_end">
          <b-button
            variant="primary"
            style="width: 100px"
            @click="check_btn"
            v-show="condition == 'check'"
            >Check</b-button
          >
          <b-button
            variant="primary"
            style="width: 100px"
            @click="next_btn"
            v-show="condition == 'next'"
            >Next</b-button
          >
        </b-row>
        <!-- check and next button end -->
        <!-- sentence editing modal start-->
        <b-modal v-model="is_modal_open" title="Practice sentences">
          <b-row class="m-3">
            <b-form-textarea
              class="w-100 h-75"
              rows="10"
              placeholder="Enter the sentences you want to practice line by line."
              v-model="edited_conversation_string"
            ></b-form-textarea>
          </b-row>
        </b-modal>
        <!-- sentence editing modal end-->
      </b-col>
    </b-row>
  </b-container>
</template>
<script>
export default {
  data() {
    return {
      is_last_conversation: false,
      is_blurred: true,
      is_modal_open: false,
      is_test_end: false,
      always_show_text: true,
      condition: "check",
      current_idx: 0,
      wrong_senteces: [],
      edited_conversation_string: "",
      default_str: "Hoe is je thuis?\nHoe is je thuis?",
      current_conversation: {
        lan_code: "nl",
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

  props: {
    get_conversations: Function,
    loaded_conversation: Object,
  },
  computed: {
    testing_sentence() {
      return this.generate_testing_sentence();
    },
  },
  watch: {
    loaded_conversation(new_conversation) {
      console.log("new_conversation", new_conversation);
      if (new_conversation) {
        this.init_test();
        this.current_conversation = new_conversation;
        this.edited_conversation_string = this.conversation_to_string(
          new_conversation.conversations
        );
      } else {
        this.is_last_conversation = this.is_test_end ? true : false;
      }
    },
    always_show_text(new_value) {
      this.is_blurred = new_value;
    },
  },
  methods: {
    generate_testing_sentence() {
      if (!this.edited_conversation_string) {
        this.edited_conversation_string = this.default_str;
      }
      const target_sentences = (this.edited_conversation_string || "")
        .split("\n")
        .filter((sentence) => sentence !== "");
      const target_sentence = target_sentences[this.current_idx];
      const target_sentence_arr = (target_sentence || "")
        .split(" ")
        .map((word) => {
          return this.trim_punctuation(word);
        })
        .filter((word) => word !== "");
      return {
        sentences_arr: target_sentences,
        curr_sentence_idx: this.current_idx,
        curr_sentence: target_sentence,
        trimmed_sentence_arr: target_sentence_arr,
      };
    },
    next_conversation_btn() {
      this.$emit(
        "to_next_conversation",
        this.current_conversation.conversation_id
      );
      console.log("this.current_conversation", this.current_conversation);
    },
    test_again_btn() {
      this.init_test();
    },
    init_test() {
      this.is_last_conversation = false;
      this.wrong_senteces = [];
      this.is_test_end = false;
      this.current_idx = 0;
      this.is_blurred = true;
      this.condition = "check";
    },
    conversation_to_string(conversations) {
      let text = "";
      conversations.forEach((conv) => {
        text += `${conv.content}\n`;
      });
      return text;
    },
    next_btn() {
      const total_num = this.testing_sentence.sentences_arr.length;
      const current = this.current_idx + 1;
      if (total_num === current) {
        this.is_test_end = true;
      } else {
        if (this.current_idx === this.current_conversation.length) {
          this.wrong_senteces = [];
        }
        document.querySelectorAll(".input-answer").forEach((input) => {
          input.style.backgroundColor = "white";
          input.value = "";
        });
        this.condition = "check";
        const sentences = this.edited_conversation_string.split("\n");
        if (this.current_idx < sentences.length - 1) {
          this.is_blurred = this.always_show_text ? true : false;
          this.current_idx += 1;
        }
        this.play_btn();
      }
    },
    check_btn() {
      this.is_blurred = false;
      this.condition = "next";
      this.is_this_question_correct = true;
      let answer_inputs_value = [];
      let is_this_question_correct = true;
      const correct_answer_value = this.testing_sentence.trimmed_sentence_arr;
      const answer_inputs = document.querySelectorAll(".input-answer");
      answer_inputs.forEach((input) => {
        answer_inputs_value.push(input.value);
      });
      for (let i = 0; i < correct_answer_value.length; i++) {
        const correct_ans = correct_answer_value[i].trim().toLowerCase();
        const input_ans = answer_inputs_value[i].trim().toLowerCase();
        if (correct_ans == input_ans) {
          answer_inputs[i].style.backgroundColor = "white";
        } else {
          answer_inputs[i].style.backgroundColor = "#ffd6d6";
          is_this_question_correct = false;
        }
      }
      if (!is_this_question_correct) {
        this.wrong_senteces.push(this.testing_sentence.curr_sentence);
      }
    },
    speak_text(text, lan_code, rate, volumn) {
      const speech_utterance = new SpeechSynthesisUtterance(text);
      speech_utterance.lang = lan_code;
      speech_utterance.rate = rate;
      speech_utterance.volume = volumn;
      window.speechSynthesis.speak(speech_utterance);
    },
    handle_key(idx, event) {
      if (event.key === "ArrowRight" || event.key === "ArrowLeft") {
        const next_idx = event.key === "ArrowRight" ? idx + 1 : idx - 1;
        const next_input = this.$refs[`word${next_idx}`]?.[0];
        if (next_input) {
          next_input.focus();
        }
      } else if (event.key === "Enter") {
        this.condition === "check" ? this.check_btn() : this.next_btn();
      }
    },
    trim_punctuation(word) {
      const punctuation_regex = /[!"#$%&()*+,\-./:;<=>?@[\]^_`{|}~]/g;
      return word.replace(punctuation_regex, "").trim();
    },
    open_modal() {
      this.is_modal_open = true;
    },
    play_btn() {
      this.speak_text(
        this.testing_sentence.curr_sentence,
        this.current_conversation.lan_code,
        this.speak_text_data.rate,
        this.speak_text_data.volumn
      );
    },
  },
  mounted() {
    this.get_conversations();
    this.init_test();
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
