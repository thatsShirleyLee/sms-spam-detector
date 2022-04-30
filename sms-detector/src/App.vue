<template>
  <v-app>
    <div style="background-color: #1976D2">
      <div 
        class="d-flex align-center"
        style="color: #ffffff; justify-content: center">
        <h1 class="display-2 font-weight-bold mb-3">Spam or Ham</h1>
        <v-img
          alt="Detector Logo"
          class="shrink mr-2"
          contain
          src="src/logo.png"
          transition="scale-transition"
          height="15vh"
          width="35vh"
        />
        <h1 class="display-2 font-weight-bold mb-3">SMS Detector</h1>
      </div>
    </div>
    <v-main>
      <MainBody/>
    </v-main>
  </v-app>
</template>

<script>
import MainBody from './components/MainBody';

export default {
  name: 'App',

  components: {
    MainBody,
  },

  data: () => ({
    //
  }),
};
</script>
