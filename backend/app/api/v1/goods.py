"""商品相关 API"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Optional

from app.core.database import get_db
from app.schemas.goods import GoodsStock, GoodsListResponse, HotSalesProduct, SlowMovingProduct
from app.services.goods_service import GoodsService
from app.api.deps import get_current_user

router = APIRouter(prefix="/goods", tags=["商品"])


@router.get("/query/{code}", response_model=GoodsStock, summary="根据编码查询商品")
def get_goods_by_code(
    code: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    根据商品编码或条码查询商品详情

    - **code**: 商品编码（goods_no）或条码（barcode）
    """
    result = GoodsService.get_goods_by_code(db, code)

    if not result:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="商品不存在")

    return GoodsStock(**result)


@router.get("/list", response_model=GoodsListResponse, summary="获取商品列表")
def get_goods_list(
    search: Optional[str] = Query(None, description="通用搜索（商品编号或名称）"),
    goods_no: Optional[str] = Query(None, description="商品编号"),
    name: Optional[str] = Query(None, description="商品名称"),
    material: Optional[str] = Query(None, description="材质"),
    fabric: Optional[str] = Query(None, description="面料"),
    painting: Optional[str] = Query(None, description="工艺"),
    size: Optional[str] = Query(None, description="尺寸"),
    goods_cotegory_id1: Optional[int] = Query(None, description="一级分类ID"),
    goods_cotegory_id2: Optional[int] = Query(None, description="二级分类ID"),
    class_field: Optional[str] = Query(None, description="类别", alias="class"),
    barcode: Optional[str] = Query(None, description="条码"),
    category_id: Optional[int] = Query(None, description="分类ID（兼容旧版）"),
    goods_class: Optional[str] = Query(None, description="商品种类"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    获取商品列表（支持分页和多字段筛选）

    - **search**: 通用搜索（商品编号或名称）
    - **goods_no**: 商品编号
    - **name**: 商品名称
    - **material**: 材质
    - **fabric**: 面料
    - **painting**: 工艺
    - **size**: 尺寸
    - **goods_cotegory_id1**: 一级分类ID
    - **goods_cotegory_id2**: 二级分类ID
    - **class**: 类别
    - **barcode**: 条码
    - **category_id**: 分类ID（兼容旧版）
    - **goods_class**: 商品种类
    - **page**: 页码
    - **page_size**: 每页数量
    """
    result = GoodsService.get_goods_list(
        db=db,
        search=search,
        goods_no=goods_no,
        name=name,
        material=material,
        fabric=fabric,
        painting=painting,
        size=size,
        goods_cotegory_id1=goods_cotegory_id1,
        goods_cotegory_id2=goods_cotegory_id2,
        class_field=class_field,
        barcode=barcode,
        category_id=category_id,
        goods_class=goods_class,
        page=page,
        page_size=page_size
    )
    return GoodsListResponse(**result)


@router.get("/hot", summary="获取热销商品", response_model=list[HotSalesProduct])
def get_hot_goods(
    company_id: Optional[int] = Query(None, description="公司ID"),
    dept_id: Optional[int] = Query(None, description="部门ID"),
    limit: int = Query(5, ge=1, le=50, description="返回数量"),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    获取热销商品（当月销量Top）

    参照原PHP逻辑：
    - 统计当月销售数量 Top5
    - 排除"礼品袋"商品
    - 关联品牌和库存信息
    - 处理退货（order_class != 1 时数量取负）

    - **company_id**: 公司ID（可选）
    - **dept_id**: 部门ID（可选，用于筛选特定仓库）
    - **limit**: 返回商品数量，默认5条

    权限说明：
    - 管理员可以查看所有部门的数据
    - 非管理员只能查看本部门的数据
    """
    # 获取用户的dept_id和is_admin
    actual_dept_id = dept_id
    is_admin = False

    if current_user.user_class == "E":
        employee = db.execute(
            text("SELECT dept_id, admin FROM employee WHERE user_id = :uid"),
            {"uid": current_user.id}
        ).first()

        if employee:
            is_admin = employee[1] == 1
            # 只有非管理员才限制部门
            if not is_admin and not dept_id:
                actual_dept_id = employee[0]

    result = GoodsService.get_hot_goods(db, company_id, actual_dept_id, limit)
    return result


@router.get("/slow", summary="获取滞销商品", response_model=list[SlowMovingProduct])
def get_slow_goods(
    company_id: Optional[int] = Query(None, description="公司ID"),
    dept_id: Optional[int] = Query(None, description="部门ID"),
    limit: int = Query(3, ge=1, le=50, description="返回数量"),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    获取滞销商品（库存>0且入库30天以上，当月无销售）

    参照原PHP逻辑：
    - 库存数量 > 0
    - 入库时间超过 30 天
    - 当月无销售记录
    - 按库存数量降序排列

    - **company_id**: 公司ID（可选）
    - **dept_id**: 部门ID（可选，用于筛选特定仓库）
    - **limit**: 返回商品数量，默认3条

    权限说明：
    - 管理员可以查看所有部门的数据
    - 非管理员只能查看本部门的数据
    """
    # 获取用户的dept_id和is_admin
    actual_dept_id = dept_id
    is_admin = False

    if current_user.user_class == "E":
        employee = db.execute(
            text("SELECT dept_id, admin FROM employee WHERE user_id = :uid"),
            {"uid": current_user.id}
        ).first()

        if employee:
            is_admin = employee[1] == 1
            # 只有非管理员才限制部门
            if not is_admin and not dept_id:
                actual_dept_id = employee[0]

    result = GoodsService.get_slow_goods(db, company_id, actual_dept_id, limit)
    return result


@router.get("/low-stock", summary="获取库存预警商品")
def get_low_stock_goods(
    threshold: int = Query(10, ge=1, description="库存预警阈值"),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    获取库存预警商品（库存低于阈值）

    - **threshold**: 库存预警阈值，默认10

    权限说明：
    - 管理员可以查看所有部门的数据
    - 非管理员只能查看本部门的数据
    """
    # 获取用户的dept_id
    dept_id = None
    if current_user.user_class == "E":
        employee = db.execute(
            text("SELECT dept_id, admin FROM employee WHERE user_id = :uid"),
            {"uid": current_user.id}
        ).first()

        if employee:
            is_admin = employee[1] == 1
            # 只有非管理员才限制部门
            if not is_admin:
                dept_id = employee[0]

    result = GoodsService.get_low_stock_goods(db, threshold, dept_id)
    return {
        "total": len(result),
        "items": result
    }


@router.get("/stats/inventory", summary="获取库存统计")
def get_inventory_stats(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    获取库存统计信息

    返回商品总数、库存充足/不足/缺货数量

    权限说明：
    - 管理员可以查看所有部门的统计
    - 非管理员只能查看本部门的统计
    """
    # 获取用户的dept_id
    dept_id = None
    if current_user.user_class == "E":
        employee = db.execute(
            text("SELECT dept_id, admin FROM employee WHERE user_id = :uid"),
            {"uid": current_user.id}
        ).first()

        if employee:
            is_admin = employee[1] == 1
            # 只有非管理员才限制部门
            if not is_admin:
                dept_id = employee[0]

    return GoodsService.get_inventory_stats(db, dept_id)
