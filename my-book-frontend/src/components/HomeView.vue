<template>
  <div class="home-container">
    <NavBar />
    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<script>
import NavBar from '@/components/NavBar.vue';

export default {
  components: { NavBar }
}
</script>

<style scoped>
.main-content {
  margin-top: 60px; /* 留出导航栏的高度，防止内容被遮挡 */
  min-height: calc(100vh - 60px);
  background-color: #f9f9f9;
}
</style>