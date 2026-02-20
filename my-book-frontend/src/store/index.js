// src/store/index.js
import { createStore } from 'vuex'

export default createStore({
  state: {
    user: {
      username: "",
      is_login: false
    }
  },
  mutations: {
    // 这个名字必须和 LoginPage.vue 里的 commit 名字一致
    updateUser(state, user) {
      state.user.username = user.username;
      state.user.is_login = user.is_login;
    }
  }
})