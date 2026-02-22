<template>
  <nav class="navbar">
    <div class="nav-content">
      <div class="logo">图书推荐系统</div>
      <div class="links">
        <router-link to="/home/search">搜索图书</router-link>
        <router-link to="/home/recommend">图书推荐</router-link>
        <router-link to="/home/profile">我的</router-link>
      </div>
      <div class="user-status">
        <span>欢迎, {{ username }}</span>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { computed, onMounted } from 'vue';
import { useStore } from 'vuex';

const store = useStore();

// 1. 使用计算属性从 Vuex 获取用户名
// 这样当 store 里的数据变化时，这里的 username 会自动跟着变
const username = computed(() => {
  return store.state.user.username || "访客"; 
});

// 2. 解决刷新页面数据丢失的问题
onMounted(() => {
  const savedName = localStorage.getItem('username');
  if (savedName && !store.state.user.username) {
    // 如果本地有存用户名，但 Vuex 里是空的（说明刷新了），就把它补回去
    store.commit('updateUser', {
      username: savedName,
      is_login: true
    });
  }
});
</script>

<script>
import { computed } from 'vue';
import { useStore } from 'vuex';

export default {
  setup() {
    const store = useStore();
    // 假设你在登录成功后将用户名存入了 Vuex
    const username = computed(() => store.state.username || '访客');
    return { username };
  }
}
</script>

<style scoped>
.navbar {
  position: fixed; /* 固定在顶部 */
  top: 0;
  left: 0;
  width: 100%;
  height: 60px;
  background-color: #2c3e50;
  color: white;
  z-index: 1000;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.nav-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 100%;
  padding: 0 20px;
}

.links a {
  color: #bdc3c7;
  text-decoration: none;
  margin: 0 15px;
  font-weight: 500;
  transition: color 0.3s;
}

/* 当前激活路由的样式 */
.router-link-active {
  color: #ffffff !important;
  border-bottom: 2px solid #ffffff;
  padding-bottom: 5px;
}
</style>