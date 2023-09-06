<template>
  <div>
    <b-row class="mb-3">
      <b-card class="d-flex flex-row">
        <!-- play and stop button -->
        <b-col cols="auto"> </b-col>
        <b-col class="col">
          <b-button-group
            role="group"
            aria-label="video-control"
            size="lg"
            class="button-group-fill align-items-center"
          >
            <b-button
              type="button"
              class="btn-dark"
              :disabled="sliding"
              @click="play_slides_btn"
            >
              <b-icon-play-fill></b-icon-play-fill> Play
            </b-button>
            <b-button
              type="button"
              class="btn-primary"
              :disabled="!sliding"
              @click="stop_slides_btn"
            >
              <b-icon-stop-fill></b-icon-stop-fill> Stop
            </b-button>
            <b-button class="d-flex">
              <span class="w-50"> Speed {{ speech_speed * 100 }}</span>

              <b-form-input
                id="sentence-num-input"
                class="ml-1"
                type="range"
                :min="MIN_SPEED"
                :max="MAX_SPEED"
                :step="SPEED_INCREMENT"
                v-model="speech_speed"
                @change="adjust_speed"
              ></b-form-input>
            </b-button>
          </b-button-group>
          <!-- Alert -->
          <b-alert :show="is_alert_shown" class="m-3 alert-warning"
            >It is fastest!</b-alert
          >
        </b-col>
      </b-card>
    </b-row>
    <b-row>
      <!-- action alerts -->
      <b-alert :show="is_copied" class="m-3 alert-success">Copied!</b-alert>
      <b-alert :show="is_saved" class="m-3 alert-success">Saved!</b-alert>
      <b-card class="mb-3 content-card">
        <b-col cols="12" class="d-flex justify-content-between mb-3">
          <!-- txt and pic view switch  -->
          <b-button-toolbar>
            <b-button-group role="group" aria-label="view-control" class="">
              <b-button
                type="button"
                :class="is_carousel_shown ? '' : 'btn-dark'"
                @click="is_carousel_shown = false"
              >
                <b-icon-chat-dots-fill></b-icon-chat-dots-fill> txt
              </b-button>
              <b-button
                type="button"
                :class="is_carousel_shown ? 'btn-dark' : ''"
                @click="is_carousel_shown = true"
              >
                <b-icon-image-fill></b-icon-image-fill> pic
              </b-button>
            </b-button-group>
          </b-button-toolbar>

          <!-- conversation button group block -->
          <Transition name="slide-fade">
            <b-button-toolbar v-if="!is_carousel_shown">
              <b-button-group role="group" class="btn-group">
                <b-button
                  variant="secondary"
                  :disabled="is_editing"
                  @click="translate_btn(received_data)"
                >
                  <b-icon-translate></b-icon-translate>
                  Translate</b-button
                >
                <b-button
                  variant="secondary"
                  :disabled="is_editing"
                  @click="copy_btn"
                  ><b-icon-clipboard></b-icon-clipboard> Copy</b-button
                >
                <b-button @click="edit_btn" variant="secondary">
                  <b-icon-pen></b-icon-pen> Edit</b-button
                >
                <b-button
                  variant="secondary"
                  :disabled="is_editing"
                  @click="save_btn"
                  v-if="is_logged_in"
                  ><b-icon-check-circle></b-icon-check-circle> Save</b-button
                >
              </b-button-group>
            </b-button-toolbar>
          </Transition>
        </b-col>
        <hr />
        <!-- conversation editing block -->
        <Transition name="slide-fade">
          <b-col cols="12" v-if="!is_carousel_shown">
            <div v-if="is_editing">
              <p
                class="d-flex justify-content-center align-items-center"
                v-for="(msg, idx) in edited_conversations"
                :key="idx"
              >
                <b class="mr-3">{{ msg.sender }}</b>

                <b-form-input
                  id="topic-input"
                  v-model="msg.content"
                  :required="true"
                ></b-form-input>
              </p>
              <b-button variant="secondary" @click="edit_submit_btn"
                >Save</b-button
              >
            </div>
            <div v-else ref="copy_conversations">
              <div v-if="is_translation_shown && translated_conversations">
                <p
                  v-for="(msg, idx) in translated_conversations.conversations"
                  :key="idx"
                >
                  <b-badge variant="info mr-1">{{ msg.sender }}</b-badge>
                  {{ msg.content }}
                </p>
                <!-- <b-button
                  type="button"
                  variant="outline-dark"
                  @click="keep_generate_btn"
                >
                  Keep Generating 5 sentencesss
                </b-button> -->
              </div>
              <div v-else-if="received_data && received_data.conversations">
                <p v-for="(msg, idx) in received_data.conversations" :key="idx">
                  <b-badge variant="info mr-1">{{ msg.sender }}</b-badge>
                  {{ msg.content }}
                </p>
                <b-button
                  type="button"
                  variant="outline-primary"
                  @click="keep_generate_btn"
                  class="w-100 my-2"
                >
                  Keep Generating 5 sentencesss
                </b-button>
              </div>
              <div
                v-else-if="
                  loaded_conversation && loaded_conversation.conversations
                "
              >
                <p
                  v-for="(msg, idx) in loaded_conversation.conversations"
                  :key="idx"
                >
                  <b-badge variant="info mr-1">{{ msg.sender }}</b-badge>
                  {{ msg.content }}
                </p>
                <b-button
                  type="button"
                  variant="outline-dark"
                  @click="keep_generate_btn"
                >
                  Keep Generating 5 sentencesss
                </b-button>
              </div>
              <div v-else>
                <p class="text-secondary">Please generate conversations</p>
              </div>
            </div>
            <!-- <div v-else ref="copy_conversations">
            <div v-if="is_translation_shown">
              <p
                v-for="(msg, idx) in translated_conversations.conversations"
                :key="idx"
              >
                <b-badge variant="info mr-1">{{ msg.sender }}</b-badge>
                {{ msg.content }}
              </p>
            </div>
            <div v-else>
              <div v-if="received_data">
                <p v-for="(msg, idx) in received_data.conversations" :key="idx">
                  <b-badge variant="info mr-1">{{ msg.sender }}</b-badge>
                  {{ msg.content }}
                </p>
              </div>
              <div v-else-if="this.loaded_conversation">
                <p
                  v-for="(msg, idx) in loaded_conversation.conversations"
                  :key="idx"
                >
                  <b-badge variant="info mr-1">{{ msg.sender }}</b-badge>
                  {{ msg.content }}
                </p>
              </div>
              <div v-else>
                <p class="text-secondary">Please generate conversations</p>
              </div>
            </div>
          </div> -->
          </b-col>
        </Transition>
        <!-- conversation end -->
        <!-- carousel block start -->
        <Transition name="slide-fade">
          <b-carousel
            class="pic-carousel"
            fade
            controls
            indicators
            v-model="current_slide"
            :interval="slides_speed"
            v-show="is_carousel_shown"
          >
            <b-carousel-slide
              v-for="(conversation, idx) in received_data.conversations"
              :text="conversation.content"
              :key="idx"
              :current_slide="idx"
              :img-src="slide_image(conversation.sender)"
            ></b-carousel-slide>
          </b-carousel>
        </Transition>
        <!-- picture block end -->
      </b-card>
    </b-row>
  </div>
</template>

<script>
import { eventBus } from "@/main";
import axios from "axios";
export default {
  data() {
    return {
      is_carousel_shown: false,
      // conversation
      is_logged_in: false,
      is_copied: false,
      is_saved: false,
      is_translation_shown: false,
      is_editing: false,
      translate_to_lan_code: "en",
      edited_conversations: [],
      translated_conversations: [],
      // picture block
      MIN_SPEED: 0.6,
      MAX_SPEED: 1.0,
      SPEED_INCREMENT: 0.05,
      volumn: 100,
      speech_speed: 0.8,
      speech_utterance: null,
      current_slide: 0,
      slides_speed: 0,
      sliding: false,
      is_alert_shown: false,
      slide_imgs: {
        A: require("../assets/person_a.png"),
        B: require("../assets/person_b.png"),
      },
      received_data: {
        lan_code: "nl",
        translated_conversations: [],
        conversations: [
          {
            content: "het meisje.",
            sender: "A",
          },
          {
            content: "Volgens de man.",
            sender: "B",
          },
          {
            content: "2. het meisje is klein.",
            sender: "A",
          },
          {
            content: "2. Volgens de man is grote.",
            sender: "B",
          },
        ],
      },
    };
  },
  props: {
    conversation: {
      type: Object,
    },
    loaded_conversation: {
      type: Object,
    },
  },
  methods: {
    keep_generate_btn() {
      console.log("clicked");
    },
    // picture block
    adjust_speed(request) {
      this.is_alert_shown = false;
      if (request === "slower") {
        if (this.speech_speed > this.MIN_SPEED) {
          this.speech_speed -= this.SPEED_INCREMENT;
        } else {
          this.is_alert_shown = true;
          setTimeout(() => {
            this.is_alert_shown = false;
          }, 2000);
        }
      } else if (request === "faster") {
        if (this.speech_speed < this.MAX_SPEED) {
          this.speech_speed += this.SPEED_INCREMENT;
        } else {
          this.is_alert_shown = true;
          setTimeout(() => {
            this.is_alert_shown = false;
          }, 2000);
        }
      }
    },
    async play_slides_btn() {
      this.current_slide = 0;
      this.sliding = true;
      for (
        let i = this.current_slide;
        i < this.received_data.conversations.length;
        i++
      ) {
        if (this.sliding) {
          await this.play_one_slide(i);
          this.current_slide++;
        } else {
          this.current_slide = 0;
          break;
        }
      }
      this.sliding = false;
    },

    async play_one_slide(i) {
      const current_content = this.received_data.conversations[i].content;
      const lan_code = this.received_data.lan_code;
      const speech_speed = this.speech_speed;
      const speech_time = this.calculate_speech_time(current_content, lan_code);
      const speech_volumn = this.volumn;
      this.speak_text(current_content, lan_code, speech_speed, speech_volumn);
      // Wait for the speech to finish
      await new Promise((resolve) => {
        setTimeout(() => {
          resolve();
        }, speech_time);
      });
    },

    calculate_speech_time(content, lan_code) {
      let characters_per_second = 7.5;
      if (lan_code === "ja") {
        characters_per_second = 4;
      }
      const speech_time = (content.length / characters_per_second) * 1000;
      return speech_time;
    },

    stop_slides_btn() {
      this.current_slide = 0;
      this.sliding = false;
      window.speechSynthesis.cancel();
    },
    speak_text(text, languageCode, rate, volumn) {
      const speech_utterance = new SpeechSynthesisUtterance(text);
      speech_utterance.lang = languageCode;
      speech_utterance.rate = rate;
      speech_utterance.volume = volumn;
      window.speechSynthesis.speak(speech_utterance);
    },
    // conversation
    save_btn() {
      const token = localStorage.getItem("token");
      const config = {
        headers: {
          Authorization: token,
        },
      };
      const payload = {
        data: this.received_data,
      };
      axios
        .post("http://127.0.0.1:5000/save", payload, config)
        .then((res) => {
          if (res.status === 200) {
            this.is_saved = true;
            this.$emit("save_btn_clicked");
            setTimeout(() => {
              this.is_saved = false;
            }, 2000);
          }
        })
        .catch((err) => {
          console.log(err);
        });
    },
    edit_btn() {
      this.edited_conversations = this.received_data.conversations;
      this.is_editing = true;
    },
    edit_submit_btn() {
      this.received_data.conversations = this.edited_conversations;
      this.is_editing = false;
      this.is_translation_shown = false;
      this.translated_conversations = [];
    },
    translate_btn(received_data) {
      const lan_code = received_data.lan_code;
      const conversations = received_data.conversations;
      const translate_to_lan_code = this.translate_to_lan_code;

      const payload = {
        lan_code,
        conversations,
        translate_to_lan_code,
      };
      axios
        .post("http://127.0.0.1:5000/translate", payload)
        .then((res) => {
          this.is_translation_shown = !this.is_translation_shown;
          this.translated_conversations = res.data;
        })
        .catch((err) => {
          console.log(err);
        });
    },
    copy_btn() {
      const conversationsDiv = this.$refs.copy_conversations;
      const range = document.createRange();
      range.selectNode(conversationsDiv);

      const selection = window.getSelection();
      selection.removeAllRanges();
      selection.addRange(range);

      document.execCommand("copy");
      selection.removeAllRanges();
      this.is_copied = true;
      setTimeout(() => {
        this.is_copied = false;
      }, 2000);
    },
  },
  computed: {
    slide_image() {
      return (sender) => {
        return this.slide_imgs[sender];
      };
    },
  },
  watch: {
    current_slide(slide) {
      if (slide == this.received_data.conversations.length) {
        this.current_slide = 0;
      }
    },
    loaded_conversation(loaded_data) {
      if (loaded_data) {
        this.received_data = loaded_data;
        eventBus.$emit("received_data", this.received_data);
      }
    },
  },
  mounted() {
    eventBus.$on("received_data", (data) => {
      this.received_data = data;
    });
    eventBus.$on("generated_data", (data) => {
      if (data) {
        this.received_data = data;
        this.received_data.translated_conversations =
          this.translated_conversations;

        eventBus.$emit("received_data", this.received_data);
        this.translated_conversations = [];
        this.edited_conversations = [];
        this.is_editing = false;
      }
    });
  },
  created() {
    if (localStorage.getItem("token")) {
      this.is_logged_in = true;
    }
  },
};
</script>

<style scoped>
.toolbar-section {
  min-height: 200px;
}
.toolbar {
  display: flex;
  justify-content: space-between;
  padding: 10px;
  border-bottom: 1px solid #ccc;
}
.button-group-fill {
  width: 100%;
}
.pic-carousel {
  width: 90%;
  font-size: 1.5rem;
  text-shadow: 1px 1px 2px #333;
  margin: 20px auto;
  border-radius: 1rem;
}
.carousel-caption {
  background: #0000008f;
  border-radius: 1rem;
  font-size: 1.5rem;
  right: 3% !important;
  left: 3% !important;
  padding: 10px !important;
}
.speed-input label {
  margin-right: 1rem;
}

.slide-fade-enter-active {
  transition: all 0.3s ease-out;
}

.slide-fade-leave-active {
  transition: all 0.2s cubic-bezier(1, 0.5, 0.8, 1);
}

.slide-fade-enter-from,
.slide-fade-leave-to {
  transform: translateX(20px);
  opacity: 0;
}
.content-card {
  min-height: 450px;
}
</style>
