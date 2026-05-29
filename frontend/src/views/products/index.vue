<template>
  <div class="products-container">
    <!-- 页面标题 -->
    <div class="page-header">
      <h1 class="page-title">商品与库存管理</h1>
    </div>

    <!-- 功能导航 -->
    <div class="nav-tabs">
      <div
        class="nav-tab"
        :class="{ active: currentTab === 'query' }"
        @click="currentTab = 'query'"
      >
        <div class="tab-icon">🔍</div>
        <div class="tab-text">商品查询</div>
      </div>
      <div
        class="nav-tab"
        :class="{ active: currentTab === 'stockIn' }"
        @click="currentTab = 'stockIn'"
      >
        <div class="tab-icon">📥</div>
        <div class="tab-text">商品入库</div>
      </div>
      <div
        class="nav-tab"
        :class="{ active: currentTab === 'stockOut' }"
        @click="currentTab = 'stockOut'"
      >
        <div class="tab-icon">📤</div>
        <div class="tab-text">商品出库</div>
      </div>
      <div
        class="nav-tab"
        :class="{ active: currentTab === 'inventory' }"
        @click="currentTab = 'inventory'"
      >
        <div class="tab-icon">📦</div>
        <div class="tab-text">库存列表</div>
      </div>
      <div
        class="nav-tab"
        :class="{ active: currentTab === 'check' }"
        @click="currentTab = 'check'"
      >
        <div class="tab-icon">📋</div>
        <div class="tab-text">库存盘点</div>
      </div>
      <div
        class="nav-tab"
        :class="{ active: currentTab === 'history' }"
        @click="currentTab = 'history'"
      >
        <div class="tab-icon">📊</div>
        <div class="tab-text">库存流水</div>
      </div>
    </div>

    <!-- 商品查询模块 -->
    <div v-show="currentTab === 'query'" class="tab-content">
      <div class="search-section">
        <div class="search-box">
          <el-input
            v-model="searchText"
            placeholder="请输入商品规格、编码或名称..."
            clearable
            @keyup.enter="handleSearch"
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
          <el-button type="primary" @click="handleSearch">查询</el-button>
        </div>
      </div>

      <!-- 商品详情 -->
      <div v-if="selectedProduct" class="product-detail">
        <div class="detail-card">
          <div class="detail-image">
            <img :src="selectedProduct.photo || '/placeholder.png'" :alt="selectedProduct.name" />
            <div class="detail-status" :class="selectedProduct.status">
              {{ selectedProduct.status === 'active' ? '在售' : '已下架' }}
            </div>
          </div>
          <div class="detail-info">
            <h2 class="detail-name">{{ selectedProduct.name }}</h2>
            <div class="detail-code">规格：{{ selectedProduct.material || '-' }} / {{ selectedProduct.fabric || '-' }} / {{ selectedProduct.painting || '-' }} / {{ selectedProduct.size || '-' }}</div>
            <div class="detail-grid">
              <div class="grid-item">
                <div class="item-label">价格</div>
                <div class="item-value price">¥{{ selectedProduct.price }}</div>
              </div>
              <div class="grid-item">
                <div class="item-label">库存</div>
                <div class="item-value" :class="getStockClass(selectedProduct.stock)">
                  {{ selectedProduct.stock }} 件
                </div>
              </div>
              <div class="grid-item">
                <div class="item-label">月销</div>
                <div class="item-value">{{ selectedProduct.monthSales || 0 }} 件</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 热销与滞销商品 -->
      <div class="products-sections">
        <!-- 热销商品 -->
        <div class="section-panel hot-panel">
          <div class="section-header">
            <div class="header-left">
              <div class="section-icon">🔥</div>
              <h3 class="section-title">热销商品</h3>
              <span class="section-count">共 {{ hotProducts.length }} 件</span>
            </div>
            <div class="section-tip">本月销量Top商品，建议重点推荐</div>
          </div>
          <div class="products-list">
            <div
              v-for="(product, index) in hotProducts"
              :key="product.id"
              class="product-item"
              @click="selectProduct(product)"
            >
              <div class="item-rank">{{ index + 1 }}</div>
              <div class="item-info">
                <div class="item-name">{{ product.name }}</div>
                <div class="item-spec">
                  {{ product.material || '-' }} / {{ product.fabric || '-' }} / {{ product.painting || '-' }} / {{ product.size || '-' }}
                </div>
              </div>
              <div class="item-price">¥{{ product.price }}</div>
              <div class="item-stock" :class="getStockClass(product.stock)">
                库存: {{ product.stock }}
              </div>
              <div class="item-sales">
                <span class="sales-label">月销</span>
                <span class="sales-value">{{ product.monthSales }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- 滞销商品 -->
        <div class="section-panel slow-panel">
          <div class="section-header">
            <div class="header-left">
              <div class="section-icon">📉</div>
              <h3 class="section-title">滞销商品</h3>
              <span class="section-count">共 {{ slowProducts.length }} 件</span>
            </div>
            <div class="section-tip">本月销量较低，建议促销处理</div>
          </div>
          <div class="products-list">
            <div
              v-for="product in slowProducts"
              :key="product.id"
              class="product-item"
              @click="selectProduct(product)"
            >
              <div class="item-info">
                <div class="item-name">{{ product.name }}</div>
                <div class="item-spec">
                  {{ product.material || '-' }} / {{ product.fabric || '-' }} / {{ product.painting || '-' }} / {{ product.size || '-' }}
                </div>
              </div>
              <div class="item-price">¥{{ product.price }}</div>
              <div class="item-stock" :class="getStockClass(product.stock)">
                库存: {{ product.stock }}
              </div>
              <div class="item-sales low-sales">
                <span class="sales-label">月销</span>
                <span class="sales-value">{{ product.monthSales }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-if="!selectedProduct && !searchText" class="welcome-state">
        <div class="welcome-icon">📦</div>
        <div class="welcome-title">请输入商品规格查询</div>
        <div class="welcome-desc">或点击下方商品查看详情</div>
      </div>

      <div v-if="hasSearched && searchText && !selectedProduct" class="no-result">
        <div class="no-result-text">未找到商品</div>
      </div>
    </div>

    <!-- 库存列表模块 -->
    <div v-show="currentTab === 'inventory'" class="tab-content">
      <!-- 统计卡片 -->
      <div class="stats-row">
        <div class="stat-card">
          <div class="stat-icon" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
            <el-icon><Goods /></el-icon>
          </div>
          <div class="stat-content">
            <div class="stat-label">商品总数</div>
            <div class="stat-value">{{ inventoryStats.total }}</div>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon" style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);">
            <el-icon><Check /></el-icon>
          </div>
          <div class="stat-content">
            <div class="stat-label">库存充足</div>
            <div class="stat-value">{{ inventoryStats.normal }}</div>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon" style="background: linear-gradient(135deg, #faad14 0%, #ffec3d 100%);">
            <el-icon><Warning /></el-icon>
          </div>
          <div class="stat-content">
            <div class="stat-label">库存不足</div>
            <div class="stat-value">{{ inventoryStats.low }}</div>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon" style="background: linear-gradient(135deg, #ff4d4f 0%, #ff7875 100%);">
            <el-icon><Close /></el-icon>
          </div>
          <div class="stat-content">
            <div class="stat-label">已缺货</div>
            <div class="stat-value">{{ inventoryStats.out }}</div>
          </div>
        </div>
      </div>

      <!-- 库存预警 -->
      <div v-if="lowStockProducts.length > 0" class="warning-section">
        <div class="warning-header">
          <div class="warning-icon">⚠️</div>
          <h3 class="warning-title">库存预警商品</h3>
          <span class="warning-count">共 {{ lowStockProducts.length }} 件</span>
        </div>
        <div class="warning-list">
          <div
            v-for="product in lowStockProducts"
            :key="product.id"
            class="warning-item"
            @click="selectProduct(product)"
          >
            <div class="warning-info">
              <div class="warning-name">{{ product.name }}</div>
              <div class="warning-code">{{ product.code }}</div>
            </div>
            <div class="warning-stock">
              仅剩 <span class="stock-num">{{ product.stock }}</span> 件
            </div>
            <el-icon class="warning-arrow"><ArrowRight /></el-icon>
          </div>
        </div>
      </div>

      <!-- 筛选和表格 -->
      <div class="filter-section">
        <el-input
          v-model="inventorySearch"
          placeholder="搜索商品..."
          clearable
          style="width: 300px"
        />
        <el-select v-model="stockFilter" placeholder="库存状态" clearable style="width: 150px">
          <el-option label="正常" value="normal" />
          <el-option label="不足" value="low" />
          <el-option label="缺货" value="out" />
        </el-select>
      </div>

      <div class="inventory-table">
        <el-table :data="filteredInventory" style="width: 100%">
          <el-table-column prop="code" label="编码" width="120" />
          <el-table-column prop="name" label="商品名称" />
          <el-table-column prop="price" label="价格" width="100">
            <template #default="{ row }">
              ¥{{ row.price }}
            </template>
          </el-table-column>
          <el-table-column prop="stock" label="库存" width="100">
            <template #default="{ row }">
              <span :class="getStockClass(row.stock)">{{ row.stock }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="monthSales" label="月销" width="80" />
          <el-table-column label="状态" width="80">
            <template #default="{ row }">
              <el-tag :type="row.status === 'active' ? 'success' : 'info'">
                {{ row.status === 'active' ? '在售' : '下架' }}
              </el-tag>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </div>

    <!-- 商品入库模块 -->
    <div v-show="currentTab === 'stockIn'" class="tab-content">
      <div class="type-cards">
        <div
          v-for="type in stockInTypes"
          :key="type.value"
          class="type-card"
          :class="{ selected: selectedInType === type.value }"
          @click="selectedInType = type.value"
        >
          <div class="type-icon">{{ type.icon }}</div>
          <div class="type-name">{{ type.label }}</div>
        </div>
      </div>

      <div class="stock-form">
        <div class="form-grid">
          <div class="form-item">
            <label>入库单号</label>
            <el-input v-model="stockInForm.billNo" disabled />
          </div>
          <div class="form-item">
            <label>入库日期</label>
            <el-date-picker v-model="stockInForm.date" type="date" style="width: 100%" />
          </div>
        </div>

        <div class="form-section">
          <div class="section-header">
            <h3>商品明细</h3>
            <el-button type="primary" @click="addInItem">
              <el-icon><Plus /></el-icon>
              添加商品
            </el-button>
          </div>

          <div v-if="stockInForm.items.length === 0" class="empty-items">
            <div class="empty-text">请添加入库商品</div>
          </div>

          <el-table v-else :data="stockInForm.items" style="width: 100%">
            <el-table-column label="编码" width="150">
              <template #default="{ row, $index }">
                <el-input
                  v-model="row.code"
                  placeholder="扫码或输入"
                  @blur="findProductByCode(row, 'in')"
                />
              </template>
            </el-table-column>
            <el-table-column prop="productName" label="商品名称" />
            <el-table-column label="数量" width="140">
              <template #default="{ row }">
                <el-input-number v-model="row.quantity" :min="1" :disabled="!row.productId" />
              </template>
            </el-table-column>
            <el-table-column label="单价" width="140">
              <template #default="{ row }">
                <el-input-number v-model="row.price" :min="0" :precision="2" :disabled="!row.productId" />
              </template>
            </el-table-column>
            <el-table-column label="金额" width="120">
              <template #default="{ row }">
                ¥{{ (row.quantity * row.price).toFixed(2) }}
              </template>
            </el-table-column>
            <el-table-column label="操作" width="80">
              <template #default="{ $index }">
                <el-button type="danger" link @click="removeInItem($index)">
                  <el-icon><Delete /></el-icon>
                </el-button>
              </template>
            </el-table-column>
          </el-table>

          <div v-if="stockInForm.items.length > 0" class="form-summary">
            <div class="summary-row">
              <span>入库总数：</span>
              <span>{{ inTotalQty }} 件</span>
            </div>
            <div class="summary-row total">
              <span>入库总额：</span>
              <span class="total-amount">¥{{ inTotalAmount.toFixed(2) }}</span>
            </div>
          </div>
        </div>

        <div class="form-actions">
          <el-button @click="resetStockIn">重置</el-button>
          <el-button type="primary" @click="submitStockIn" :disabled="stockInForm.items.length === 0">
            确认入库
          </el-button>
        </div>
      </div>
    </div>

    <!-- 商品出库模块 -->
    <div v-show="currentTab === 'stockOut'" class="tab-content">
      <div class="type-cards">
        <div
          v-for="type in stockOutTypes"
          :key="type.value"
          class="type-card"
          :class="{ selected: selectedOutType === type.value }"
          @click="selectedOutType = type.value"
        >
          <div class="type-icon">{{ type.icon }}</div>
          <div class="type-name">{{ type.label }}</div>
        </div>
      </div>

      <div class="stock-form">
        <div class="form-grid">
          <div class="form-item">
            <label>出库单号</label>
            <el-input v-model="stockOutForm.billNo" disabled />
          </div>
          <div class="form-item">
            <label>出库日期</label>
            <el-date-picker v-model="stockOutForm.date" type="date" style="width: 100%" />
          </div>
        </div>

        <div class="form-section">
          <div class="section-header">
            <h3>商品明细</h3>
            <el-button type="primary" @click="addOutItem">
              <el-icon><Plus /></el-icon>
              添加商品
            </el-button>
          </div>

          <div v-if="stockOutForm.items.length === 0" class="empty-items">
            <div class="empty-text">请添加出库商品</div>
          </div>

          <el-table v-else :data="stockOutForm.items" style="width: 100%">
            <el-table-column label="编码" width="150">
              <template #default="{ row, $index }">
                <el-input
                  v-model="row.code"
                  placeholder="扫码或输入"
                  @blur="findProductByCode(row, 'out')"
                />
              </template>
            </el-table-column>
            <el-table-column prop="productName" label="商品名称" />
            <el-table-column label="当前库存" width="100">
              <template #default="{ row }">
                <span :class="getStockClass(row.currentStock)">{{ row.currentStock || '-' }}</span>
              </template>
            </el-table-column>
            <el-table-column label="出库数量" width="140">
              <template #default="{ row }">
                <el-input-number
                  v-model="row.quantity"
                  :min="1"
                  :max="row.currentStock || 1"
                  :disabled="!row.productId"
                />
              </template>
            </el-table-column>
            <el-table-column label="操作" width="80">
              <template #default="{ $index }">
                <el-button type="danger" link @click="removeOutItem($index)">
                  <el-icon><Delete /></el-icon>
                </el-button>
              </template>
            </el-table-column>
          </el-table>

          <div v-if="stockOutForm.items.length > 0" class="form-summary">
            <div class="summary-row">
              <span>出库总数：</span>
              <span>{{ outTotalQty }} 件</span>
            </div>
          </div>
        </div>

        <div class="form-actions">
          <el-button @click="resetStockOut">重置</el-button>
          <el-button type="primary" @click="submitStockOut" :disabled="stockOutForm.items.length === 0">
            确认出库
          </el-button>
        </div>
      </div>
    </div>

    <!-- 库存盘点模块 -->
    <div v-show="currentTab === 'check'" class="tab-content">
      <div class="check-section">
        <div class="section-header">
          <h3>盘点任务</h3>
          <el-button type="primary" @click="startNewCheck">
            <el-icon><Plus /></el-icon>
            新建盘点
          </el-button>
        </div>

        <div v-if="!activeCheck" class="task-list">
          <el-empty description="暂无盘点任务" />
        </div>

        <div v-else class="active-check">
          <div class="check-header">
            <el-button @click="activeCheck = null">返回</el-button>
            <span>已盘点：{{ activeCheck.checkedCount }} / {{ activeCheck.totalCount }}</span>
          </div>

          <div class="check-scan">
            <el-input
              v-model="checkScanText"
              placeholder="请扫描商品条码..."
              @keyup.enter="handleCheckScan"
              clearable
            >
              <template #prefix>
                <el-icon><Search /></el-icon>
              </template>
            </el-input>
          </div>

          <div class="check-records">
            <h4>盘点记录</h4>
            <el-table :data="activeCheck.records" style="width: 100%">
              <el-table-column prop="productCode" label="编码" width="120" />
              <el-table-column prop="productName" label="商品名称" />
              <el-table-column prop="systemStock" label="系统库存" width="100" />
              <el-table-column prop="actualStock" label="实际库存" width="100" />
              <el-table-column label="差异" width="100">
                <template #default="{ row }">
                  <span :class="row.systemStock !== row.actualStock ? 'text-danger' : ''">
                    {{ row.actualStock - row.systemStock > 0 ? '+' : '' }}{{ row.actualStock - row.systemStock }}
                  </span>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </div>
      </div>
    </div>

    <!-- 库存流水模块 -->
    <div v-show="currentTab === 'history'" class="tab-content">
      <div class="filter-section">
        <el-select v-model="historyTypeFilter" placeholder="变动类型" clearable style="width: 150px">
          <el-option label="入库" value="in" />
          <el-option label="出库" value="out" />
          <el-option label="盘点" value="check" />
          <el-option label="销售" value="sale" />
        </el-select>
      </div>

      <div class="history-table">
        <el-table :data="filteredHistory" style="width: 100%">
          <el-table-column prop="productCode" label="编码" width="120" />
          <el-table-column prop="productName" label="商品名称" />
          <el-table-column label="类型" width="100">
            <template #default="{ row }">
              <el-tag :type="getHistoryTypeTag(row.type)">
                {{ getHistoryTypeName(row.type) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="变动数量" width="100">
            <template #default="{ row }">
              <span :class="row.quantity > 0 ? 'text-success' : 'text-danger'">
                {{ row.quantity > 0 ? '+' : '' }}{{ row.quantity }}
              </span>
            </template>
          </el-table-column>
          <el-table-column prop="afterStock" label="后库存" width="100" />
          <el-table-column prop="createdAt" label="时间" width="180" />
        </el-table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getGoodsByCode, getGoodsList, getHotGoods, getSlowGoods, getLowStockGoods, getInventoryStats } from '@/api/goods'

const currentTab = ref('query')
const searchText = ref('')
const selectedProduct = ref(null)
const hasSearched = ref(false)  // 标记是否已执行查询

// 库存列表相关
const inventorySearch = ref('')
const stockFilter = ref('')

// 库存盘点相关
const activeCheck = ref(null)
const checkScanText = ref('')

// 库存流水相关
const historyTypeFilter = ref('')

// 入库相关
const selectedInType = ref('purchase')
const stockInTypes = [
  { value: 'purchase', label: '采购入库', icon: '🛒' },
  { value: 'return', label: '退货入库', icon: '🔄' },
  { value: 'transfer', label: '调拨入库', icon: '📦' },
  { value: 'other', label: '其他入库', icon: '📝' }
]
const stockInForm = ref({
  billNo: `IN${Date.now()}`,
  date: new Date(),
  items: []
})

// 出库相关
const selectedOutType = ref('damage')
const stockOutTypes = [
  { value: 'damage', label: '报损出库', icon: '❌' },
  { value: 'return', label: '退货出库', icon: '🔄' },
  { value: 'transfer', label: '调拨出库', icon: '📦' },
  { value: 'other', label: '其他出库', icon: '📝' }
]
const stockOutForm = ref({
  billNo: `OUT${Date.now()}`,
  date: new Date(),
  items: []
})

// 商品数据（从API获取）
const products = ref([])

// 热销商品
const hotProducts = ref([])

// 滞销商品
const slowProducts = ref([])

// 库存预警商品
const lowStockProducts = ref([])

// 库存统计
const inventoryStats = ref({
  total: 0,
  normal: 0,
  low: 0,
  out: 0
})

// 热销商品（月销量Top10）- 兼容旧代码
const hotProductsComputed = computed(() => hotProducts.value)

// 滞销商品（月销量低于5件且库存超过10件）- 兼容旧代码
const slowProductsComputed = computed(() => slowProducts.value)

// 库存预警商品（库存低于10件）- 兼容旧代码
const lowStockProductsComputed = computed(() => lowStockProducts.value)

// 选择商品并跳转到查询页
const selectProduct = (product) => {
  selectedProduct.value = product
}

// 库存流水数据
const stockHistory = ref([
  { id: 1, productName: '可口可乐 500ml', productCode: 'P001', type: 'sale', quantity: -2, afterStock: 120, createdAt: '2026-05-28 14:30:25' },
  { id: 2, productName: '可口可乐 500ml', productCode: 'P001', type: 'in', quantity: 50, afterStock: 122, createdAt: '2026-05-28 10:15:00' }
])

// 过滤后的库存列表
const filteredInventory = computed(() => {
  return products.value.filter(product => {
    const matchSearch = !inventorySearch.value || product.name.includes(inventorySearch.value) || product.code.includes(inventorySearch.value)
    const matchStock = !stockFilter.value ||
      (stockFilter.value === 'normal' && product.stock >= 10) ||
      (stockFilter.value === 'low' && product.stock > 0 && product.stock < 10) ||
      (stockFilter.value === 'out' && product.stock === 0)
    return matchSearch && matchStock
  })
})

// 过滤后的流水记录
const filteredHistory = computed(() => {
  return stockHistory.value.filter(record => {
    const matchType = !historyTypeFilter.value || record.type === historyTypeFilter.value
    return matchType
  })
})

// 入库汇总
const inTotalQty = computed(() => {
  return stockInForm.value.items.reduce((sum, item) => sum + (item.quantity || 0), 0)
})

const inTotalAmount = computed(() => {
  return stockInForm.value.items.reduce((sum, item) => sum + (item.quantity || 0) * (item.price || 0), 0)
})

// 出库汇总
const outTotalQty = computed(() => {
  return stockOutForm.value.items.reduce((sum, item) => sum + (item.quantity || 0), 0)
})

// 获取库存样式
const getStockClass = (stock) => {
  if (stock === 0) return 'stock-out'
  if (stock < 10) return 'stock-low'
  return ''
}

// 搜索商品
const handleSearch = async () => {
  if (!searchText.value.trim()) {
    ElMessage.warning('请输入商品规格、编码或名称')
    return
  }

  hasSearched.value = true  // 标记已执行查询

  try {
    const result = await getGoodsByCode(searchText.value.trim())
    selectedProduct.value = {
      id: result.id,
      name: result.name,
      code: result.code || result.goods_no,
      barcode: result.barcode,
      category_id: result.category_id,
      category_name: result.category_name,
      goods_class: result.goods_class,
      price: result.price,
      cost_price: result.cost_price,
      photo: result.photo,
      material: result.material,
      fabric: result.fabric,
      painting: result.painting,
      size: result.size,
      stop: result.stop,
      show: result.show,
      status: result.status === '通过' ? 'active' : 'inactive',
      property: result.property,
      remark: result.remark,
      stock: result.stock,
      monthSales: result.month_sales || 0
    }
  } catch (error) {
    selectedProduct.value = null
    ElMessage.warning('未找到商品')
  }
}

// 根据编码查找商品
const findProductByCode = (item, type) => {
  if (!item.code || !item.code.trim()) return

  const product = products.value.find(p => p.code === item.code.trim())
  if (!product) {
    ElMessage.warning('未找到商品')
    item.productId = null
    item.productName = ''
    item.currentStock = 0
    return
  }

  item.productId = product.id
  item.productName = product.name
  item.currentStock = product.stock

  if (type === 'in') {
    item.price = product.price
  }
}

// 添加入库商品
const addInItem = () => {
  stockInForm.value.items.push({
    code: '',
    productId: null,
    productName: '',
    quantity: 1,
    price: 0
  })
}

// 移除入库商品
const removeInItem = (index) => {
  stockInForm.value.items.splice(index, 1)
}

// 重置入库单
const resetStockIn = () => {
  stockInForm.value = {
    billNo: `IN${Date.now()}`,
    date: new Date(),
    items: []
  }
}

// 提交入库
const submitStockIn = () => {
  const invalidItem = stockInForm.value.items.find(item => !item.productId || !item.quantity || !item.price)
  if (invalidItem) {
    ElMessage.warning('请完善商品信息')
    return
  }

  ElMessageBox.confirm(
    `确认入库 ${inTotalQty.value} 件商品，总额 ¥${inTotalAmount.value.toFixed(2)}？`,
    '确认入库',
    { type: 'warning' }
  ).then(() => {
    stockInForm.value.items.forEach(item => {
      const product = products.value.find(p => p.id === item.productId)
      if (product) {
        product.stock += item.quantity
      }
      stockHistory.value.unshift({
        id: Date.now(),
        productName: item.productName,
        productCode: item.code,
        type: 'in',
        quantity: item.quantity,
        afterStock: 0,
        createdAt: new Date().toLocaleString()
      })
    })

    ElMessage.success('入库成功')
    resetStockIn()
  }).catch(() => {})
}

// 添加出库商品
const addOutItem = () => {
  stockOutForm.value.items.push({
    code: '',
    productId: null,
    productName: '',
    currentStock: 0,
    quantity: 1
  })
}

// 移除出库商品
const removeOutItem = (index) => {
  stockOutForm.value.items.splice(index, 1)
}

// 重置出库单
const resetStockOut = () => {
  stockOutForm.value = {
    billNo: `OUT${Date.now()}`,
    date: new Date(),
    items: []
  }
}

// 提交出库
const submitStockOut = () => {
  const invalidItem = stockOutForm.value.items.find(item => !item.productId || !item.quantity)
  if (invalidItem) {
    ElMessage.warning('请完善商品信息')
    return
  }

  const outOfStockItem = stockOutForm.value.items.find(item => item.quantity > item.currentStock)
  if (outOfStockItem) {
    ElMessage.warning(`${outOfStockItem.productName} 库存不足`)
    return
  }

  ElMessageBox.confirm(
    `确认出库 ${outTotalQty.value} 件商品？`,
    '确认出库',
    { type: 'warning' }
  ).then(() => {
    stockOutForm.value.items.forEach(item => {
      const product = products.value.find(p => p.id === item.productId)
      if (product) {
        product.stock -= item.quantity
      }
      stockHistory.value.unshift({
        id: Date.now(),
        productName: item.productName,
        productCode: item.code,
        type: 'out',
        quantity: -item.quantity,
        afterStock: 0,
        createdAt: new Date().toLocaleString()
      })
    })

    ElMessage.success('出库成功')
    resetStockOut()
  }).catch(() => {})
}

// 新建盘点
const startNewCheck = () => {
  activeCheck.value = {
    id: Date.now(),
    totalCount: products.value.length,
    checkedCount: 0,
    records: []
  }
}

// 盘点扫码
const handleCheckScan = () => {
  if (!checkScanText.value.trim()) return

  const product = products.value.find(p => p.code === checkScanText.value.trim())
  if (!product) {
    ElMessage.warning('未找到商品')
    return
  }

  const existingRecord = activeCheck.value.records.find(r => r.productId === product.id)
  if (existingRecord) {
    ElMessage.info('该商品已盘点')
    checkScanText.value = ''
    return
  }

  ElMessageBox.prompt('请输入实际库存数量', `盘点：${product.name}`, {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    inputValue: product.stock.toString()
  }).then(({ value }) => {
    const actualStock = parseInt(value)
    activeCheck.value.records.push({
      id: Date.now(),
      productId: product.id,
      productName: product.name,
      productCode: product.code,
      systemStock: product.stock,
      actualStock: actualStock
    })
    activeCheck.value.checkedCount++
    checkScanText.value = ''
    ElMessage.success('已记录')
  }).catch(() => {
    checkScanText.value = ''
  })
}

// 获取流水类型标签样式
const getHistoryTypeTag = (type) => {
  const tagMap = {
    in: 'success',
    out: 'danger',
    check: 'warning',
    sale: 'info'
  }
  return tagMap[type] || 'info'
}

// 获取流水类型名称
const getHistoryTypeName = (type) => {
  const nameMap = {
    in: '入库',
    out: '出库',
    check: '盘点',
    sale: '销售'
  }
  return nameMap[type] || type
}

// 加载热销商品
const loadHotGoods = async () => {
  try {
    const result = await getHotGoods(10)
    hotProducts.value = result.items.map(item => ({
      id: item.id,
      name: item.name,
      code: item.code,
      price: item.price,
      photo: item.photo,
      material: item.material,
      fabric: item.fabric,
      painting: item.painting,
      size: item.size,
      stock: item.stock,
      monthSales: item.month_sales || 0
    }))
  } catch (error) {
    console.error('获取热销商品失败', error)
  }
}

// 加载滞销商品
const loadSlowGoods = async () => {
  try {
    const result = await getSlowGoods(10)
    slowProducts.value = result.items.map(item => ({
      id: item.id,
      name: item.name,
      code: item.code,
      price: item.price,
      photo: item.photo,
      material: item.material,
      fabric: item.fabric,
      painting: item.painting,
      size: item.size,
      stock: item.stock,
      monthSales: item.month_sales || 0
    }))
  } catch (error) {
    console.error('获取滞销商品失败', error)
  }
}

// 加载库存预警商品
const loadLowStockGoods = async () => {
  try {
    const result = await getLowStockGoods(10)
    lowStockProducts.value = result.items.map(item => ({
      id: item.id,
      name: item.name,
      code: item.code,
      price: item.price,
      stock: item.stock
    }))
  } catch (error) {
    console.error('获取库存预警商品失败', error)
  }
}

// 加载库存统计
const loadInventoryStats = async () => {
  try {
    const result = await getInventoryStats()
    inventoryStats.value = result
  } catch (error) {
    console.error('获取库存统计失败', error)
  }
}

onMounted(async () => {
  // 加载商品数据
  await Promise.all([
    loadHotGoods(),
    loadSlowGoods(),
    loadLowStockGoods(),
    loadInventoryStats()
  ])
})
</script>

<style scoped lang="scss">
.products-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #e4e8ec 100%);
  padding: 30px;
}

.page-header {
  margin-bottom: 24px;

  .page-title {
    font-size: 32px;
    font-weight: 700;
    color: #2c3e50;
  }
}

.nav-tabs {
  display: flex;
  gap: 16px;
  margin-bottom: 30px;
  background: #fff;
  padding: 12px;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);

  .nav-tab {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    padding: 16px 24px;
    border-radius: 12px;
    cursor: pointer;
    transition: all 0.3s ease;

    &:hover {
      background: #f5f7fa;
    }

    &.active {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: #fff;
    }

    .tab-icon {
      font-size: 24px;
    }

    .tab-text {
      font-size: 16px;
      font-weight: 600;
    }
  }
}

.tab-content {
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

// 商品查询
.search-section {
  margin-bottom: 30px;

  .search-box {
    background: #fff;
    border-radius: 16px;
    padding: 20px;
    display: flex;
    gap: 16px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);

    .el-input {
      flex: 1;
    }
  }
}

.product-detail {
  margin-bottom: 30px;

  .detail-card {
    background: #fff;
    border-radius: 20px;
    overflow: hidden;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
    display: flex;
  }

  .detail-image {
    width: 280px;
    height: 280px;
    background: linear-gradient(135deg, #f5f7fa 0%, #e4e8ec 100%);
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;

    img {
      width: 100%;
      height: 100%;
      object-fit: cover;
    }

    .detail-status {
      position: absolute;
      top: 16px;
      right: 16px;
      padding: 6px 16px;
      border-radius: 20px;
      font-size: 14px;
      font-weight: 600;

      &.active {
        background: rgba(67, 233, 123, 0.9);
        color: #fff;
      }

      &.inactive {
        background: rgba(250, 112, 154, 0.9);
        color: #fff;
      }
    }
  }

  .detail-info {
    flex: 1;
    padding: 32px;

    .detail-name {
      font-size: 24px;
      font-weight: 700;
      color: #2c3e50;
      margin-bottom: 12px;
    }

    .detail-code {
      font-size: 14px;
      color: #999;
      margin-bottom: 24px;
    }

    .detail-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 24px;

      .grid-item {
        .item-label {
          font-size: 13px;
          color: #999;
          margin-bottom: 8px;
        }

        .item-value {
          font-size: 20px;
          font-weight: 600;
          color: #2c3e50;

          &.price {
            font-size: 24px;
            color: #43e97b;
          }
        }
      }
    }
  }
}

.welcome-state, .no-result {
  text-align: center;
  padding: 80px 20px;

  .welcome-icon {
    font-size: 64px;
    margin-bottom: 16px;
  }

  .welcome-title, .no-result-text {
    font-size: 18px;
    font-weight: 600;
    color: #2c3e50;
  }
}

// 通用样式
.filter-section {
  background: #fff;
  border-radius: 16px;
  padding: 20px;
  margin-bottom: 20px;
  display: flex;
  gap: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
}

.inventory-table, .history-table {
  background: #fff;
  border-radius: 16px;
  padding: 20px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
}

.stock-low {
  color: #faad14;
}

.stock-out {
  color: #ff4d4f;
}

.text-success {
  color: #52c41a;
}

.text-danger {
  color: #ff4d4f;
}

// 统计卡片
.stats-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-bottom: 30px;

  .stat-card {
    background: #fff;
    border-radius: 16px;
    padding: 20px;
    display: flex;
    align-items: center;
    gap: 16px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);

    .stat-icon {
      width: 48px;
      height: 48px;
      display: flex;
      align-items: center;
      justify-content: center;
      border-radius: 12px;
      color: #fff;
      font-size: 20px;
    }

    .stat-content {
      .stat-label {
        font-size: 13px;
        color: #999;
        margin-bottom: 4px;
      }

      .stat-value {
        font-size: 24px;
        font-weight: 700;
        color: #2c3e50;
      }
    }
  }
}

// 热销滞销区域
.products-sections {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
  margin-bottom: 30px;
}

.section-panel {
  background: #fff;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);

  .section-header {
    padding: 20px;
    border-bottom: 1px solid #f0f0f0;
    display: flex;
    justify-content: space-between;
    align-items: center;

    .header-left {
      display: flex;
      align-items: center;
      gap: 12px;

      .section-icon {
        font-size: 24px;
      }

      .section-title {
        font-size: 16px;
        font-weight: 600;
        color: #2c3e50;
      }

      .section-count {
        font-size: 12px;
        color: #999;
        background: #f5f7fa;
        padding: 4px 12px;
        border-radius: 12px;
      }
    }

    .section-tip {
      font-size: 12px;
      color: #999;
    }
  }

  .products-list {
    padding: 16px;
    display: flex;
    flex-direction: column;
    gap: 8px;
    max-height: 400px;
    overflow-y: auto;
  }

  .product-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px;
    border-radius: 12px;
    cursor: pointer;
    transition: all 0.2s ease;

    &:hover {
      background: #f5f7fa;
    }

    .item-rank {
      width: 32px;
      height: 32px;
      display: flex;
      align-items: center;
      justify-content: center;
      background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
      color: #fff;
      font-size: 14px;
      font-weight: 700;
      border-radius: 8px;
      flex-shrink: 0;
    }

    .item-info {
      flex: 1;
      min-width: 0;

      .item-name {
        font-size: 14px;
        font-weight: 500;
        color: #2c3e50;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
      }

      .item-code {
        font-size: 12px;
        color: #999;
      }
    }

    .item-price {
      font-size: 14px;
      font-weight: 600;
      color: #43e97b;
      flex-shrink: 0;
    }

    .item-stock {
      font-size: 12px;
      color: #666;
      flex-shrink: 0;
    }

    .item-sales {
      display: flex;
      flex-direction: column;
      align-items: center;
      flex-shrink: 0;

      .sales-label {
        font-size: 10px;
        color: #999;
      }

      .sales-value {
        font-size: 14px;
        font-weight: 600;
        color: #667eea;
      }

      &.low-sales {
        .sales-value {
          color: #faad14;
        }
      }
    }
  }
}

// 库存预警
.warning-section {
  background: #fff;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
  margin-bottom: 30px;

  .warning-header {
    padding: 16px 20px;
    background: linear-gradient(135deg, #ff9a56 0%, #ff6b6b 100%);
    display: flex;
    align-items: center;
    gap: 12px;

    .warning-icon {
      font-size: 24px;
    }

    .warning-title {
      font-size: 16px;
      font-weight: 600;
      color: #fff;
      flex: 1;
    }

    .warning-count {
      font-size: 12px;
      color: rgba(255, 255, 255, 0.9);
      background: rgba(255, 255, 255, 0.2);
      padding: 4px 12px;
      border-radius: 12px;
    }
  }

  .warning-list {
    padding: 16px 20px;
    display: flex;
    flex-direction: column;
    gap: 12px;
  }

  .warning-item {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 16px;
    background: #fff5f0;
    border-radius: 12px;
    cursor: pointer;
    transition: all 0.2s ease;

    &:hover {
      background: #ffe7d6;
      transform: translateX(4px);
    }

    .warning-info {
      flex: 1;

      .warning-name {
        font-size: 14px;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 4px;
      }

      .warning-code {
        font-size: 12px;
        color: #999;
      }
    }

    .warning-stock {
      font-size: 14px;
      color: #666;

      .stock-num {
        font-size: 18px;
        font-weight: 700;
        color: #ff4d4f;
      }
    }

    .warning-arrow {
      color: #999;
      font-size: 16px;
    }
  }
}

// 入库出库
.type-cards {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-bottom: 30px;

  .type-card {
    background: #fff;
    border-radius: 16px;
    padding: 24px;
    text-align: center;
    cursor: pointer;
    border: 2px solid transparent;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
    transition: all 0.3s ease;

    &:hover {
      transform: translateY(-4px);
      box-shadow: 0 8px 30px rgba(0, 0, 0, 0.1);
    }

    &.selected {
      border-color: #667eea;
    }

    .type-icon {
      font-size: 32px;
      margin-bottom: 12px;
    }

    .type-name {
      font-size: 16px;
      font-weight: 600;
      color: #2c3e50;
    }
  }
}

.stock-form {
  background: #fff;
  border-radius: 20px;
  padding: 30px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
  margin-bottom: 30px;

  .form-item {
    label {
      font-size: 14px;
      font-weight: 500;
      color: #666;
      margin-bottom: 8px;
      display: block;
    }
  }
}

.form-section {
  margin-bottom: 30px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;

  h3 {
    font-size: 18px;
    font-weight: 600;
    color: #2c3e50;
  }
}

.empty-items {
  text-align: center;
  padding: 60px 20px;
  background: #f9fafc;
  border-radius: 12px;

  .empty-text {
    font-size: 14px;
    color: #999;
  }
}

.form-summary {
  margin-top: 20px;
  padding: 20px;
  background: #f9fafc;
  border-radius: 12px;

  .summary-row {
    display: flex;
    justify-content: space-between;
    margin-bottom: 12px;
    font-size: 14px;

    &.total {
      padding-top: 12px;
      border-top: 1px solid #e8e8e8;
      font-size: 16px;
      font-weight: 600;

      .total-amount {
        font-size: 24px;
        color: #43e97b;
      }
    }
  }
}

.form-actions {
  display: flex;
  justify-content: center;
  gap: 16px;
  padding-top: 30px;
  border-top: 1px solid #f0f0f0;
}

// 盘点
.check-section {
  background: #fff;
  border-radius: 20px;
  padding: 30px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);

  .section-header {
    margin-bottom: 30px;
  }
}

.active-check {
  .check-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
    padding-bottom: 20px;
    border-bottom: 1px solid #f0f0f0;
  }

  .check-scan {
    margin-bottom: 30px;
  }

  .check-records {
    h4 {
      font-size: 16px;
      font-weight: 600;
      color: #2c3e50;
      margin-bottom: 16px;
    }
  }
}
</style>
