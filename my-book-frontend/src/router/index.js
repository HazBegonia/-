import { createRouter, createWebHistory } from 'vue-router'
import LoginPage from '../views/LoginPage.vue'

const routes = [
  { path: '/', component: LoginPage } // 设置首页就是你的登录页
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router