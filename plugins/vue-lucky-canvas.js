import { defineNuxtPlugin } from '#app'
import VueLuckyCanvas from '@lucky-canvas/vue'

export default defineNuxtPlugin(nuxtApp => {
  nuxtApp.vueApp.use(VueLuckyCanvas)
})
