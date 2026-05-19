"""销售统计服务"""
from datetime import datetime, timedelta
from sqlalchemy import text

from sqlalchemy.orm import Session


class StatsService:
    """销售统计服务类"""

    @staticmethod
    def get_sales_stats(db: Session, dept_id: int = None):
        """
        获取销售统计数据

        Args:
            db: 数据库会话
            dept_id: 部门ID（可选，用于过滤特定部门的数据）

        Returns:
            销售统计数据字典
        """
        # 获取当前时间
        now = datetime.now()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        yesterday_start = today_start - timedelta(days=1)
        month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        year_start = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)

        # 构建基础查询条件
        base_where = "WHERE type = 1 AND status >= 9"
        params = {}

        if dept_id:
            base_where += " AND dept_id = :dept_id"
            params["dept_id"] = dept_id

        # 今日销售额和订单数
        today_query = text(f"""
            SELECT COUNT(*) as orders, COALESCE(SUM(totalmoney), 0) as sales
            FROM order_user
            {base_where} AND reg_date >= :today_start
        """)
        today_result = db.execute(today_query, {"today_start": int(today_start.timestamp()), **params}).first()
        today_sales = float(today_result[1]) if today_result else 0
        today_orders = today_result[0] if today_result else 0

        # 昨日销售额
        yesterday_query = text(f"""
            SELECT COALESCE(SUM(totalmoney), 0) as sales
            FROM order_user
            {base_where} AND reg_date >= :yesterday_start AND reg_date < :today_end
        """)
        yesterday_result = db.execute(yesterday_query, {
            "yesterday_start": int(yesterday_start.timestamp()),
            "today_end": int(today_start.timestamp()),
            **params
        }).first()
        yesterday_sales = float(yesterday_result[0]) if yesterday_result else 0

        # 本月销售额
        month_query = text(f"""
            SELECT COALESCE(SUM(totalmoney), 0) as sales
            FROM order_user
            {base_where} AND reg_date >= :month_start
        """)
        month_result = db.execute(month_query, {"month_start": int(month_start.timestamp()), **params}).first()
        month_sales = float(month_result[0]) if month_result else 0

        # 今年销售额
        year_query = text(f"""
            SELECT COALESCE(SUM(totalmoney), 0) as sales
            FROM order_user
            {base_where} AND reg_date >= :year_start
        """)
        year_result = db.execute(year_query, {"year_start": int(year_start.timestamp()), **params}).first()
        year_sales = float(year_result[0]) if year_result else 0

        # 总订单数
        total_query = text(f"SELECT COUNT(*) FROM order_user {base_where}")
        total_result = db.execute(total_query, params).scalar()
        total_orders = total_result or 0

        return {
            "today_sales": today_sales,
            "yesterday_sales": yesterday_sales,
            "month_sales": month_sales,
            "year_sales": year_sales,
            "total_orders": total_orders,
            "today_orders": today_orders,
        }
