import { defineStore } from 'pinia'
import { login as loginApi, getUserInfo } from '@/api/auth'

export const useUserStore = defineStore('user', {
  state: () => ({
    token: localStorage.getItem('token') || '',
    userInfo: null,
  }),

  getters: {
    isLoggedIn: (state) => !!state.token,
    userClass: (state) => state.userInfo?.user_class || '',
    userName: (state) => state.userInfo?.name || state.userInfo?.user_login_account || '',
    userLoginAccount: (state) => state.userInfo?.user_login_account || '',
    deptId: (state) => state.userInfo?.dept_id || null,
  },

  actions: {
    /**
     * 登录
     */
    async login(loginForm) {
      try {
        const res = await loginApi(loginForm)
        this.token = res.access_token
        this.userInfo = res.user_info
        localStorage.setItem('token', res.access_token)
        return true
      } catch (error) {
        return false
      }
    },

    /**
     * 获取用户信息
     */
    async fetchUserInfo() {
      try {
        const res = await getUserInfo()
        this.userInfo = res
        return res
      } catch (error) {
        return null
      }
    },

    /**
     * 登出
     */
    logout() {
      this.token = ''
      this.userInfo = null
      localStorage.removeItem('token')
    },
  },
})
