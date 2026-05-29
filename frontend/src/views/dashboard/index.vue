<template>
  <div class="dashboard-container">
    <!-- 顶部欢迎区 -->
    <div class="welcome-banner">
      <div class="banner-content">
        <div class="greeting">
          <h1>Hi, {{ userStore.userName }} 👋</h1>
          <p>今天是 {{ currentDate }}，祝你工作愉快！</p>
        </div>
        <div class="banner-decoration">
          <div class="circle circle-1"></div>
          <div class="circle circle-2"></div>
          <div class="circle circle-3"></div>
        </div>
      </div>
    </div>

    <!-- 销售数据统计卡片 -->
    <div class="stats-grid">
      <div class="stat-card gradient-1">
        <div class="stat-icon">
          <el-icon><ShoppingCart /></el-icon>
        </div>
        <div class="stat-info">
          <div class="stat-label">今日销售额</div>
          <div class="stat-value">¥{{ formatMoney(stats.todaySales) }}</div>
          <div class="stat-sub">{{ stats.todayOrders }} 笔订单</div>
        </div>
        <div class="stat-bg">Today</div>
      </div>

      <div class="stat-card gradient-2">
        <div class="stat-icon">
          <el-icon><Calendar /></el-icon>
        </div>
        <div class="stat-info">
          <div class="stat-label">昨日销售额</div>
          <div class="stat-value">¥{{ formatMoney(stats.yesterdaySales) }}</div>
          <div class="stat-sub" :class="{ 'up': stats.todaySales > stats.yesterdaySales, 'down': stats.todaySales < stats.yesterdaySales }">
            {{ getGrowthRate() }}
          </div>
        </div>
        <div class="stat-bg">Yesterday</div>
      </div>

      <div class="stat-card gradient-3">
        <div class="stat-icon">
          <el-icon><TrendCharts /></el-icon>
        </div>
        <div class="stat-info">
          <div class="stat-label">本月销售额</div>
          <div class="stat-value">¥{{ formatMoney(stats.monthSales) }}</div>
          <div class="stat-sub">累计本月</div>
        </div>
        <div class="stat-bg">Month</div>
      </div>

      <div class="stat-card gradient-4">
        <div class="stat-icon">
          <el-icon><DataLine /></el-icon>
        </div>
        <div class="stat-info">
          <div class="stat-label">今年销售额</div>
          <div class="stat-value">¥{{ formatMoney(stats.yearSales) }}</div>
          <div class="stat-sub">共 {{ stats.totalOrders }} 笔</div>
        </div>
        <div class="stat-bg">Year</div>
      </div>
    </div>

    <!-- 主内容区 -->
    <div class="main-content">
      <!-- 用户信息卡片 -->
      <div class="info-section">
        <div class="section-title">
          <span class="title-icon">📋</span>
          <span>个人信息</span>
        </div>
        <div class="info-cards">
          <div class="info-card">
            <div class="card-icon">
              <el-icon><User /></el-icon>
            </div>
            <div class="card-content">
              <div class="card-label">登录账号</div>
              <div class="card-value">{{ userStore.userInfo?.user_login_account }}</div>
            </div>
          </div>

          <div class="info-card">
            <div class="card-icon">
              <el-icon><Avatar /></el-icon>
            </div>
            <div class="card-content">
              <div class="card-label">姓名</div>
              <div class="card-value">{{ userStore.userInfo?.name || '-' }}</div>
            </div>
          </div>

          <div class="info-card">
            <div class="card-icon" style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);">
              <el-icon><TrendCharts /></el-icon>
            </div>
            <div class="card-content">
              <div class="card-label">本月销售目标</div>
              <div class="card-value">¥{{ formatMoney(personalStats.monthTarget) }}</div>
            </div>
          </div>

          <div class="info-card">
            <div class="card-icon" style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);">
              <el-icon><DataLine /></el-icon>
            </div>
            <div class="card-content">
              <div class="card-label">本月销售额</div>
              <div class="card-value">¥{{ formatMoney(personalStats.monthSales) }}</div>
            </div>
          </div>

          <div class="info-card">
            <div class="card-icon" style="background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);">
              <el-icon><DataAnalysis /></el-icon>
            </div>
            <div class="card-content">
              <div class="card-label">本年销售额</div>
              <div class="card-value">¥{{ formatMoney(personalStats.yearSales) }}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- 快捷操作 -->
      <div class="actions-section">
        <div class="section-title">
          <span class="title-icon">🚀</span>
          <span>快捷操作</span>
        </div>
        <div class="action-cards">
          <div class="action-card" style="--delay: 0s" @click="router.push('/products')">
            <div class="action-icon" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
              <el-icon><Goods /></el-icon>
            </div>
            <div class="action-content">
              <div class="action-title">商品管理</div>
              <div class="action-desc">管理商品信息</div>
            </div>
            <el-icon class="arrow-icon"><ArrowRight /></el-icon>
          </div>

          <div class="action-card" style="--delay: 0.1s">
            <div class="action-icon" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
              <el-icon><Document /></el-icon>
            </div>
            <div class="action-content">
              <div class="action-title">订单管理</div>
              <div class="action-desc">查看处理订单</div>
            </div>
            <el-icon class="arrow-icon"><ArrowRight /></el-icon>
          </div>

          <div class="action-card" style="--delay: 0.2s">
            <div class="action-icon" style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);">
              <el-icon><Service /></el-icon>
            </div>
            <div class="action-content">
              <div class="action-title">售后管理</div>
              <div class="action-desc">处理售后问题</div>
            </div>
            <el-icon class="arrow-icon"><ArrowRight /></el-icon>
          </div>

          <div class="action-card" style="--delay: 0.3s">
            <div class="action-icon" style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);">
              <el-icon><Management /></el-icon>
            </div>
            <div class="action-content">
              <div class="action-title">行政管理</div>
              <div class="action-desc">行政事务管理</div>
            </div>
            <el-icon class="arrow-icon"><ArrowRight /></el-icon>
          </div>
        </div>
      </div>
    </div>

    <!-- 商品分析区域 -->
    <div class="goods-analysis-section">
      <!-- 热销商品 Top5 -->
      <div class="goods-card">
        <div class="card-header">
          <div class="header-left">
            <span class="card-icon">🔥</span>
            <span class="card-title">热销商品 Top5</span>
          </div>
          <span class="card-subtitle">当月销量排行</span>
        </div>
        <div class="goods-list" v-loading="goodsLoading">
          <div v-if="hotGoods.length === 0" class="empty-state">
            <el-icon><Goods /></el-icon>
            <p>暂无数据</p>
          </div>
          <div v-else class="goods-item" v-for="(item, index) in hotGoods" :key="item.goods_id">
            <div class="goods-rank" :class="`rank-${index + 1}`">{{ index + 1 }}</div>
            <div class="goods-info">
              <div class="goods-name">{{ item.goods_name }}</div>
              <div class="goods-meta">
                <span v-if="item.brand_name" class="brand-tag">{{ item.brand_name }}</span>
                <span v-if="item.barcode" class="barcode-tag">{{ item.barcode }}</span>
              </div>
            </div>
            <div class="goods-data">
              <div class="data-item">
                <span class="data-label">销量</span>
                <span class="data-value primary">{{ item.sales_quantity }}</span>
              </div>
              <div class="data-item">
                <span class="data-label">库存</span>
                <span class="data-value" :class="{ 'low': item.stock_quantity < 10 }">{{ item.stock_quantity }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 滞销商品 Top3 -->
      <div class="goods-card">
        <div class="card-header">
          <div class="header-left">
            <span class="card-icon">📦</span>
            <span class="card-title">滞销商品 Top3</span>
          </div>
          <span class="card-subtitle">库存积压预警</span>
        </div>
        <div class="goods-list" v-loading="goodsLoading">
          <div v-if="slowGoods.length === 0" class="empty-state">
            <el-icon><Goods /></el-icon>
            <p>暂无数据</p>
          </div>
          <div v-else class="goods-item warning" v-for="(item, index) in slowGoods" :key="item.goods_id">
            <div class="goods-rank rank-slow">{{ index + 1 }}</div>
            <div class="goods-info">
              <div class="goods-name">{{ item.goods_name }}</div>
              <div class="goods-meta">
                <span v-if="item.brand_name" class="brand-tag">{{ item.brand_name }}</span>
                <span v-if="item.barcode" class="barcode-tag">{{ item.barcode }}</span>
              </div>
            </div>
            <div class="goods-data">
              <div class="data-item">
                <span class="data-label">库存</span>
                <span class="data-value warning">{{ item.stock_quantity }}</span>
              </div>
              <div class="data-item">
                <span class="data-label">销量</span>
                <span class="data-value muted">{{ item.sales_quantity }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 底部退出按钮 -->
    <div class="logout-section">
      <el-button @click="handleLogout" class="logout-btn">
        <el-icon><SwitchButton /></el-icon>
        退出登录
      </el-button>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { getSalesStats, getMySalesStats } from '@/api/stats'
import { getHotGoods, getSlowGoods } from '@/api/goods'
import dayjs from 'dayjs'
import {
  ShoppingCart,
  Calendar,
  TrendCharts,
  DataLine,
  User,
  Avatar,
  DataAnalysis,
  Goods,
  Document,
  Service,
  Management,
  SwitchButton,
  ArrowRight
} from '@element-plus/icons-vue'

const router = useRouter()
const userStore = useUserStore()

const stats = ref({
  todaySales: 0,
  yesterdaySales: 0,
  monthSales: 0,
  yearSales: 0,
  totalOrders: 0,
  todayOrders: 0
})

// 个人销售数据
const personalStats = ref({
  monthTarget: 0,
  monthSales: 0,
  yearSales: 0
})

// 热销商品
const hotGoods = ref([])

// 滞销商品
const slowGoods = ref([])

// 加载中状态
const goodsLoading = ref(false)

const currentDate = computed(() => {
  return dayjs().format('YYYY年MM月DD日')
})

const formatMoney = (value) => {
  if (!value) return '0.00'
  return Number(value).toLocaleString('zh-CN', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  })
}

const getGrowthRate = () => {
  if (!stats.value.yesterdaySales) return '无可对比'
  const rate = ((stats.value.todaySales - stats.value.yesterdaySales) / stats.value.yesterdaySales * 100).toFixed(1)
  return rate > 0 ? `+${rate}%` : `${rate}%`
}

const loadStats = async () => {
  try {
    const data = await getSalesStats()
    // 后端返回 snake_case，前端使用 camelCase，进行转换
    stats.value = {
      todaySales: data.today_sales,
      yesterdaySales: data.yesterday_sales,
      monthSales: data.month_sales,
      yearSales: data.year_sales,
      totalOrders: data.total_orders,
      todayOrders: data.today_orders
    }
  } catch (error) {
    console.error('获取销售统计失败', error)
  }
}

const loadPersonalStats = async () => {
  try {
    const data = await getMySalesStats()
    personalStats.value = {
      monthTarget: data.month_target,
      monthSales: data.month_sales,
      yearSales: data.year_sales
    }
  } catch (error) {
    console.error('获取个人销售数据失败', error)
  }
}

const handleLogout = () => {
  userStore.logout()
  router.push('/login')
}

// 加载热销商品
const loadHotGoods = async () => {
  try {
    goodsLoading.value = true
    console.log('正在加载热销商品...')
    const data = await getHotGoods({ limit: 5 })
    console.log('热销商品数据:', data)
    hotGoods.value = data || []
  } catch (error) {
    console.error('获取热销商品失败', error)
  } finally {
    goodsLoading.value = false
  }
}

// 加载滞销商品
const loadSlowGoods = async () => {
  try {
    goodsLoading.value = true
    console.log('正在加载滞销商品...')
    const data = await getSlowGoods({ limit: 3 })
    console.log('滞销商品数据:', data)
    slowGoods.value = data || []
  } catch (error) {
    console.error('获取滞销商品失败', error)
  } finally {
    goodsLoading.value = false
  }
}

onMounted(() => {
  loadStats()
  loadPersonalStats()
  loadHotGoods()
  loadSlowGoods()
})
</script>

<style scoped lang="scss">
.dashboard-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #e4e8ec 100%);
  padding: 30px;
}

.welcome-banner {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 24px;
  padding: 40px;
  margin-bottom: 30px;
  position: relative;
  overflow: hidden;
  box-shadow: 0 20px 60px rgba(102, 126, 234, 0.3);

  .banner-content {
    position: relative;
    z-index: 1;
  }

  .greeting {
    h1 {
      font-size: 36px;
      font-weight: 700;
      color: #fff;
      margin-bottom: 10px;
    }

    p {
      font-size: 16px;
      color: rgba(255, 255, 255, 0.8);
    }
  }

  .banner-decoration {
    position: absolute;
    right: 40px;
    top: 50%;
    transform: translateY(-50%);
    display: flex;
    gap: 20px;
  }

  .circle {
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
  }

  .circle-1 { width: 120px; height: 120px; }
  .circle-2 { width: 80px; height: 80px; margin-top: 40px; }
  .circle-3 { width: 50px; height: 50px; margin-top: 60px; }
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-bottom: 30px;
}

.stat-card {
  position: relative;
  border-radius: 20px;
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  overflow: hidden;
  color: #fff;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;

  &:hover {
    transform: translateY(-5px);
    box-shadow: 0 15px 40px rgba(0, 0, 0, 0.15);
  }

  .stat-icon {
    width: 50px;
    height: 50px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(255, 255, 255, 0.2);
    border-radius: 14px;
    font-size: 24px;
  }

  .stat-info {
    z-index: 1;
  }

  .stat-label {
    font-size: 13px;
    opacity: 0.9;
  }

  .stat-value {
    font-size: 28px;
    font-weight: 700;
  }

  .stat-sub {
    font-size: 12px;
    opacity: 0.8;

    &.up { color: #67f7a7; }
    &.down { color: #ff7b7b; }
  }

  .stat-bg {
    position: absolute;
    right: -10px;
    bottom: -15px;
    font-size: 60px;
    font-weight: 900;
    opacity: 0.1;
    line-height: 1;
  }

  &.gradient-1 {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  }

  &.gradient-2 {
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  }

  &.gradient-3 {
    background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  }

  &.gradient-4 {
    background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
  }
}

.main-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 30px;
  margin-bottom: 30px;
}

.info-section,
.actions-section {
  .section-title {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 18px;
    font-weight: 600;
    color: #2c3e50;
    margin-bottom: 20px;

    .title-icon {
      font-size: 22px;
    }
  }
}

.info-cards {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.info-card {
  background: #fff;
  border-radius: 16px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
  transition: all 0.3s ease;

  &:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.1);
  }

  .card-icon {
    width: 48px;
    height: 48px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 12px;
    color: #fff;
    font-size: 20px;
  }

  .card-label {
    font-size: 13px;
    color: #999;
    margin-bottom: 4px;
  }

  .card-value {
    font-size: 16px;
    font-weight: 600;
    color: #2c3e50;

    &.normal { color: #52c41a; }
    &.disabled { color: #ff4d4f; }
    &.inactive { color: #faad14; }
  }
}

.action-cards {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.action-card {
  background: #fff;
  border-radius: 16px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
  cursor: pointer;
  transition: all 0.3s ease;
  animation: slideIn 0.5s ease backwards;
  animation-delay: var(--delay);

  &:hover {
    transform: translateX(10px);
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
  }

  .action-icon {
    width: 52px;
    height: 52px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 14px;
    color: #fff;
    font-size: 22px;
  }

  .action-content {
    flex: 1;

    .action-title {
      font-size: 16px;
      font-weight: 600;
      color: #2c3e50;
      margin-bottom: 4px;
    }

    .action-desc {
      font-size: 13px;
      color: #999;
    }
  }

  .arrow-icon {
    color: #ddd;
    font-size: 18px;
    transition: all 0.3s ease;
  }

  &:hover .arrow-icon {
    color: #667eea;
    transform: translateX(5px);
  }
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateX(-20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.goods-analysis-section {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 30px;
  margin-bottom: 30px;
}

.goods-card {
  background: #fff;
  border-radius: 20px;
  padding: 24px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
  transition: all 0.3s ease;

  &:hover {
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.1);
  }

  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;

    .header-left {
      display: flex;
      align-items: center;
      gap: 10px;
    }

    .card-icon {
      font-size: 24px;
    }

    .card-title {
      font-size: 18px;
      font-weight: 600;
      color: #2c3e50;
    }

    .card-subtitle {
      font-size: 13px;
      color: #999;
    }
  }

  .goods-list {
    min-height: 200px;

    .empty-state {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding: 40px 0;
      color: #ccc;

      .el-icon {
        font-size: 48px;
        margin-bottom: 10px;
      }

      p {
        font-size: 14px;
      }
    }

    .goods-item {
      display: flex;
      align-items: center;
      gap: 12px;
      padding: 12px;
      border-radius: 12px;
      margin-bottom: 8px;
      background: #f8f9fa;
      transition: all 0.3s ease;

      &:hover {
        background: #f0f2f5;
        transform: translateX(5px);
      }

      &.warning {
        background: linear-gradient(135deg, #fff5f5 0%, #fff0f0 100%);

        &:hover {
          background: linear-gradient(135deg, #ffe8e8 0%, #ffe0e0 100%);
        }
      }

      .goods-rank {
        width: 32px;
        height: 32px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 8px;
        font-weight: 700;
        font-size: 14px;
        background: #e9ecef;
        color: #6c757d;

        &.rank-1 {
          background: linear-gradient(135deg, #ffd700 0%, #ffed4e 100%);
          color: #fff;
        }

        &.rank-2 {
          background: linear-gradient(135deg, #c0c0c0 0%, #e0e0e0 100%);
          color: #fff;
        }

        &.rank-3 {
          background: linear-gradient(135deg, #cd7f32 0%, #e8a868 100%);
          color: #fff;
        }

        &.rank-slow {
          background: linear-gradient(135deg, #ff6b6b 0%, #ff8787 100%);
          color: #fff;
        }
      }

      .goods-info {
        flex: 1;
        min-width: 0;

        .goods-name {
          font-size: 14px;
          font-weight: 500;
          color: #2c3e50;
          white-space: nowrap;
          overflow: hidden;
          text-overflow: ellipsis;
          margin-bottom: 4px;
        }

        .goods-meta {
          display: flex;
          gap: 8px;
          flex-wrap: wrap;

          .brand-tag,
          .barcode-tag {
            font-size: 12px;
            padding: 2px 8px;
            border-radius: 4px;
            background: #e9ecef;
            color: #6c757d;
          }

          .brand-tag {
            background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
            color: #1976d2;
          }
        }
      }

      .goods-data {
        display: flex;
        gap: 16px;

        .data-item {
          display: flex;
          flex-direction: column;
          align-items: flex-end;

          .data-label {
            font-size: 11px;
            color: #999;
            margin-bottom: 2px;
          }

          .data-value {
            font-size: 16px;
            font-weight: 600;
            color: #2c3e50;

            &.primary {
              color: #667eea;
            }

            &.warning {
              color: #ff6b6b;
            }

            &.muted {
              color: #adb5bd;
            }

            &.low {
              color: #faad14;
            }
          }
        }
      }
    }
  }
}

.logout-section {
  display: flex;
  justify-content: center;
}

.logout-btn {
  padding: 16px 48px;
  border-radius: 50px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  color: #fff;
  font-size: 16px;
  font-weight: 600;
  box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
  transition: all 0.3s ease;

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 15px 40px rgba(102, 126, 234, 0.4);
  }

  .el-icon {
    margin-right: 8px;
  }
}
</style>
