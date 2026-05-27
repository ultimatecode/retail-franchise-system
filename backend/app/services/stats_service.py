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


class PersonalStatsService:
    """个人销售统计服务类"""

    @staticmethod
    def get_personal_sales_stats(db: Session, emp_id: int = None):
        """
        获取个人销售统计数据

        Args:
            db: 数据库会话
            emp_id: 员工ID

        Returns:
            个人销售统计数据字典
        """
        # 获取当前时间
        now = datetime.now()
        month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        year_start = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        current_year = now.year
        current_month = now.month

        # 初始化统计数据
        month_target = 0
        month_sales = 0
        year_sales = 0

        if emp_id:
            # 从 saleskpi 表获取本月销售目标
            month_kpi_query = text("""
                SELECT kpi
                FROM saleskpi
                WHERE emp_id = :emp_id
                AND year = :year
                AND month = :month
                LIMIT 1
            """)
            month_result = db.execute(month_kpi_query, {
                "emp_id": emp_id,
                "year": current_year,
                "month": current_month
            }).first()
            if month_result and month_result[0]:
                month_target = float(month_result[0])

            # 从 order_sales 和 order_sales_double 表获取本月销售额
            month_sales_query = text("""
                SELECT COALESCE(SUM(sales_amount), 0) as total_sales
                FROM (
                    SELECT COALESCE(os.amount, 0) as sales_amount
                    FROM order_sales os
                    INNER JOIN order_user ou ON os.order_id = ou.id
                    WHERE ou.type = 1 AND ou.status >= 9 AND os.emp_id = :emp_id
                    AND ou.reg_date >= :month_start
                    UNION ALL
                    SELECT COALESCE(osd.amount, 0) as sales_amount
                    FROM order_sales_double osd
                    INNER JOIN order_user ou ON osd.order_id = ou.id
                    WHERE ou.type = 1 AND ou.status >= 9 AND osd.emp_id = :emp_id
                    AND ou.reg_date >= :month_start
                ) combined
            """)
            month_result = db.execute(month_sales_query, {
                "emp_id": emp_id,
                "month_start": int(month_start.timestamp())
            }).first()
            if month_result:
                month_sales = float(month_result[0])

            # 从 order_sales 和 order_sales_double 表获取本年销售额
            year_sales_query = text("""
                SELECT COALESCE(SUM(sales_amount), 0) as total_sales
                FROM (
                    SELECT COALESCE(os.amount, 0) as sales_amount
                    FROM order_sales os
                    INNER JOIN order_user ou ON os.order_id = ou.id
                    WHERE ou.type = 1 AND ou.status >= 9 AND os.emp_id = :emp_id
                    AND ou.reg_date >= :year_start
                    UNION ALL
                    SELECT COALESCE(osd.amount, 0) as sales_amount
                    FROM order_sales_double osd
                    INNER JOIN order_user ou ON osd.order_id = ou.id
                    WHERE ou.type = 1 AND ou.status >= 9 AND osd.emp_id = :emp_id
                    AND ou.reg_date >= :year_start
                ) combined
            """)
            year_result = db.execute(year_sales_query, {
                "emp_id": emp_id,
                "year_start": int(year_start.timestamp())
            }).first()
            if year_result:
                year_sales = float(year_result[0])

        return {
            "month_target": month_target,
            "month_sales": month_sales,
            "year_sales": year_sales,
        }
