import { defineNuxtConfig } from "nuxt/config";
import lara from "@primevue/themes/lara";
export default defineNuxtConfig({
  modules: ["@primevue/nuxt-module"],
  primevue: {
    options: {
      theme: {
        preset: lara,
      },
    },
  },
});
