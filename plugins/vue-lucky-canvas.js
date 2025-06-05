// sweetalert2 本身并不是一个 Vue 插件（Vue Plugin），而是一个独立的库，所以直接使用 nuxtApp.vueApp.use(Swal) 会报错
import { defineNuxtPlugin } from '#app'
import VueLuckyCanvas from '@lucky-canvas/vue'

export default defineNuxtPlugin(nuxtApp => {
  nuxtApp.vueApp.use(VueLuckyCanvas)
})
