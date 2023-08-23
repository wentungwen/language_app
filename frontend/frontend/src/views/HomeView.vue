<template>
  <main class="home">
    <b-row>
      <b-col md="2"> </b-col>
      <b-col md="10">
        <b-container fluid>
          <b-row>
            <b-col cols="4">
              <div class="bg-secondary">Content for Section 2 here --</div>
            </b-col>

            <b-col cols="8">
              <div class="bg-secondary">! Content for Section 3 here -</div>
            </b-col>
          </b-row>
        </b-container>
      </b-col>
    </b-row>
  </main>
</template>

<script>
export default {
  name: "HomeView",
  components: {},
  data() {
    return {
      mainProps: {
        // blank: false,
        // blankColor: "#777",
        width: 75,
        height: 75,
        class: "m2",
      },
    };
  },
};
</script>
