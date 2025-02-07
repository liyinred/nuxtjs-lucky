<template>
  <div style="display:flex; flex-direction: column; align-items: center; justify-content: center;">
    <!-- <div v-if="isLuckyWheelVisible" style="margin-top: 20px;font-weight: bold;font-size: 20px;">
      {{ $t('wheel') }}
    </div> -->
    <div v-if="isLuckyWheelVisible" style="margin-top: 20px;">
      <LuckyWheel ref="myLucky" width="350px" height="350px" :prizes="prizes" :blocks="blocks" :buttons="buttons"
        :default-config="default1" @start="startCallback" @end="endCallback" />
    </div>
    <div v-else
      style="margin-top: 20px; display: flex; flex-direction: column; align-items: center; justify-content: center;">
      <img :src="msbioLogo" style="margin-top: 20px; width: 50%; height: auto;" />
      <div style="font-weight: bold;font-size: 30px;">{{ resultMessage }}</div>
      <div style="font-size: 20px; margin-top: 10px;">{{ $t('time') }}{{ shanghaiTime }}</div>
    </div>
    <div v-if="resultMessage1 && isLuckyWheelVisible"
      style="margin-top: 0px; display: flex; flex-direction: column; align-items: center; justify-content: center;">
      <img :src="msbioLogo" style="margin-top: 20px; width: 50%; height: auto;" />
      <div style="font-weight: bold; font-size: 30px;">{{ $t('prize') }}{{ resultMessage1 }}</div>
      <div style="font-size: 15px;color: gray;">{{ $t('user') }}{{ user }}</div>
      <div style="font-size: 15px;color: gray;">{{ $t('scrs') }}</div>
      <div style="font-size: 20px; margin-top: 10px;">{{ $t('time') }}{{ shanghaiTime }}</div>
    </div>
  </div>

  <!-- <div>
    <div>
      <button @click="setLocale('en')">en</button>
      <button @click="setLocale('cn')">cn</button>
      <p>{{ $t('welcome') }}</p>
    </div>
  </div> -->

</template>

<script setup>
import { onMounted, onUnmounted, ref } from 'vue'
import { useI18n } from 'vue-i18n'

// 使用 vue-i18n 设置语言
const { setLocale } = useI18n()

// 在组件挂载时自动设置语言
onMounted(() => {
  const browserLanguage = navigator.language || 'en'
  console.log(browserLanguage)

  let locale = 'en'

  if (browserLanguage.includes('zh')) {
    locale = 'cn'
    useHead({
      title: 'MSBIO抽奖'
    })
  } else if (browserLanguage.includes('en')) {
    locale = 'en'
    useHead({
      title: 'MSBIO Lucky'
    })
  }

  setLocale(locale)
})

// 获取并显示上海时间
const shanghaiTime = ref('')

const updateTime = () => {
  const now = new Date()
  shanghaiTime.value = now.toLocaleString('zh-CN', {
    timeZone: 'Asia/Shanghai',
    hour12: false,
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
}

let intervalId
onMounted(() => {
  updateTime() // 初始化时间
  intervalId = setInterval(updateTime, 1000) // 每秒更新一次时间
})

onUnmounted(() => {
  clearInterval(intervalId) // 组件卸载时清除定时器
})

</script>


<script>
export default {
  // setup() {
  //   useHead({
  //     title: 'MSBIO抽奖'
  //   })
  //   const shanghaiTime = ref('');

  //   const updateTime = () => {
  //     const now = new Date();
  //     shanghaiTime.value = now.toLocaleString('zh-CN', {
  //       timeZone: 'Asia/Shanghai',
  //       hour12: false,
  //       year: 'numeric',
  //       month: '2-digit',
  //       day: '2-digit',
  //       hour: '2-digit',
  //       minute: '2-digit',
  //       second: '2-digit'
  //     });
  //   };

  //   let intervalId;
  //   onMounted(() => {
  //     updateTime(); // 初始化时间
  //     intervalId = setInterval(updateTime, 1000); // 每秒更新一次时间
  //   });

  //   onUnmounted(() => {
  //     clearInterval(intervalId); // 组件卸载时清除定时器
  //   });

  //   return {
  //     shanghaiTime
  //   };
  // },
  data() {
    return {
      msbioLogo: 'msbio.avif',
      blocks: [
        // { padding: '13px', background: '#617df2' },
        {
          padding: '33',
          imgs: [{
            src: '1.webp',
            width: '100%',
            top: '5px',
            left: '4px',
            rotate: true
          }]
        },
      ],
      prizes: [
        {
          fonts: [{ text: '雨伞', top: '10%', fontColor: '#92342A' }], background: '#FFD099', range: '30',
          imgs: [{
            src: '3.webp',
            width: '35%',
            top: '35px'
          }]
        },
        {
          fonts: [{ text: '玩具', top: '10%', fontColor: '#92342A' }], background: '#FFFFFF', range: '30',
          imgs: [{
            src: '3.webp',
            width: '35%',
            top: '35px'
          }]
        },
        {
          fonts: [{ text: '招财猫', top: '10%', fontColor: '#92342A' }], background: '#FFD099', range: '40',
          imgs: [{
            src: '3.webp',
            width: '35%',
            top: '35px'
          }]
        },
        {
          fonts: [{ text: '小玩偶', top: '10%', fontColor: '#92342A' }], background: '#FFFFFF', range: '40',
          imgs: [{
            src: '3.webp',
            width: '35%',
            top: '35px'
          }]
        },
        {
          fonts: [{ text: '冰箱贴', top: '10%', fontColor: '#92342A' }], background: '#FFD099', range: '100',
          imgs: [{
            src: '3.webp',
            width: '35%',
            top: '35px'
          }]
        },
        {
          fonts: [{ text: '便签', top: '10%', fontColor: '#92342A' }], background: '#FFFFFF', range: '100',
          imgs: [{
            src: '3.webp',
            width: '35%',
            top: '35px'
          }]
        },
      ],
      buttons: [
        // { radius: '40%', background: '#617df2' },
        // { radius: '35%', background: '#afc8ff' },
        // {
        //   radius: '30%', background: '#869cfa',
        //   pointer: true,
        //   fonts: [{ text: '开始', top: '-10px' }]
        // },
        {
          radius: '45%',
          imgs: [{
            src: '2.webp ',
            width: '80%',
            top: '-95%'
          }]
        }
      ],
      default1: {
        speed: 40
      },
      isLuckyWheelVisible: true,  // 控制LuckyWheel的显示和隐藏
      resultMessage: '',
      resultMessage1: '',
      user: ''
    }
  },
  methods: {
    // 点击抽奖按钮会触发start回调
    async startCallback() {
      this.$refs.myLucky.play()

      try {
        // 异步请求接口获取index值
        const response = await this.fetchLuckyIndex()
        if (response && response.index !== undefined) {
          const index = response.index // 假设接口返回的JSON结构是 { index: 0 }
          this.user = response.user
          // 模拟延迟以展示抽奖动画
          setTimeout(() => {
            // 调用stop停止旋转并传递中奖索引
            this.$refs.myLucky.stop(index)
          }, 3000)
        } else {
          console.error('未能获取有效的幸运索引')
        }
      } catch (error) {
        console.error('获取幸运索引失败', error)
      }
    },

    // 抽奖结束会触发end回调
    endCallback(prize) {
      const message1 = this.$t('won');
      console.log('抽到的 prize' + prize.fonts[0].text)
      alert(message1 + prize.fonts[0].text + '！')
      this.resultMessage1 = prize.fonts[0].text;
    },

    async fetchLuckyIndex() {
      try {
        const urlParams = new URLSearchParams(window.location.search);
        const openid = urlParams.get('openid');
        console.log("openid is ", openid)
        const response = await fetch(`http://192.168.1.125:8080/get_lucky_product_id/${openid}`)
        if (response.status === 404) {
          this.handleProductUnavailable()
          return null;
        }
        if (response.status === 400) {
          this.handleProductUnavailable1()
          return null;
        }

        if (!response.ok) {
          throw new Error('网络错误')
        }

        return await response.json()
      } catch (error) {
        this.handleProductUnavailable()
        console.error('接口请求失败:', error)
        throw error
      }
    },

    // 处理产品已抽完的情况
    handleProductUnavailable() {
      const message1 = this.$t('sry1');
      const message2 = this.$t('thx');
      this.isLuckyWheelVisible = false;
      this.showConfirmDialog(message1, () => {
        this.resultMessage = message2;
        // this.$router.push('/thanks');
      });
    },

    handleProductUnavailable1() {
      const message1 = this.$t('sry2');
      const message2 = this.$t('thx');
      this.isLuckyWheelVisible = false;
      this.showConfirmDialog(message1, () => {
        this.resultMessage = message2;
        // this.$router.push('/thanks');
      });
    },


    // 显示确认框，处理用户点击
    showConfirmDialog(message, onConfirm) {
      const userConfirmed = window.confirm(message);

      if (userConfirmed) {
        onConfirm();
      } else {
        onConfirm();
      }
    }

  }
}
</script>
