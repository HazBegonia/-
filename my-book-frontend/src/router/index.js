import { createRouter, createWebHistory } from 'vue-router'
import LoginPage from '../views/LoginPage.vue'
// 根据你的图片，HomeView 放在了 components 文件夹下
import HomeView from '../components/HomeView.vue' 

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', name: 'login', component: LoginPage },
  { 
    path: '/home', 
    name: 'home', 
    component: HomeView,
    redirect: '/home/search', // 登录后默认显示搜索页
    children: [
      {
        path: 'search',
        name: 'search',
        // 建议在 views 下创建对应的页面文件
        component: () => import('../views/SearchPage.vue') 
      },
      {
        path: 'recommend',
        name: 'recommend',
        component: () => import('../views/RecommendPage.vue')
      },
      {
        path: 'profile',
        name: 'profile',
        component: () => import('../views/ProfilePage.vue')
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router