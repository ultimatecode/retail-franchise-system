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

/**
 * 获取个人销售数据
 */
export function getMySalesStats() {
  return request({
    url: '/stats/my-sales',
    method: 'get'
  })
}
