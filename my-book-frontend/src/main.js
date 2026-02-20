import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store' // 1. 引入 store
import axios from 'axios';

// 2. 使用 .use(store) 挂载它
createApp(App).use(store).use(router).mount('#app')
axios.defaults.withCredentials = true;