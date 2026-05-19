import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { getUserInfo } from '@/api/auth'
import { ElMessage } from 'element-plus'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/login/index.vue'),
    meta: { title: '登录', requiresAuth: false }
  },
  {
    path: '/',
    redirect: '/dashboard'
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('@/views/dashboard/index.vue'),
    meta: { title: '首页', requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach(async (to, from, next) => {
  const userStore = useUserStore()
  const token = userStore.token

  // 设置页面标题
  document.title = to.meta.title ? `${to.meta.title} - Sunday Space零售系统` : 'Sunday Space零售系统'

  if (to.meta.requiresAuth !== false) {
    // 需要登录
    if (token) {
      // 有token，验证是否有效
      if (!userStore.userInfo) {
        // 没有用户信息，尝试获取
        try {
          await userStore.fetchUserInfo()
          next()
        } catch (error) {
          // token无效，清除并跳转登录
          userStore.logout()
          ElMessage.warning('登录已过期，请重新登录')
          next('/login')
        }
      } else {
        next()
      }
    } else {
      // 没有token，跳转登录
      ElMessage.warning('请先登录')
      next('/login')
    }
  } else {
    // 不需要登录
    if (token && to.path === '/login') {
      next('/dashboard')
    } else {
      next()
    }
  }
})

export default router
