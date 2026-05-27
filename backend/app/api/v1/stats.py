"""统计相关 API"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.core.database import get_db
from app.schemas.stats import SalesStats, PersonalSalesStats
from app.services.stats_service import StatsService, PersonalStatsService
from app.api.deps import get_current_user

router = APIRouter(prefix="/stats", tags=["统计"])


@router.get("/sales", response_model=SalesStats, summary="获取销售统计")
def get_sales_stats(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    获取销售统计数据

    权限说明：
    - 管理员(employee.admin=1): 可查看所有部门数据
    - 其他用户: 仅可查看本部门数据
    """
    # 获取用户的dept_id和is_admin
    dept_id = None
    is_admin = False

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

    stats = StatsService.get_sales_stats(db, dept_id)
    return SalesStats(**stats)


@router.get("/my-sales", response_model=PersonalSalesStats, summary="获取个人销售数据")
def get_my_sales_stats(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    获取个人销售数据（用于个人信息区域）
    """
    # 获取用户的 emp_id
    emp_id = None

    if current_user.user_class == "E":
        employee = db.execute(
            text("SELECT id FROM employee WHERE user_id = :uid"),
            {"uid": current_user.id}
        ).first()
        if employee:
            emp_id = employee[0]

    stats = PersonalStatsService.get_personal_sales_stats(db, emp_id)
    return PersonalSalesStats(**stats)
