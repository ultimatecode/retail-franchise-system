<template>
  <div class="login-container">
    <div class="login-bg">
      <div class="bg-circle circle-1"></div>
      <div class="bg-circle circle-2"></div>
      <div class="bg-circle circle-3"></div>
      <div class="bg-circle circle-4"></div>
    </div>

    <div class="login-content">
      <div class="login-logo">
        <div class="logo-icon">
          <span class="logo-text">S</span>
        </div>
        <h1>Sunday Space</h1>
        <p>零售管理系统</p>
      </div>

      <el-form
        ref="loginFormRef"
        :model="loginForm"
        :rules="loginRules"
        class="login-form"
        @keyup.enter="handleLogin"
      >
        <el-form-item prop="user_login_account">
          <el-input
            v-model="loginForm.user_login_account"
            placeholder="请输入账号"
            size="large"
            prefix-icon="User"
            clearable
            class="custom-input"
          />
        </el-form-item>

        <el-form-item prop="password">
          <el-input
            v-model="loginForm.password"
            type="password"
            placeholder="请输入密码"
            size="large"
            prefix-icon="Lock"
            show-password
            clearable
            class="custom-input"
          />
        </el-form-item>

        <el-form-item>
          <el-button
            type="primary"
            size="large"
            :loading="loading"
            class="login-btn"
            @click="handleLogin"
          >
            <span>登 录</span>
            <el-icon class="btn-icon"><ArrowRight /></el-icon>
          </el-button>
        </el-form-item>
      </el-form>

      <div class="login-footer">
        <p>Sunday Space Retail Management System</p>
      </div>
    </div>

    <div class="floating-icons">
      <div class="float-icon" style="top: 10%; left: 10%; animation-delay: 0s;">🛍️</div>
      <div class="float-icon" style="top: 20%; right: 15%; animation-delay: 1s;">📦</div>
      <div class="float-icon" style="bottom: 30%; left: 8%; animation-delay: 2s;">🏪</div>
      <div class="float-icon" style="bottom: 15%; right: 10%; animation-delay: 0.5s;">💼</div>
      <div class="float-icon" style="top: 50%; left: 5%; animation-delay: 1.5s;">📊</div>
      <div class="float-icon" style="top: 40%; right: 8%; animation-delay: 2.5s;">🎯</div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

const loginFormRef = ref(null)
const loading = ref(false)

const loginForm = reactive({
  user_login_account: '',
  password: ''
})

const loginRules = {
  user_login_account: [
    { required: true, message: '请输入账号', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 1, message: '密码不能为空', trigger: 'blur' }
  ]
}

const handleLogin = async () => {
  const valid = await loginFormRef.value?.validate()
  if (!valid) return

  loading.value = true
  try {
    const success = await userStore.login(loginForm)
    if (success) {
      ElMessage.success('登录成功')
      router.push('/dashboard')
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped lang="scss">
.login-container {
  position: relative;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  overflow: hidden;
}

.login-bg {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
}

.bg-circle {
  position: absolute;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
  animation: float 20s infinite ease-in-out;
}

.circle-1 {
  width: 300px;
  height: 300px;
  top: -100px;
  left: -100px;
}

.circle-2 {
  width: 200px;
  height: 200px;
  top: 20%;
  right: -50px;
  animation-delay: -5s;
}

.circle-3 {
  width: 150px;
  height: 150px;
  bottom: 10%;
  left: 10%;
  animation-delay: -10s;
}

.circle-4 {
  width: 250px;
  height: 250px;
  bottom: -100px;
  right: -80px;
  animation-delay: -15s;
}

@keyframes float {
  0%, 100% {
    transform: translate(0, 0) scale(1);
  }
  25% {
    transform: translate(30px, 30px) scale(1.1);
  }
  50% {
    transform: translate(0, 50px) scale(1);
  }
  75% {
    transform: translate(-30px, 20px) scale(0.9);
  }
}

.login-content {
  position: relative;
  z-index: 10;
  width: 100%;
  max-width: 420px;
  padding: 40px;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 24px;
  box-shadow: 0 30px 80px rgba(0, 0, 0, 0.2);
  backdrop-filter: blur(10px);
  animation: slideUp 0.6s ease;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.login-logo {
  text-align: center;
  margin-bottom: 40px;

  .logo-icon {
    width: 70px;
    height: 70px;
    margin: 0 auto 20px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);

    .logo-text {
      font-size: 36px;
      font-weight: 700;
      color: #fff;
    }
  }

  h1 {
    font-size: 28px;
    font-weight: 700;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 8px;
  }

  p {
    font-size: 14px;
    color: #999;
  }
}

.login-form {
  :deep(.el-form-item) {
    margin-bottom: 24px;
  }

  :deep(.custom-input) {
    .el-input__wrapper {
      background: #f5f7fa;
      border: 2px solid transparent;
      border-radius: 12px;
      box-shadow: none;
      padding: 8px 16px;
      transition: all 0.3s ease;

      &:hover {
        background: #f0f2f5;
      }

      &.is-focus {
        background: #fff;
        border-color: #667eea;
        box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.1);
      }
    }

    .el-input__inner {
      color: #2c3e50;
      font-size: 15px;

      &::placeholder {
        color: #aaa;
      }
    }

    .el-input__prefix {
      color: #667eea;
    }

    .el-input__clear,
    .el-input__password {
      color: #aaa;

      &:hover {
        color: #667eea;
      }
    }
  }

  .login-btn {
    width: 100%;
    height: 52px;
    border-radius: 14px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border: none;
    color: #fff;
    font-size: 16px;
    font-weight: 600;
    letter-spacing: 2px;
    box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;

    &:hover {
      transform: translateY(-2px);
      box-shadow: 0 15px 40px rgba(102, 126, 234, 0.4);
    }

    &:active {
      transform: translateY(0);
    }

    .btn-icon {
      transition: transform 0.3s ease;
    }

    &:hover .btn-icon {
      transform: translateX(5px);
    }
  }
}

.login-footer {
  margin-top: 30px;
  text-align: center;

  p {
    font-size: 12px;
    color: #999;
  }
}

.floating-icons {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 1;
}

.float-icon {
  position: absolute;
  font-size: 32px;
  opacity: 0.3;
  animation: bounce 3s infinite ease-in-out;
}

@keyframes bounce {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-20px);
  }
}

:deep(.el-form-item__error) {
  color: #f5576c;
  font-size: 12px;
}
</style>
