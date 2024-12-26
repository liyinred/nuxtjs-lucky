<template>
  <div>
    <h1>产品列表</h1>
    <div v-if="error">
      <p>数据加载失败：{{ error.message }}</p>
    </div>
    <div v-else>
      <div v-for="product in products" :key="product.id" class="product-card">
        <h2>{{ product.name }}</h2>
        <p><strong>目录号:</strong> {{ product.catalog_number }}</p>
        <p><strong>规格:</strong> {{ product.specification }}</p>
        <p><strong>单位:</strong> {{ product.unit }}</p>
        <p><strong>价格:</strong> ¥{{ product.price }}</p>
        <p><strong>分类:</strong> {{ product.category.join(', ') }}</p>
        <p><strong>次级抗体:</strong> {{ product.secondary_antibody }}</p>
        <p><strong>标签:</strong> {{ product.tag.join(', ') }}</p>
        <p><strong>促销标签:</strong> {{ product.tag_promotion.join(', ') }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

// 使用 Nuxt 3 的 useFetch 获取数据
const { data, error } = await useFetch('https://44ud77915sf2.vicp.fun/products');

// 将 API 返回的结果赋值给 products
const products = ref([]);

if (data.value) {
  products.value = data.value;
}
</script>

<style scoped>
.product-card {
  border: 1px solid #ccc;
  padding: 16px;
  margin: 16px 0;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}
</style>
