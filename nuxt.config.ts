// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: "2024-11-01",
  devtools: { enabled: false },
  ssr: true,

  app: {
    head: {
      title: "MSBIO",
      link: [{ rel: "icon", href: "/favicon.ico" }],
    },
    pageTransition: { name: "page", mode: "out-in" },
  },

  devServer: {
    host: "0.0.0.0",
    port: 3000,
  },

  css: ["~/assets/css/global.css"],

  routeRules: {
    // '/': { redirect: 'https://msbiox.com/' },
    "/": { redirect: "/lucky" },
  },
  // plugins: ["~/plugins/vue-lucky-canvas.js"],

  modules: ["@nuxtjs/i18n", "@nuxtjs/tailwindcss"],
  i18n: {
    vueI18n: "./i18n.config.ts", // if you are using custom path, default
    bundle: {
      optimizeTranslationDirective: false,
    },
  },
});
