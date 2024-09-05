import { defineNuxtConfig } from "nuxt/config";
import lara from "@primevue/themes/lara";

export default defineNuxtConfig({
  css: ["./assets/css/tailwind.css", "primeicons/primeicons.css"],
  modules: ["@primevue/nuxt-module"],
  primevue: {
    options: {
      theme: {
        preset: lara,
      },
    },
  },
});
