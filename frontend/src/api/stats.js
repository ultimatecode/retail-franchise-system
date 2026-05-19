import request from '@/utils/request'

/**
 * 获取销售统计
 */
export function getSalesStats() {
  return request({
    url: '/stats/sales',
    method: 'get'
  })
}
