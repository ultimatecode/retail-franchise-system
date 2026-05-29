"""商品 Schema"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class GoodsBase(BaseModel):
    """商品基础 Schema"""
    id: int
    goods_no: Optional[str] = None
    name: str
    barcode: Optional[str] = None
    goods_cotegory_id: Optional[int] = None
    goods_class: Optional[str] = None
    price: Optional[float] = None
    cost_price: Optional[float] = None
    photo: Optional[str] = None
    photo1: Optional[str] = None
    material: Optional[str] = None
    fabric: Optional[str] = None
    painting: Optional[str] = None
    size: Optional[str] = None
    stop: Optional[int] = None
    show: Optional[str] = None
    status: Optional[str] = None
    property: Optional[str] = None
    remark: Optional[str] = None

    class Config:
        from_attributes = True


class GoodsStock(GoodsBase):
    """带库存的商品 Schema"""
    stock: Optional[int] = 0
    month_sales: Optional[int] = 0


class GoodsListResponse(BaseModel):
    """商品列表响应"""
    total: int
    items: list[GoodsStock]


class GoodsQueryParams(BaseModel):
    """商品查询参数"""
    search: Optional[str] = None
    goods_no: Optional[str] = None
    name: Optional[str] = None
    material: Optional[str] = None
    fabric: Optional[str] = None
    painting: Optional[str] = None
    size: Optional[str] = None
    goods_cotegory_id1: Optional[int] = None
    goods_cotegory_id2: Optional[int] = None
    class_field: Optional[str] = None
    barcode: Optional[str] = None
    category_id: Optional[int] = None
    goods_class: Optional[str] = None
    page: int = 1
    page_size: int = 20


class HotSalesProduct(BaseModel):
    """热销商品 Schema"""
    id: int
    code: Optional[str] = None
    goods_id: int
    goods_no: Optional[str] = None
    goods_name: str
    name: Optional[str] = None
    price: Optional[float] = None
    photo: Optional[str] = None
    material: Optional[str] = None
    fabric: Optional[str] = None
    painting: Optional[str] = None
    size: Optional[str] = None
    barcode: Optional[str] = None
    brand_name: Optional[str] = None
    sales_quantity: int
    sales_amount: float
    stock_quantity: int
    stock: Optional[int] = None
    month_sales: Optional[int] = None
    status: Optional[str] = None


class SlowMovingProduct(BaseModel):
    """滞销商品 Schema"""
    id: int
    code: Optional[str] = None
    goods_id: int
    goods_no: Optional[str] = None
    goods_name: str
    name: Optional[str] = None
    price: Optional[float] = None
    photo: Optional[str] = None
    material: Optional[str] = None
    fabric: Optional[str] = None
    painting: Optional[str] = None
    size: Optional[str] = None
    barcode: Optional[str] = None
    brand_name: Optional[str] = None
    stock_quantity: int
    stock: Optional[int] = None
    sales_quantity: int = 0
    sales_amount: float = 0
    month_sales: Optional[int] = None
    status: Optional[str] = None
