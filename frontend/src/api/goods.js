// 商品相关 API
import request from '@/utils/request'

/**
 * 根据编码查询商品
 * @param {string} code - 商品编码或条码
 */
export function getGoodsByCode(code) {
  return request({
    url: `/goods/query/${code}`,
    method: 'get'
  })
}

/**
 * 获取商品列表
 * @param {Object} params - 查询参数
 * @param {string} params.search - 通用搜索（商品编号或名称）
 * @param {string} params.goods_no - 商品编号
 * @param {string} params.name - 商品名称
 * @param {string} params.material - 材质
 * @param {string} params.fabric - 面料
 * @param {string} params.painting - 工艺
 * @param {string} params.size - 尺寸
 * @param {number} params.goods_cotegory_id1 - 一级分类ID
 * @param {number} params.goods_cotegory_id2 - 二级分类ID
 * @param {string} params.class - 类别
 * @param {string} params.barcode - 条码
 * @param {number} params.category_id - 分类ID（兼容旧版）
 * @param {string} params.goods_class - 商品种类
 * @param {number} params.page - 页码
 * @param {number} params.page_size - 每页数量
 */
export function getGoodsList(params) {
  return request({
    url: '/goods/list',
    method: 'get',
    params
  })
}

/**
 * 获取热销商品
 * @param {number} limit - 返回数量，默认10
 */
export function getHotGoods(limit = 10) {
  return request({
    url: '/goods/hot',
    method: 'get',
    params: { limit }
  })
}

/**
 * 获取滞销商品
 * @param {number} limit - 返回数量，默认10
 */
export function getSlowGoods(limit = 10) {
  return request({
    url: '/goods/slow',
    method: 'get',
    params: { limit }
  })
}

/**
 * 获取库存预警商品
 * @param {number} threshold - 库存预警阈值，默认10
 */
export function getLowStockGoods(threshold = 10) {
  return request({
    url: '/goods/low-stock',
    method: 'get',
    params: { threshold }
  })
}

/**
 * 获取库存统计
 */
export function getInventoryStats() {
  return request({
    url: '/goods/stats/inventory',
    method: 'get'
  })
}
