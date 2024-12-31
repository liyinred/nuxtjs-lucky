// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: "2024-11-01",
  devtools: { enabled: true },
  ssr: true,
  app: {
    head: {
      title: "MSBIO",
      link: [{ rel: "icon", type: "image/x-icon", href: "/logo.ico" }],
    },
    pageTransition: { name: 'page', mode: 'out-in' }
  },
  devServer: {
    host: "0.0.0.0",
    port: 3000,
  },
  routeRules: {
    '/': { redirect: 'https://msbiox.com/' },
  },
  plugins: ["~/plugins/vue-lucky-canvas.js"],
});
