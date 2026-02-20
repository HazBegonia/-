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
                    <img :src="captchaUrl" class="captcha-img" @click="refreshCaptcha">
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
                    <img :src="captchaUrl" class="captcha-img" @click="refreshCaptcha" title="点击刷新">
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
import axios from 'axios' // 必须导入

export default {
    name: 'LoginPage',
    setup() {
        const store = useStore()
        const router = useRouter()
        const isLoginForm = ref(true)
        const error_message = ref('')
        
        // 1. 统一管理验证码地址
        const captchaUrl = ref('http://127.0.0.1:8000/api/users/captcha/') 

        const loginForm = reactive({ username: '', password: '', captcha: '' })
        const registerForm = reactive({ username: '', password: '', confirmedPassword: '', captcha: '' })

        // 2. 刷新验证码逻辑
        const refreshCaptcha = () => {
            captchaUrl.value = 'http://127.0.0.1:8000/api/users/captcha/?t=' + Math.random()
        }

        // 3. 登录逻辑 (参数补全)
        // LoginPage.vue 中的 login 函数
        const login = async () => {
            error_message.value = "";
            try {
                console.log("正在尝试登录...", loginForm.username);
                const resp = await axios.post('http://127.0.0.1:8000/api/users/login/', {
                    username: loginForm.username,
                    password: loginForm.password,
                    user_captcha: loginForm.captcha
                });

                // 这里的判断必须和后端返回的 msg 完全一致
                if (resp.data.msg === "登录成功") {
                    console.log("后端验证通过，准备存储数据...");
                    
                    // 1. 存储用户名
                    localStorage.setItem('username', loginForm.username);
                    
                    // 2. 更新 Vuex 状态
                    store.commit('updateUser', {
                        username: loginForm.username,
                        is_login: true
                    });

                    console.log("数据存储完毕，准备跳转...");
                    // 3. 核心修复：改用路径跳转，避免 name 不匹配的问题
                    // 确保你的路由配置中路径是 /home/recommend
                    await router.push('/home/recommend'); 
                } else {
                    error_message.value = resp.data.msg;
                }
            } catch (err) {
                console.error("前端逻辑崩溃或网络错误:", err);
                refreshCaptcha();
                // 如果后端返回了错误码，显示后端的 msg；否则显示错误对象
                error_message.value = err.response?.data?.msg || "前端页面逻辑错误，请检查控制台";
            }
        };

        // 4. 注册逻辑 (统一使用 axios)
        const register = async () => {
            error_message.value = ''
            if (registerForm.password !== registerForm.confirmedPassword) {
                error_message.value = "两次密码不一致"
                return
            }
            try {
                const resp = await axios.post("http://127.0.0.1:8000/api/users/register/", {
                    username: registerForm.username,
                    password: registerForm.password,
                    user_captcha: registerForm.captcha // 修正绑定后这里就有值了
                });
                alert("注册成功！");
                toggleForm();
            } catch (err) {
                refreshCaptcha();
                error_message.value = err.response?.data?.msg || "注册失败";
            }
        }

        // --- 保持原本的 UI 计算属性不变 ---
        const preBoxStyles = computed(() => ({
            transform: `translateX(${isLoginForm.value ? 0 : '100%'})`,
            backgroundColor: isLoginForm.value ? 'rgb(139,232,145)' : 'rgb(173,208,216)'
        }))

        const currentImage = computed(() =>
            isLoginForm.value
                ? require('@/assets/images/icon/login.png')
                : require('@/assets/images/icon/regiestor.png')
        )

        const toggleForm = () => {
            isLoginForm.value = !isLoginForm.value;
            error_message.value = '';
            refreshCaptcha(); 
        }

        return {
            isLoginForm, loginForm, registerForm, error_message, captchaUrl,
            preBoxStyles, currentImage, toggleForm, login, register, refreshCaptcha
        }
    }
}
</script>

<style scoped>
/* 这里 100% 保留你之前的 CSS 代码，不做任何改动 */
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

.input-box {
    display: flex;
    flex-direction: column;
    align-items: center; 
    width: 100%;
}

input {
    height: 40px;
    border: none;
    border-radius: 20px;
    padding: 0 15px;
    background: rgba(255,255,255,0.8);
    outline: none;
    box-sizing: border-box; 
}

.input-box > input, 
.captcha-container {
    width: 75% !important; 
    margin-bottom: 20px;
}

.captcha-container {
    display: flex;
    justify-content: space-between; 
    align-items: center;
}

.captcha-input {
    width: 55% !important; 
    margin-bottom: 0 !important; 
}

.captcha-img {
    width: 40% !important; 
    height: 40px;
    border-radius: 20px;
    background: #fff;
    cursor: pointer;
    object-fit: fill;
}

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