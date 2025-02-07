<!-- <template>
  <div>
    <NuxtRouteAnnouncer />
    <NuxtWelcome />
  </div>
</template> -->

<template>
  <NuxtPage />
</template>

<style>
.page-enter-active,
.page-leave-active {
  transition: all 0.4s;
}

.page-enter-from,
.page-leave-to {
  opacity: 0;
  filter: blur(1rem);
}
</style>

<!-- <script setup>
import { onMounted } from 'vue'

const { setLocale } = useI18n()

// 在组件挂载时自动设置语言
onMounted(() => {
  const browserLanguage = navigator.language || 'en'
  console.log(browserLanguage)

  let locale = 'en'

  if (browserLanguage.includes('zh')) {
    locale = 'cn'
  } else if (browserLanguage.includes('en')) {
    locale = 'en'
  }

  setLocale(locale)
})
</script> -->