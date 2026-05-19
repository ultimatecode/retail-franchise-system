"""销售统计 Schema"""
from pydantic import BaseModel
from typing import Optional


class SalesStats(BaseModel):
    """销售统计 Schema"""
    today_sales: float = 0
    yesterday_sales: float = 0
    month_sales: float = 0
    year_sales: float = 0
    total_orders: int = 0
    today_orders: int = 0
