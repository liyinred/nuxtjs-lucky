<template>
  <view style="display:flex; flex-direction: column; align-items: center; justify-content: center;">
    <view v-if="isLuckyWheelVisible" style="margin-top: 20px;">
      <LuckyWheel ref="myLucky" width="350rpx" height="350rpx" :prizes="prizes" :blocks="blocks" :buttons="buttons"
        @start="startCallback" @end="endCallback" />
    </view>
    <view v-else
      style="margin-top: 20px; display: flex; flex-direction: column; align-items: center; justify-content: center;">
      <img :src="imageSrc" style="margin-top: 20px; width: 60%; height: auto;" />
      <view style="font-weight: bold;font-size: 35px;font-style: italic;">{{ resultMessage }}</view>
      <view style="font-size: 20px; margin-top: 10px;">当前时间：{{ shanghaiTime }}</view>
    </view>
    <view v-if="resultMessage1 && isLuckyWheelVisible"
      style="margin-top: 20px; display: flex; flex-direction: column; align-items: center; justify-content: center;">
      <img :src="imageSrc" style="margin-top: 20px; width: 50%; height: auto;" />
      <view style="font-weight: bold; font-size: 30px;">您获取的奖品为：{{ resultMessage1 }}</view>
      <view style="font-size: 15px;color: gray;">请勿刷新界面并截图以保存获奖记录</view>
      <view style="font-size: 20px; margin-top: 10px;">当前时间：{{ shanghaiTime }}</view>
    </view>
  </view>
</template>

<script>
export default {
  setup() {
    useHead({
      title: 'MSBIO抽奖'
    })
    const shanghaiTime = ref('');

    const updateTime = () => {
      const now = new Date();
      shanghaiTime.value = now.toLocaleString('zh-CN', {
        timeZone: 'Asia/Shanghai',
        hour12: false,
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
      });
    };

    let intervalId;
    onMounted(() => {
      updateTime(); // 初始化时间
      intervalId = setInterval(updateTime, 1000); // 每秒更新一次时间
    });

    onUnmounted(() => {
      clearInterval(intervalId); // 组件卸载时清除定时器
    });

    return {
      shanghaiTime
    };
  },
  data() {
    return {
      imageSrc: 'https://cdn-fusion.imgcdn.store/i/2024/2W369651lUfsVCRb.png',
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
          fonts: [{ text: '招财猫', top: '10%', fontColor: '#92342A' }], background: '#FFFFFF', range: '30',
          imgs: [{
            src: '3.webp',
            width: '35%',
            top: '35px'
          }]
        },
        {
          fonts: [{ text: '小玩偶', top: '10%', fontColor: '#92342A' }], background: '#FFD099', range: '40',
          imgs: [{
            src: '3.webp',
            width: '35%',
            top: '35px'
          }]
        },
        {
          fonts: [{ text: '文创冰箱贴', top: '10%', fontColor: '#92342A' }], background: '#FFFFFF', range: '40',
          imgs: [{
            src: '3.webp',
            width: '35%',
            top: '35px'
          }]
        },
        {
          fonts: [{ text: '便签', top: '10%', fontColor: '#92342A' }], background: '#FFD099', range: '100',
          imgs: [{
            src: '3.webp',
            width: '35%',
            top: '35px'
          }]
        },
        {
          fonts: [{ text: '玩具', top: '10%', fontColor: '#92342A' }], background: '#FFFFFF', range: '100',
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
      isLuckyWheelVisible: true,  // 控制LuckyWheel的显示和隐藏
      resultMessage: '',
      resultMessage1: ''
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
      console.log('恭喜中奖: ' + prize.fonts[0].text)
      alert('恭喜你抽到 ' + prize.fonts[0].text + '！')
      this.resultMessage1 = prize.fonts[0].text;
    },

    async fetchLuckyIndex() {
      try {
        const urlParams = new URLSearchParams(window.location.search);
        const openid = urlParams.get('openid');
        console.log("openid is ", openid)
        const response = await fetch(`http://114.132.74.7:8080/get_lucky_product_id/${openid}`)
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
      this.isLuckyWheelVisible = false;
      this.showConfirmDialog('很抱歉，产品已经被抽完', () => {
        this.resultMessage = '十分感谢您的参与';
      });
    },

    handleProductUnavailable1() {
      this.isLuckyWheelVisible = false;
      this.showConfirmDialog('很抱歉，你已经参与过次抽奖活动', () => {
        this.resultMessage = '十分感谢您的参与';
      });
    },


    // 显示确认框，处理用户点击
    showConfirmDialog(message, onConfirm) {
      // 在点击确认或取消时都执行相同的操作
      const userConfirmed = window.confirm(message);

      if (userConfirmed) {
        onConfirm();  // 点击确认时执行
      } else {
        onConfirm();  // 点击取消时也执行相同的处理
      }
    }

  }
}
</script>
