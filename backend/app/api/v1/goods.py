"""商品相关 API"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.core.database import get_db
from app.schemas.goods import GoodsStock, GoodsListResponse
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


@router.get("/hot", summary="获取热销商品")
def get_hot_goods(
    limit: int = Query(10, ge=1, le=50, description="返回数量"),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    获取热销商品（按本月销量排序）

    - **limit**: 返回商品数量，默认10条
    """
    result = GoodsService.get_hot_goods(db, limit)
    return {
        "total": len(result),
        "items": result
    }


@router.get("/slow", summary="获取滞销商品")
def get_slow_goods(
    limit: int = Query(10, ge=1, le=50, description="返回数量"),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    获取滞销商品（低销量且库存充足）

    - **limit**: 返回商品数量，默认10条
    """
    result = GoodsService.get_slow_goods(db, limit)
    return {
        "total": len(result),
        "items": result
    }


@router.get("/low-stock", summary="获取库存预警商品")
def get_low_stock_goods(
    threshold: int = Query(10, ge=1, description="库存预警阈值"),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    获取库存预警商品（库存低于阈值）

    - **threshold**: 库存预警阈值，默认10
    """
    result = GoodsService.get_low_stock_goods(db, threshold)
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
    """
    return GoodsService.get_inventory_stats(db)
