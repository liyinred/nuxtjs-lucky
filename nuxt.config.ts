// https://nuxt.com/docs/api/configuration/nuxt-config
import tailwindcss from "@tailwindcss/vite";
export default defineNuxtConfig({
  compatibilityDate: "2024-11-01",
  devtools: { enabled: false },
  ssr: true,

  app: {
    head: {
      title: "MSBIO",
      // link: [{ rel: "icon", type: "image/x-icon", href: "/logo.ico" }],
    },
    pageTransition: { name: "page", mode: "out-in" },
  },

  devServer: {
    host: "0.0.0.0",
    port: 3000,
  },

  css: [
    // 引入全局 CSS 文件
    "~/assets/css/global.css",
    "~/assets/css/tailwindcss.css",
  ],

  routeRules: {
    // '/': { redirect: 'https://msbiox.com/' },
    "/": { redirect: "/lucky" },
  },
  // plugins: ["~/plugins/vue-lucky-canvas.js"],
  vite: {
    plugins: [tailwindcss()],
  },

  modules: ["@nuxtjs/i18n"],
  i18n: {
    vueI18n: "./i18n.config.ts", // if you are using custom path, default
  },
});
