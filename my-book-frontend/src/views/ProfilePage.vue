<template>
  <div class="profile-container">
    <section class="info-card">
      <div class="avatar">{{ userInfo.username?.charAt(0).toUpperCase() }}</div>
      <div class="user-details">
        <h2>{{ userInfo.username }}</h2>
        <button class="action-btn" @click="isChanging = true">修改密码</button>
      </div>
    </section>

    <div v-if="isChanging" class="pwd-modal-overlay">
      <div class="pwd-modal">
        <h3>修改密码</h3>
        <div class="modal-inputs">
          <input v-model="pwdForm.old_password" type="password" placeholder="原密码">
          <input v-model="pwdForm.new_password" type="password" placeholder="新密码">
        </div>
        <div class="modal-btns">
          <button @click="submitChange" class="confirm-btn">确认修改</button>
          <button @click="cancelChange" class="cancel-btn">取消</button>
        </div>
      </div>
    </div>

    <div class="content-grid">
      <section class="list-section">
        <h3>最近浏览</h3>
        <div class="list-wrapper">
          <div v-for="(item, index) in historyList" :key="index" class="list-item">
            <span class="upc-val">{{ item.upc }}</span>
            <span class="time">{{ item.time }}</span>
          </div>
          <p v-if="historyList.length === 0" class="empty">暂无浏览记录</p>
        </div>
      </section>

      <section class="list-section">
        <h3>我的收藏</h3>
        <div class="list-wrapper">
          <div v-for="(item, index) in collectionList" :key="index" class="list-item">
            <div class="book-info">
              <span class="book-name">{{ item.book_name }}</span>
              <span class="upc-sub">{{ item.upc }}</span>
            </div>
            <span class="time">{{ item.collect_time }}</span>
          </div>
          <p v-if="collectionList.length === 0" class="empty">暂无收藏书籍</p>
        </div>
      </section>
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue';
import axios from 'axios';

export default {
  name: 'ProfilePage',
  setup() {
    const userInfo = ref({});
    const historyList = ref([]);
    const collectionList = ref([]);
    const username = localStorage.getItem('username');

    // 修改密码弹窗状态
    const isChanging = ref(false);
    const pwdForm = reactive({ old_password: '', new_password: '' });

    const fetchData = async () => {
      if (!username) return;
      try {
        const [infoRes, historyRes, collectRes] = await Promise.all([
          axios.get(`http://127.0.0.1:8000/api/profile/info/?username=${username}`),
          axios.get(`http://127.0.0.1:8000/api/profile/history/?username=${username}`),
          axios.get(`http://127.0.0.1:8000/api/profile/collections/?username=${username}`)
        ]);
        if (infoRes.data.status === 'success') userInfo.value = infoRes.data.data;
        if (historyRes.data.status === 'success') historyList.value = historyRes.data.data;
        if (collectRes.data.status === 'success') collectionList.value = collectRes.data.data;
      } catch (err) {
        console.error("加载失败:", err);
      }
    };

    const submitChange = async () => {
      try {
        const resp = await axios.post('http://127.0.0.1:8000/api/users/change_password/', {
          username: username,
          old_password: pwdForm.old_password,
          new_password: pwdForm.new_password
        });
        alert(resp.data.msg); // 弹出修改成功
        cancelChange();
      } catch (err) {
        alert(err.response?.data?.msg || "原密码有误"); // 弹出原密码有误
      }
    };

    const cancelChange = () => {
      isChanging.value = false;
      pwdForm.old_password = '';
      pwdForm.new_password = '';
    };

    onMounted(fetchData);
    return { userInfo, historyList, collectionList, isChanging, pwdForm, submitChange, cancelChange };
  }
};
</script>

<style scoped>
.profile-container { padding: 20px; max-width: 1000px; margin: 0 auto; }
.info-card { display: flex; align-items: center; background: #fff; padding: 25px; border-radius: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); margin-bottom: 20px; }
.avatar { width: 60px; height: 60px; background: #8be891; border-radius: 50%; display: flex; justify-content: center; align-items: center; font-size: 24px; color: #fff; margin-right: 20px; }
.action-btn { background: #69b3f0; color: #fff; border: none; padding: 6px 15px; border-radius: 4px; cursor: pointer; font-size: 13px; }

/* 弹窗样式 */
.pwd-modal-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); display: flex; justify-content: center; align-items: center; z-index: 1000; }
.pwd-modal { background: #fff; padding: 25px; border-radius: 8px; width: 300px; box-shadow: 0 5px 15px rgba(0,0,0,0.3); }
.modal-inputs input { width: 100%; margin: 8px 0; padding: 10px; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; }
.modal-btns { display: flex; justify-content: space-between; margin-top: 15px; }
.confirm-btn { background: #69b3f0; color: #fff; border: none; padding: 8px 15px; border-radius: 4px; cursor: pointer; }
.cancel-btn { background: #ccc; color: #fff; border: none; padding: 8px 15px; border-radius: 4px; cursor: pointer; }

/* 列表展示 */
.content-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
.list-section { background: #fff; padding: 20px; border-radius: 12px; min-height: 300px; }
.list-item { display: flex; justify-content: space-between; align-items: center; padding: 12px 0; border-bottom: 1px solid #f5f5f5; }
.upc-val { color: #666; font-family: monospace; }
.book-name { font-weight: bold; color: #333; }
.upc-sub { font-size: 11px; color: #999; display: block; }
.time { font-size: 12px; color: #aaa; }
.empty { text-align: center; color: #ccc; margin-top: 40px; }
</style>