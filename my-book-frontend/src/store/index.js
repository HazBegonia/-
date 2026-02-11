import { createStore } from 'vuex'

export default createStore({
  state: {
    user: {
      pulling_info: false,
      is_login: false
    }
  },
  mutations: {
    updateToken(state, token) {
      state.token = token;
    },
    updatePullingInfo(state, pulling_info) {
      state.user.pulling_info = pulling_info;
    }
  },
  actions: {
    // 暂时留空，保证你的 LoginPage.vue 调用时不崩溃
    login(context, data) { },
    getinfo(context, data) { }
  }
})