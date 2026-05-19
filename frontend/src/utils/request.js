import axios from 'axios'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/stores/user'

// 创建 axios 实例
const service = axios.create({
  baseURL: '/api/v1',
  timeout: 15000
})

// 请求拦截器
service.interceptors.request.use(
  (config) => {
    const userStore = useUserStore()
    if (userStore.token) {
      config.headers.Authorization = `Bearer ${userStore.token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器
service.interceptors.response.use(
  (response) => {
    return response.data
  },
  (error) => {
    const userStore = useUserStore()

    if (error.response) {
      const { status, data } = error.response

      switch (status) {
        case 401:
          // 如果在登录页，不跳转，只显示错误
          if (window.location.pathname === '/login') {
            ElMessage.error(data.detail || '账号或密码错误')
          } else {
            ElMessage.error(data.detail || '登录已过期，请重新登录')
            userStore.logout()
            window.location.href = '/login'
          }
          break
        case 403:
          ElMessage.error(data.detail || '没有权限')
          break
        case 404:
          ElMessage.error(data.detail || '请求的资源不存在')
          break
        case 500:
          ElMessage.error(data.detail || '服务器错误')
          break
        default:
          ElMessage.error(data.detail || '请求失败')
      }
    } else {
      ElMessage.error('网络错误，请检查网络连接')
    }

    return Promise.reject(error)
  }
)

export default service
