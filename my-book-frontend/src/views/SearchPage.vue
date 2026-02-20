<template>
  <div :class="['search-wrapper', { 'has-results': results.length > 0 }]">
    
    <div class="logo-area">
      <h1 class="google-logo">
        <span style="color: #4285F4">B</span>
        <span style="color: #EA4335">o</span>
        <span style="color: #FBBC05">o</span>
        <span style="color: #4285F4">k</span>
        <span style="color: #34A853">G</span>
        <span style="color: #EA4335">o</span>
      </h1>
    </div>

    <div class="search-bar-container">
      <div class="input-group">
        <span class="search-icon" @click="performSearch">🔍</span>
        <input 
          type="text" 
          v-model="query" 
          @keyup.enter="performSearch"
          placeholder="搜索你感兴趣的图书..."
        />
      </div>
    </div>

    <div v-if="results.length > 0" class="results-container">
      <div v-for="book in results" :key="book.UPC" class="book-item">
        <div class="image-container">
          <img :src="book.image" alt="book cover" class="book-thumbnail" />
        </div>
        
        <div class="book-details">
          <div class="star-rating">
            <span v-for="i in 5" :key="i" :class="['icon-star', i <= book.rating ? 'filled' : 'empty']">★</span>
          </div>

          <h3 class="book-title" :title="book.book_name">{{ book.book_name }}</h3>
          
          <div class="price-stock">
            <span class="price">£{{ book.price }}</span>
            <span class="stock-status">
              <i class="check-icon">✔</i> In stock
            </span>
          </div>

          <button @click="addToBasket(book.UPC)" class="buy-button">Add to basket</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';
import $ from 'jquery';

export default {
  setup() {
    const query = ref('');
    const results = ref([]);

    const performSearch = () => {
      const keyword = query.value.trim();
      if (!keyword) return;

      $.ajax({
        url: "http://127.0.0.1:8000/search/api/suggest/", 
        type: "get",
        data: { q: keyword },
        xhrFields: { withCredentials: true }, 
        success(resp) {
          if (resp.data && resp.data.length > 0) {
            results.value = resp.data;
          }
        },
        error(err) {
          console.error("搜索失败:", err);
        }
      });
    };

    const addToBasket = (upc) => {
      alert(`书籍已加入收藏！UPC: ${upc}`);
    };

    return { query, results, performSearch, addToBasket };
  }
}
</script>

<style scoped>
/* --- 保留你的核心动画布局逻辑 --- */
.search-wrapper {
  display: flex; flex-direction: column; align-items: center;
  transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
  padding-top: 20vh; width: 100%;
}
.has-results { padding-top: 30px; }

.google-logo { font-size: 90px; font-family: Arial, sans-serif; margin-bottom: 30px; transition: all 0.5s ease; }
.has-results .google-logo { font-size: 35px; margin-bottom: 15px; }

.search-bar-container { width: 100%; max-width: 600px; padding: 0 20px; }
.input-group {
  display: flex; align-items: center; background: white; border: 1px solid #dfe1e5;
  border-radius: 24px; padding: 0 20px; height: 46px; transition: box-shadow 0.2s;
}
.input-group:hover, .input-group:focus-within { box-shadow: 0 1px 6px rgba(32,33,36,0.28); }
.search-icon { color: #9aa0a6; margin-right: 10px; cursor: pointer; }
input { flex: 1; border: none; outline: none; font-size: 16px; }

/* --- 样式注入：100% 模拟“图书推荐”页风格 --- */
.results-container {
  margin-top: 40px; width: 95%; max-width: 1200px;
  display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 25px;
}

.book-item { background: #fff; display: flex; flex-direction: column; align-items: center; text-align: center; }

.image-container { width: 100%; height: 200px; display: flex; justify-content: center; align-items: center; margin-bottom: 15px; }
.book-thumbnail { max-height: 100%; border: 1px solid #eee; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }

/* 星星样式 */
.star-rating { color: #ccc; font-size: 18px; margin-bottom: 8px; }
.filled { color: #f39c12; }

/* 标题样式：蓝色且悬浮下划线 */
.book-title { font-size: 14px; color: #3498db; height: 40px; overflow: hidden; margin-bottom: 10px; cursor: pointer; }
.book-title:hover { text-decoration: underline; }

/* 价格和库存颜色：绿色 */
.price-stock { display: flex; flex-direction: column; align-items: center; margin-bottom: 15px; }
.price { font-size: 18px; font-weight: bold; color: #4d8234; margin-bottom: 5px; }
.stock-status { color: #4d8234; font-size: 13px; }

/* 按钮样式：蓝色宽按钮 */
.buy-button {
  width: 100%; background-color: #559ed4; color: white; border: none;
  padding: 10px; border-radius: 4px; cursor: pointer; font-size: 14px;
}
.buy-button:hover { background-color: #448cc4; }
</style>