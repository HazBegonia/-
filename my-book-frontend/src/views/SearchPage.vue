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
      <div v-for="book in results" :key="book.UPC" class="book-card">
        <img :src="book.image" alt="book cover" />
        <div class="book-info">
          <h3>{{ book.book_name }}</h3>
          <p class="category">{{ book.subject }}</p>
          <div class="price-row">
            <span class="price">£{{ book.price }}</span>
            <button class="add-btn">Add to basket</button>
          </div>
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
        // 使用 127.0.0.1 确保本地回环测试最稳定
        url: "http://127.0.0.1:8000/search/api/suggest/", 
        type: "get",
        data: { q: keyword },
        success(resp) {
          if (resp.data && resp.data.length > 0) {
            results.value = resp.data;
          } else {
            alert("未找到匹配的书籍");
            results.value = [];
          }
        },
        error(err) {
          console.error("连接报错:", err);
          alert("服务器连接失败，请确认后端 8000 端口已启动且数据库有数据。");
        }
      });
    };

    return { query, results, performSearch };
  }
}
</script>

<style scoped>
/* --- 严格保留你喜欢的 Google UI 样式 --- */
.search-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
  padding-top: 20vh; /* 初始居中偏上 */
  width: 100%;
}

.has-results {
  padding-top: 30px; /* 搜索后迅速上移 */
}

.google-logo {
  font-size: 90px;
  font-family: Arial, sans-serif;
  margin-bottom: 30px;
  transition: all 0.5s ease;
}

.has-results .google-logo {
  font-size: 35px;
  margin-bottom: 15px;
}

.search-bar-container {
  width: 100%;
  max-width: 600px;
  padding: 0 20px;
}

.input-group {
  display: flex;
  align-items: center;
  background: white;
  border: 1px solid #dfe1e5;
  border-radius: 24px;
  padding: 0 20px;
  height: 46px;
  transition: box-shadow 0.2s;
}

.input-group:hover, .input-group:focus-within {
  box-shadow: 0 1px 6px rgba(32,33,36,0.28);
}

.search-icon { color: #9aa0a6; margin-right: 10px; cursor: pointer; }

input {
  flex: 1;
  border: none;
  outline: none;
  font-size: 16px;
}

.results-container {
  margin-top: 40px;
  width: 90%;
  max-width: 1200px;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 25px;
}

.book-card {
  background: white;
  padding: 15px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
  text-align: center;
}

.book-card img { width: 140px; height: 190px; object-fit: cover; border-radius: 4px; }
.book-info h3 { font-size: 15px; margin: 10px 0; height: 38px; overflow: hidden; }
.price { color: #b12704; font-weight: bold; font-size: 17px; }
.add-btn { 
  background: #f0c14b; border: 1px solid #a88734; border-radius: 4px; 
  padding: 5px 10px; cursor: pointer; margin-top: 10px;
}
</style>