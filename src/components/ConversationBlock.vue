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
            size="md"
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
        </b-col>
      </b-card>
    </b-row>
    <b-row>
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
          <!-- Alert -->
          <b-alert :show="is_alert_shown" class="m-3 alert-warning"
            >It is fastest!</b-alert
          >
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
        <!-- action alerts -->
        <b-alert :show="is_copied" class="m-3 alert-success">Copied!</b-alert>
        <b-alert :show="is_saved" class="m-3 alert-success">Saved!</b-alert>
        <b-alert
          :show="is_translating && !received_data.translated_conversations"
          class="m-3 alert-primary"
          >Translating...</b-alert
        >

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
              <div
                v-if="
                  is_translation_shown && received_data.translated_conversations
                "
              >
                <p
                  v-for="(msg, idx) in received_data.translated_conversations
                    .conversations"
                  :key="idx"
                >
                  <b-badge variant="info mr-1">{{ msg.sender }}</b-badge>
                  {{ msg.content }}
                </p>
              </div>
              <div
                v-else-if="
                  received_data && received_data.conversations.length > 0
                "
              >
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
                  <template v-if="!is_loading"
                    >Keep Generating sentences!</template
                  >
                  <template v-else>
                    <span class="loading-text">
                      Generating <span class="ellipsis">......</span></span
                    >
                  </template>
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
                  variant="outline-primary"
                  @click="keep_generate_btn"
                  class="w-100 my-2"
                >
                  <template v-if="!is_loading"
                    >Keep Generating sentences!</template
                  >
                  <template v-else>
                    <span class="loading-text">
                      Generating <span class="ellipsis">......</span></span
                    >
                  </template>
                </b-button>
              </div>
              <div v-else>
                <p class="text-secondary">Please generate conversations</p>
              </div>
            </div>
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
        <!-- carousel block end -->
      </b-card>
    </b-row>
  </div>
</template>

<script>
import { eventBus } from "@/main";
import { translate_conversations } from "@/utils/translateUtil";
import axios from "axios";

export default {
  data() {
    return {
      is_loading: false,
      is_carousel_shown: false,
      // conversation
      is_copied: false,
      is_saved: false,
      is_translating: false,
      is_translation_shown: false,
      is_editing: false,
      edited_conversations: [],
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
      // conversation editing
      received_data: {
        lan_code: "nl",
        translated_conversations: [],
        topic: "defaults",
        conversations: [],
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
      this.is_loading = true;
      const payload = {
        conversations: this.received_data.conversations.slice(-2),
        lan_code: this.received_data.lan_code,
        topic: this.received_data.topic,
      };
      console.log(payload);
      axios
        .post(`${process.env.VUE_APP_API_BASE_URL}/generate-five`, payload)
        .then((res) => {
          const new_conversation_arr = res.data;
          new_conversation_arr.forEach((conv) => {
            this.received_data.conversations.push(conv);
          });
          this.is_loading = false;
        })
        .catch((err) => {
          console.log(err);
        });
      this.received_data.translated_conversations = NaN;
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
          const current_content = this.received_data.conversations[i].content;
          const lan_code = this.received_data.lan_code;
          const speech_speed = this.speech_speed;
          const speech_volumn = this.volumn;

          await this.speak_text(
            current_content,
            lan_code,
            speech_speed,
            speech_volumn
          );

          this.current_slide++;
        } else {
          this.current_slide = 0;
          break;
        }
      }
      this.sliding = false;
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
      speech_utterance.addEventListener("end", () => {});
      return new Promise((resolve) => {
        speech_utterance.addEventListener("end", resolve);
        window.speechSynthesis.speak(speech_utterance);
      });
    },
    // conversation
    save_btn() {
      const token = this.get_cookie("token");
      const config = {
        headers: {
          Authorization: token,
        },
      };
      const payload = {
        data: this.received_data,
      };
      axios
        .post(`${process.env.VUE_APP_API_BASE_URL}/save`, payload, config)
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
      this.received_data.translated_conversations = NaN;
      // TODO: figure out NaN
    },
    async translate_btn(received_data) {
      // TODO: think about optimising it
      if (
        !this.received_data.translated_conversations ||
        this.received_data.translated_conversations.length == 0
      ) {
        this.is_translating = true;
        const lan_code = received_data.lan_code;
        const conversations = received_data.conversations;
        const res = await translate_conversations(lan_code, conversations);
        console.log("res", res);
        this.received_data.translated_conversations = res;
        this.is_translating = !this.is_translating;
      }
      this.is_translation_shown = !this.is_translation_shown;
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
