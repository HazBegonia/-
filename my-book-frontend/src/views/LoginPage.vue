<template>
    <div class="login-wrapper">
        <div class="box" v-if="!$store.state.user.pulling_info">
            <div class="pre-box" :style="preBoxStyles">
                <h1>WELCOME</h1>
                <p>JOIN US!</p>
                <div class="img-box">
                    <img :src="currentImage" alt="icon">
                </div>
            </div>

            <div class="register-form">
                <div class="title-box">
                    <h1>注册</h1>
                </div>
                <div class="input-box">
                    <input v-model="registerForm.username" type="text" placeholder="用户名">
                    <input v-model="registerForm.password" type="password" placeholder="密码">
                    <input v-model="registerForm.confirmedPassword" type="password" placeholder="确认密码">
                    
                    <div class="captcha-container">
                        <input v-model="registerForm.captcha" type="text" placeholder="验证码" class="captcha-input">
                        <img src="http://127.0.0.1:8000/captcha/"
                            class="captcha-img"
                            onclick="this.src='http://127.0.0.1:8000/captcha/?'+Math.random()">
                    </div>
                </div>
                <div class="btn-box">
                    <button @click="register">注册</button>
                    <p @click="toggleForm">已有账号?去登录</p>
                </div>
                <div v-if="error_message" class="error-message">{{ error_message }}</div>
            </div>

            <div class="login-form">
                <div class="title-box">
                    <h1>登录</h1>
                </div>
                <div class="input-box">
                    <input v-model="loginForm.username" type="text" placeholder="用户名">
                    <input v-model="loginForm.password" type="password" placeholder="密码">
                    
                    <div class="captcha-container">
                        <input v-model="loginForm.captcha" type="text" placeholder="验证码" class="captcha-input">
                        <img src="http://127.0.0.1:8000/captcha/"
                            class="captcha-img"
                            onclick="this.src='http://127.0.0.1:8000/captcha/?'+Math.random()">
                    </div>
                </div>
                <div class="btn-box">
                    <button @click="login">登录</button>
                    <p @click="toggleForm">没有账号?去注册</p>
                </div>
                <div v-if="error_message" class="error-message">{{ error_message }}</div>
            </div>
        </div>
    </div>
</template>

<script>
import { useStore } from 'vuex'
import { ref, reactive, computed } from 'vue'
import { useRouter } from 'vue-router'
import $ from 'jquery'

export default {
    name: 'LoginPage',
    setup() {
        const store = useStore()
        const router = useRouter()
        const isLoginForm = ref(true)
        const error_message = ref('')
        const loginForm = reactive({ username: '', password: '', captcha: '' })
        const registerForm = reactive({ username: '', password: '', confirmedPassword: '' })

        // 登录逻辑
        const login = () => {
            error_message.value = ''
            $.ajax({
                url: "http://127.0.0.1:8000/api/login/",
                type: "post",
                data: {
                    username: loginForm.username,
                    password: loginForm.password,
                    user_captcha: loginForm.captcha
                },
                xhrFields: { withCredentials: true }, 
                success(resp) {
                    alert("登录成功！");
                    router.push({ name: 'home' });
                },
                error() {
                    error_message.value = "登录失败，请检查账号密码或验证码"
                }
            });
        }

        const register = () => {
            error_message.value = ''
            $.ajax({
                url: "http://127.0.0.1:8000/api/register/",
                type: "post",
                data: {
                    username: registerForm.username,
                    password: registerForm.password,
                    user_captcha: registerForm.captcha
                },
                xhrFields: { withCredentials: true }, 
                success(resp) {
                    alert("注册成功！");
                    toggleForm();
                },
                error(err) {
                    error_message.value = err.responseJSON ? err.responseJSON.msg : "注册失败";
                }
            });
        }

        const preBoxStyles = computed(() => ({
            transform: `translateX(${isLoginForm.value ? 0 : '100%'})`,
            backgroundColor: isLoginForm.value ? 'rgb(139,232,145)' : 'rgb(173,208,216)'
        }))

        // 修正：确保路径和你的 assets 结构完全一致
        const currentImage = computed(() =>
            isLoginForm.value
                ? require('@/assets/images/icon/login.png')
                : require('@/assets/images/icon/regiestor.png')
        )

        const toggleForm = () => {
            isLoginForm.value = !isLoginForm.value;
            error_message.value = '';
        }

        return {
            isLoginForm, loginForm, registerForm, error_message,
            preBoxStyles, currentImage, toggleForm, login, register
        }
    }
}
</script>
<style scoped>
/* 背景容器 */
.login-wrapper {
    min-height: 100vh;
    width: 100vw;
    display: flex;
    justify-content: center;
    align-items: center;
    background: linear-gradient(to right, rgb(119, 234, 107), rgb(187, 201, 244)) !important;
}

.box {
    width: 800px;
    height: 500px;
    display: flex;
    position: relative;
    background-color: rgba(255, 255, 255, 0.4);
    border-radius: 12px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    overflow: hidden;
}

.pre-box {
    width: 50%;
    height: 100%;
    position: absolute;
    left: 0;
    top: 0;
    z-index: 10;
    transition: 0.5s ease-in-out;
    display: flex;
    flex-direction: column;
    align-items: center;
}

.pre-box h1 { margin-top: 80px; color: white; letter-spacing: 5px; }
.pre-box p { color: white; margin: 20px 0; font-weight: bold; }

.img-box {
    width: 150px;
    height: 150px;
    border-radius: 50%;
    overflow: hidden;
    background: white;
}
.img-box img { width: 100%; height: 100%; object-fit: cover; }

.login-form, .register-form {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
}

.title-box { height: 150px; display: flex; align-items: flex-end; margin-bottom: 30px; }
.title-box h1 { color: #fff; text-shadow: 2px 2px 4px rgba(0,0,0,0.1); }

/* --- 对齐核心代码开始 --- */

.input-box {
    display: flex;
    flex-direction: column;
    align-items: center; 
    width: 100%;
}

/* 1. 统一定义所有输入框基础样式 */
input {
    height: 40px;
    border: none;
    border-radius: 20px;
    padding: 0 15px;
    background: rgba(255,255,255,0.8);
    outline: none;
    box-sizing: border-box; /* 确保 padding 不会撑大盒子 */
}

/* 2. 强制设置用户名、密码框、以及验证码容器的宽度为 75% */
.input-box > input, 
.captcha-container {
    width: 75% !important; 
    margin-bottom: 20px;
}

/* 3. 验证码内部布局 */
.captcha-container {
    display: flex;
    justify-content: space-between; /* 左右两端对齐 */
    align-items: center;
}

.captcha-input {
    width: 55% !important; /* 占据容器左侧 55% */
    margin-bottom: 0 !important; /* 取消底部边距，让它在容器内垂直居中 */
}

.captcha-img {
    width: 40% !important; /* 占据容器右侧 40% */
    height: 40px;
    border-radius: 20px;
    background: #fff;
    cursor: pointer;
    object-fit: fill;
}

/* --- 对齐核心代码结束 --- */

.btn-box { margin-top: 10px; display: flex; align-items: center; gap: 10px; }
button {
    padding: 8px 30px;
    border-radius: 20px;
    border: none;
    background: #69b3f0;
    color: white;
    cursor: pointer;
    transition: 0.3s;
}
button:hover { opacity: 0.8; }

.btn-box p { font-size: 12px; color: #fff; cursor: pointer; }

.error-message { color: #ff4444; margin-top: 10px; font-size: 14px; text-align: center; }
</style>