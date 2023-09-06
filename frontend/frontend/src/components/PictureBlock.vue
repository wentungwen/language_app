<template>
  <div class="d-flex flex-column">
    <!-- play and stop button -->
    <b-col>
      <b-button-group
        class="mt-4 px-4 w-100"
        role="group"
        aria-label="video-control"
      >
        <b-button
          type="button"
          class="btn btn-primary"
          @click="play_slides_btn"
          :disabled="sliding"
        >
          <b-icon icon="play-fill"></b-icon> Play
        </b-button>
        <b-button
          type="button"
          class="btn-primary"
          @click="stop_slides_btn"
          :disabled="!sliding"
        >
          <b-icon icon="stop-fill"></b-icon> Stop
        </b-button>
        <b-button class="btn-primary speed-input">
          <b-form-group
            :label="'Speed: ' + speech_speed * 100"
            label-for="sentence-num-input"
            class="d-flex flex-grow-1 h-100 align-items-center"
          >
            <b-form-input
              id="sentence-num-input"
              type="range"
              :min="MIN_SPEED"
              :max="MAX_SPEED"
              :step="SPEED_INCREMENT"
              v-model="speech_speed"
              @change="adjust_speed"
            ></b-form-input>
          </b-form-group>
        </b-button>
      </b-button-group>
    </b-col>
    <!-- Alert -->
    <b-col>
      <b-alert :show="is_alert_shown" class="m-3 alert-warning"
        >It is fastest!</b-alert
      >
    </b-col>
    <!-- Text slides with image -->
    <b-col>
      <b-carousel
        fade
        controls
        indicators
        v-model="current_slide"
        :interval="slides_speed"
        background="#ababab"
        class="pic-carousel"
      >
        <b-carousel-slide
          v-for="(conversation, idx) in received_data.conversations"
          :text="conversation.content"
          :key="idx"
          :current_slide="idx"
          :img-src="slide_image(conversation.sender)"
        ></b-carousel-slide>
      </b-carousel>
    </b-col>
  </div>
</template>

<script>
import { eventBus } from "@/main";
export default {
  data() {
    return {
      MIN_SPEED: 0.5,
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
  methods: {
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
  },
  mounted() {
    eventBus.$on("received_data", (data) => {
      this.received_data = data;
    });
  },
};
</script>
<style>
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
</style>
