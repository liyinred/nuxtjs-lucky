<script setup>
import { onMounted } from 'vue'

const { setLocale } = useI18n()

// // 在组件挂载时自动设置语言
// onMounted(() => {
//   const browserLanguage = navigator.language || 'en'
//   console.log(browserLanguage)

//   let locale = 'en'

//   if (browserLanguage.includes('zh')) {
//     locale = 'cn'
//   } else if (browserLanguage.includes('en')) {
//     locale = 'en'
//   }

//   setLocale(locale)
// })
</script>

<template>
  <div class="p-4">
    <div class="space-x-2">
      <button 
        @click="setLocale('en')" 
        class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50"
      >
        English
      </button>
      <button 
        @click="setLocale('cn')" 
        class="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-opacity-50"
      >
        中文
      </button>
    </div>
    <p class="mt-4 text-lg">{{ $t('welcome') }}</p>
  </div>
</template>