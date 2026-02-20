<template>
  <div class="recommend-wrapper">
    <div class="page-header">
      <h2>🎯 为您精心推荐</h2>
      <p class="subtitle">根据您的搜索偏好，为您找到了以下书籍</p>
    </div>

    <div v-if="loading" class="status-box">智能推荐引擎正在计算中...</div>

    <div v-else-if="recommendBooks.length > 0" class="recommend-grid">
      <div v-for="book in recommendBooks" :key="book.id" class="book-item">
        <div class="image-container">
          <img :src="book.image" :alt="book.book_name" class="book-thumbnail" />
        </div>
        
        <div class="book-details">
          <div class="star-rating">
            <span v-for="i in 5" :key="i" :class="['icon-star', i <= book.rating ? 'filled' : 'empty']">★</span>
          </div>

          <h3 class="book-title" :title="book.book_name">{{ book.book_name }}</h3>
          
          <div class="price-stock">
            <span class="price">£{{ book.price.toFixed(2) }}</span>
            <span class="stock-status">
              <i class="check-icon">✔</i> In stock
            </span>
          </div>

          <button @click="addToBasket(book.upc)" class="buy-button">Add to basket</button>
        </div>
      </div>
    </div>

    <div v-else class="status-box empty">
      <p>暂无个性化推荐，快去搜索你喜欢的书籍吧！</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useStore } from 'vuex';

const store = useStore();
const recommendBooks = ref([]);
const loading = ref(true);

const fetchRecommendations = async () => {
  // 必须获取已登录的用户名
  const username = store.state.user.username || localStorage.getItem('username');
  
  if (!username) {
    loading.value = false;
    return;
  }

  try {
    const response = await axios.get(`http://127.0.0.1:8000/api/recommend/get/`, {
      params: { username: username }
    });
    if (response.data.status === 'success') {
      recommendBooks.value = response.data.data;
    }
  } catch (error) {
    console.error("推荐获取失败:", error);
  } finally {
    loading.value = false;
  }
};

const addToBasket = (upc) => {
  alert(`UPC: ${upc} 已加入收藏清单！`);
};

onMounted(() => {
  fetchRecommendations();
});
</script>

<style scoped>
/* 核心布局，复刻截图样式 */
.recommend-wrapper { max-width: 1000px; margin: 0 auto; padding: 40px 20px; font-family: sans-serif; }
.page-header { text-align: left; margin-bottom: 30px; border-bottom: 1px solid #ddd; padding-bottom: 15px; }
.subtitle { color: #888; font-size: 14px; }

/* 4列网格布局 */
.recommend-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 25px; }

.book-item { background: #fff; transition: transform 0.2s; display: flex; flex-direction: column; align-items: center; text-align: center; }

.image-container { width: 100%; height: 200px; display: flex; justify-content: center; align-items: center; margin-bottom: 15px; }
.book-thumbnail { max-height: 100%; border: 1px solid #eee; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }

/* 星星样式 */
.star-rating { color: #ccc; font-size: 18px; margin-bottom: 8px; }
.filled { color: #f39c12; }

.book-title { font-size: 14px; color: #3498db; height: 40px; overflow: hidden; margin-bottom: 10px; cursor: pointer; }
.book-title:hover { text-decoration: underline; }

/* 价格和库存 */
.price-stock { display: flex; flex-direction: column; align-items: center; margin-bottom: 15px; }
.price { color: #444; font-size: 18px; font-weight: bold; margin-bottom: 5px; color: #4d8234; /* 绿色价格 */ }
.stock-status { color: #4d8234; font-size: 13px; font-weight: normal; }
.check-icon { font-style: normal; }

/* 蓝色按钮 */
.buy-button { width: 100%; background-color: #559ed4; color: white; border: none; padding: 10px; border-radius: 4px; cursor: pointer; font-size: 14px; }
.buy-button:hover { background-color: #448cc4; }

.status-box { text-align: center; padding: 50px; color: #999; }
</style>