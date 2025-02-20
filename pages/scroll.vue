<template>
  <div class="scrollable-container">
    <!-- 这里是可滚动内容 -->
    <p>这是一个很长的内容区域，滚动条会出现。</p>
    <div v-for="i in 1000" :key="i">这是第 {{ i }} 行内容</div>
  </div>
</template>

<style scoped>
.scrollable-container {
  width: 100vw;
  height: 100vh;
  overflow: auto;
}

.scrollable-container::-webkit-scrollbar {
  width: 10px;  /* 定义滚动条宽度 */
  height: 10px; /* 定义滚动条高度（适用于水平滚动） */
  display: none;
}

.scrollable-container::-webkit-scrollbar-thumb {
  background-color: #888;
  border-radius: 10px;
}

.scrollable-container::-webkit-scrollbar-thumb:hover {
  background-color: #f70000;
}

</style>
