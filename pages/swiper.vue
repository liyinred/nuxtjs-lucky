<template>
  <div class="swiper-container">
    <swiper :modules="modules" :autoplay="{ delay: 3000, disableOnInteraction: false }" :effect="'fade'" :loop="true"
      :navigation="{
        nextEl: '.swiper-button-next',
        prevEl: '.swiper-button-prev',
      }" :pagination="{
        el: '.swiper-pagination',
        clickable: true,
      }" class="swiper swiper-fade swiper-initialized swiper-horizontal swiper-watch-progress swiper-backface-hidden">
      <swiper-slide v-for="(image, index) in images" :key="index">
        <img :src="image" alt="Slide" class="swiper-image" />
      </swiper-slide>

      <!-- 导航箭头 -->
      <div class="swiper-button-next"></div>
      <div class="swiper-button-prev"></div>

      <!-- 分页器 -->
      <div class="swiper-pagination"></div>
    </swiper>
  </div>
</template>

<script>
import { Swiper, SwiperSlide } from 'swiper/vue';
import { Autoplay, EffectFade, Navigation, Pagination } from 'swiper/modules';
import 'swiper/swiper-bundle.css';

export default {
  components: {
    Swiper,
    SwiperSlide,
  },
  setup() {
    const images = [
      '/swiper/c1.avif',
      '/swiper/c2.avif',
      '/swiper/c3.avif',
    ];

    return {
      images,
      modules: [Autoplay, EffectFade, Navigation, Pagination],
    };
  },
};
</script>

<style>
.swiper-container {
  width: 100vw;
}

.swiper {
  width: 100%;
  height: 100%;
}

.swiper-slide {
  display: flex;
  justify-content: center;
  align-items: center;
}

.swiper-image {
  width: 100vw;
  height: auto;
  object-fit: cover;
}

/* 导航箭头样式 */
.swiper-button-next,
.swiper-button-prev {
  color: white;
  /* 箭头颜色 */
  /* background-color: rgba(0, 0, 0, 0.5); */
  /* 背景色 */
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  /* 默认隐藏 */
  transition: opacity 0.3s ease;
}

.swiper-button-next::after,
.swiper-button-prev::after {
  font-size: 16px;
  font-weight: bold;
  /* 箭头大小 */
}

.swiper-container:hover .swiper-button-next,
.swiper-container:hover .swiper-button-prev {
  opacity: 1;
  /* 鼠标悬停时显示 */
}

.swiper-button-next {
  right: 10px;
  /* 右侧箭头位置 */
}

.swiper-button-prev {
  left: 10px;
  /* 左侧箭头位置 */
}

.swiper-pagination {
  position: absolute;
  bottom: 10px;
  left: 0;
  width: 100%;
  text-align: center;
}

.swiper-pagination-bullet {
  background: rgb(255, 255, 255);
  opacity: 0.5;
  width: 30px;
  height: 4px;
  display: inline-block;
  border-radius: 4px;
  cursor: pointer;
  /* transition: width 0.3s, background 0.3s; */
  transition: all 0.3s, background 0.3s;
}

.swiper-pagination-bullet-active {
  background: #fff;
  opacity: 1;
  width: 31px;
  height: 5px;
}

@media (max-width: 768px) {
  .swiper-image {
    width: auto;
    height: 70vh;
    /* 使图片高度占满屏幕高度 */
    object-fit: cover;
    object-position: center;
    /* 确保图片居中显示 */
  }
}
</style>
