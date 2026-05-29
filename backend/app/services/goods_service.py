"""商品服务"""
from datetime import datetime, timedelta
from sqlalchemy import text, orm
from sqlalchemy.orm import Session
from typing import Optional

from app.schemas.goods import GoodsStock
from app.core.config import settings


def process_image_url(photo: Optional[str]) -> Optional[str]:
    """
    处理图片 URL

    Args:
        photo: 原始图片路径

    Returns:
        处理后的图片 URL
    """
    if not photo:
        return None

    # 如果是外部 URL（以 // 开头），添加 https: 前缀
    if photo.startswith("//"):
        return f"https:{photo}"

    # 如果是相对路径（以 /Uploads/ 开头），使用图片服务器地址
    if photo.startswith("/Uploads/"):
        # 移除开头的 /，然后拼接到图片服务器地址
        path = photo.lstrip("/")
        return f"{settings.IMAGE_BASE_URL}/{path}"

    # 如果已经是完整 URL，直接返回
    if photo.startswith("http://") or photo.startswith("https://"):
        return photo

    return photo


class GoodsService:
    """商品服务类"""

    @staticmethod
    def get_goods_by_code(db: Session, code: str) -> dict:
        """
        根据商品编码查询商品

        Args:
            db: 数据库会话
            code: 商品编码（goods_no 或 barcode）

        Returns:
            商品信息字典
        """
        query = text("""
            SELECT
                g.id,
                g.goods_no,
                g.name,
                g.barcode,
                g.goods_cotegory_id,
                gc.name as category_name,
                g.goods_class,
                g.price,
                g.cost_price,
                g.photo,
                g.material,
                g.fabric,
                g.painting,
                g.size,
                g.stop,
                g.show,
                g.status,
                g.property,
                g.remark,
                COALESCE(SUM(i.count), 0) as stock
            FROM goods g
            LEFT JOIN goods_category1 gc ON g.goods_cotegory_id = gc.id
            LEFT JOIN inventory i ON g.id = i.goods_id AND i.type = 3
            WHERE (g.goods_no = :code OR g.barcode = :code)
            AND g.show = '1'
            AND g.status = '通过'
            GROUP BY g.id
            LIMIT 1
        """)

        result = db.execute(query, {"code": code}).first()

        if not result:
            return None

        # 获取本月销量
        month_start = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        month_sales_query = text("""
            SELECT COALESCE(SUM(odi.absolute_quantity), 0) as total_sales
            FROM order_delivery_item odi
            INNER JOIN order_delivery od ON odi.pid = od.id
            WHERE odi.goods_id = :goods_id
            AND od.status >= 3
            AND od.create_time >= :month_start
        """)
        month_sales_result = db.execute(month_sales_query, {
            "goods_id": result[0],
            "month_start": int(month_start.timestamp())
        }).first()
        month_sales = int(month_sales_result[0]) if month_sales_result else 0

        # 处理图片 URL
        photo = process_image_url(result[9])

        return {
            "id": result[0],
            "code": result[1],
            "name": result[2],
            "barcode": result[3],
            "category_id": result[4],
            "category_name": result[5],
            "goods_class": result[6],
            "price": float(result[7]) if result[7] else 0,
            "cost_price": float(result[8]) if result[8] else 0,
            "photo": photo,
            "material": result[10],
            "fabric": result[11],
            "painting": result[12],
            "size": result[13],
            "stop": result[14],
            "show": result[15],
            "status": result[16],
            "property": result[17],
            "remark": result[18],
            "stock": int(result[19]) if result[19] else 0,
            "month_sales": month_sales
        }

    @staticmethod
    def get_goods_list(
        db: Session,
        search: str = None,
        goods_no: str = None,
        name: str = None,
        material: str = None,
        fabric: str = None,
        painting: str = None,
        size: str = None,
        goods_cotegory_id1: int = None,
        goods_cotegory_id2: int = None,
        class_field: str = None,
        barcode: str = None,
        category_id: int = None,
        goods_class: str = None,
        page: int = 1,
        page_size: int = 20
    ) -> dict:
        """
        获取商品列表

        Args:
            db: 数据库会话
            search: 通用搜索（商品编号或名称）
            goods_no: 商品编号
            name: 商品名称
            material: 材质
            fabric: 面料
            painting: 工艺
            size: 尺寸
            goods_cotegory_id1: 一级分类ID
            goods_cotegory_id2: 二级分类ID
            class_field: 类别
            barcode: 条码
            category_id: 分类ID（兼容旧版）
            goods_class: 商品种类
            page: 页码
            page_size: 每页数量

        Returns:
            商品列表数据
        """
        # 构建查询条件
        where_conditions = ["g.show = '1'", "g.status = '通过'"]
        params = {}

        if search:
            where_conditions.append("(g.goods_no LIKE :search OR g.name LIKE :search)")
            params["search"] = f"%{search}%"

        if goods_no:
            where_conditions.append("g.goods_no LIKE :goods_no")
            params["goods_no"] = f"%{goods_no}%"

        if name:
            where_conditions.append("g.name LIKE :name")
            params["name"] = f"%{name}%"

        if material:
            where_conditions.append("g.material LIKE :material")
            params["material"] = f"%{material}%"

        if fabric:
            where_conditions.append("g.fabric LIKE :fabric")
            params["fabric"] = f"%{fabric}%"

        if painting:
            where_conditions.append("g.painting LIKE :painting")
            params["painting"] = f"%{painting}%"

        if size:
            where_conditions.append("g.size LIKE :size")
            params["size"] = f"%{size}%"

        if goods_cotegory_id1:
            where_conditions.append("g.goods_cotegory_id1 = :goods_cotegory_id1")
            params["goods_cotegory_id1"] = goods_cotegory_id1

        if goods_cotegory_id2:
            where_conditions.append("g.goods_cotegory_id2 = :goods_cotegory_id2")
            params["goods_cotegory_id2"] = goods_cotegory_id2

        if class_field:
            where_conditions.append("g.class = :class_field")
            params["class_field"] = class_field

        if barcode:
            where_conditions.append("g.barcode LIKE :barcode")
            params["barcode"] = f"%{barcode}%"

        if category_id:
            where_conditions.append("g.goods_cotegory_id = :category_id")
            params["category_id"] = category_id

        if goods_class:
            where_conditions.append("g.goods_class = :goods_class")
            params["goods_class"] = goods_class

        where_clause = " AND ".join(where_conditions)

        # 获取总数
        count_query = text(f"""
            SELECT COUNT(DISTINCT g.id)
            FROM goods g
            WHERE {where_clause}
        """)
        total_result = db.execute(count_query, params).scalar()
        total = int(total_result) if total_result else 0

        # 获取分页数据
        offset = (page - 1) * page_size

        query = text(f"""
            SELECT
                g.id,
                g.goods_no,
                g.name,
                g.barcode,
                g.goods_cotegory_id,
                gc.name as category_name,
                g.goods_class,
                g.price,
                g.photo,
                g.stop,
                g.status,
                COALESCE(SUM(i.count), 0) as stock
            FROM goods g
            LEFT JOIN goods_category1 gc ON g.goods_cotegory_id = gc.id
            LEFT JOIN inventory i ON g.id = i.goods_id AND i.type = 3
            WHERE {where_clause}
            GROUP BY g.id
            ORDER BY g.id DESC
            LIMIT :page_size OFFSET :offset
        """)

        results = db.execute(query, {**params, "page_size": page_size, "offset": offset}).fetchall()

        items = []
        month_start = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        for row in results:
            # 获取本月销量
            month_sales_query = text("""
                SELECT COALESCE(SUM(odi.absolute_quantity), 0) as total_sales
                FROM order_delivery_item odi
                INNER JOIN order_delivery od ON odi.pid = od.id
                WHERE odi.goods_id = :goods_id
                AND od.status >= 3
                AND od.create_time >= :month_start
            """)
            month_sales_result = db.execute(month_sales_query, {
                "goods_id": row[0],
                "month_start": int(month_start.timestamp())
            }).first()
            month_sales = int(month_sales_result[0]) if month_sales_result else 0

            # 处理图片 URL
            photo = process_image_url(row[8])

            items.append({
                "id": row[0],
                "code": row[1],
                "name": row[2],
                "barcode": row[3],
                "category_id": row[4],
                "category_name": row[5],
                "goods_class": row[6],
                "price": float(row[7]) if row[7] else 0,
                "photo": photo,
                "stop": row[9],
                "status": row[10],
                "stock": int(row[11]) if row[11] else 0,
                "month_sales": month_sales
            })

        return {
            "total": total,
            "items": items
        }

    @staticmethod
    def get_hot_goods(
        db: Session,
        company_id: int = None,
        dept_id: int = None,
        limit: int = 5
    ) -> list:
        """
        获取热销商品（当月销量Top）
        参照PHP逻辑：统计当月销售数量Top5，排除"礼品袋"商品，关联库存

        Args:
            db: 数据库会话
            company_id: 公司ID
            dept_id: 部门ID
            limit: 返回数量

        Returns:
            热销商品列表
        """
        now = datetime.now()
        month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        month_end = (month_start + timedelta(days=32)).replace(day=1) - timedelta(seconds=1)

        # 构建查询条件
        where_conditions = [
            "ou.type = 1",
            "ou.status BETWEEN 9 AND 15",
            "ou.reg_date >= :month_start",
            "ou.reg_date <= :month_end",
            "oud.goods_name NOT LIKE :exclude_gift"
        ]
        params = {
            "month_start": int(month_start.timestamp()),
            "month_end": int(month_end.timestamp()),
            "exclude_gift": "%礼品袋%"
        }

        if company_id:
            where_conditions.append("ou.company_id = :company_id")
            params["company_id"] = company_id

        if dept_id:
            where_conditions.append("ou.dept_id = :dept_id")
            params["dept_id"] = dept_id

        where_clause = " AND ".join(where_conditions)

        # 热销商品查询（销售数据）
        # 不JOIN inventory，避免重复累加销售数据
        query = text(f"""
            SELECT
                g.id as goods_id,
                g.goods_no,
                g.name as goods_name,
                g.price,
                g.photo,
                g.material,
                g.fabric,
                g.painting,
                g.size,
                g.barcode,
                g.stop,
                g.property,
                b.name as brand_name,
                SUM(IF(ou.order_class != 1, oud.curtom_number * -1, oud.curtom_number)) as sales_quantity,
                SUM(oud.curtom_money) as sales_amount
            FROM order_user_detail oud
            INNER JOIN order_user ou ON oud.pid = ou.id
            INNER JOIN goods g ON oud.goods_id = g.id
            LEFT JOIN brand b ON g.brand_id = b.id
            WHERE {where_clause}
            GROUP BY g.id
            HAVING sales_quantity > 0
            ORDER BY sales_quantity DESC
            LIMIT :limit
        """)

        params["limit"] = limit
        results = db.execute(query, params).fetchall()

        # 获取该部门的仓库列表，用于查询库存
        warehouse_ids = []
        if dept_id:
            warehouse_query = text("SELECT id FROM warehouse WHERE dept_id = :dept_id")
            warehouse_results = db.execute(warehouse_query, {"dept_id": dept_id}).fetchall()
            if warehouse_results:
                warehouse_ids = [w[0] for w in warehouse_results]

        # 获取商品ID列表，用于查询库存
        goods_ids = [row[0] for row in results]

        # 查询库存（单独查询，避免JOIN导致重复）
        stock_map = {}
        if goods_ids:
            warehouse_filter = ""
            if warehouse_ids:
                warehouse_filter = f" AND warehouse_id IN ({','.join(map(str, warehouse_ids))})"

            stock_query = text(f"""
                SELECT goods_id, COALESCE(SUM(count), 0) as stock_count
                FROM inventory
                WHERE goods_id IN ({','.join(map(str, goods_ids))}){warehouse_filter}
                GROUP BY goods_id
            """)
            stock_results = db.execute(stock_query).fetchall()
            stock_map = {row[0]: int(row[1]) for row in stock_results}

        items = []
        for row in results:
            goods_id = row[0]
            goods_no = row[1]
            goods_name = row[2]
            price = float(row[3]) if row[3] else 0
            photo = process_image_url(row[4])
            material = row[5]
            fabric = row[6]
            painting = row[7]
            size = row[8]
            barcode = row[9] if row[9] else ""
            stop = row[10]
            property = row[11] if row[11] else "正常"
            brand_name = row[12]
            sales_quantity = int(row[13]) if row[13] else 0
            sales_amount = float(row[14]) if row[14] else 0
            stock_quantity = stock_map.get(goods_id, 0)

            items.append({
                "id": goods_id,
                "code": goods_no,
                "goods_id": goods_id,
                "goods_no": goods_no,
                "goods_name": goods_name,
                "name": goods_name,
                "price": price,
                "photo": photo,
                "material": material,
                "fabric": fabric,
                "painting": painting,
                "size": size,
                "barcode": barcode,
                "stop": stop,
                "property": property,
                "brand_name": brand_name,
                "sales_quantity": sales_quantity,
                "sales_amount": sales_amount,
                "stock_quantity": stock_quantity,
                "stock": stock_quantity,
                "month_sales": sales_quantity
            })

        return items

    @staticmethod
    def get_slow_goods(
        db: Session,
        company_id: int = None,
        dept_id: int = None,
        limit: int = 3
    ) -> list:
        """
        获取滞销商品（库存>0且入库30天以上，当月无销售）
        参照PHP逻辑：库存>0，入库时间超过30天，当月无销售记录

        Args:
            db: 数据库会话
            company_id: 公司ID
            dept_id: 部门ID
            limit: 返回数量

        Returns:
            滞销商品列表
        """
        now = datetime.now()
        month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        month_end = (month_start + timedelta(days=32)).replace(day=1) - timedelta(seconds=1)
        month_end_date = month_end.strftime('%Y-%m-%d')
        days_30_before = (month_end - timedelta(days=30)).strftime('%Y-%m-%d')

        # 获取当月有销售的商品ID列表
        sales_where = ["ou.type = 1", "ou.status BETWEEN 9 AND 14", "ou.reg_date >= :month_start", "ou.reg_date <= :month_end"]
        sales_params = {"month_start": int(month_start.timestamp()), "month_end": int(month_end.timestamp())}

        if company_id:
            sales_where.append("ou.company_id = :company_id")
            sales_params["company_id"] = company_id

        if dept_id:
            sales_where.append("ou.dept_id = :dept_id")
            sales_params["dept_id"] = dept_id

        sales_query = text(f"""
            SELECT DISTINCT oud.goods_id
            FROM order_user_detail oud
            INNER JOIN order_user ou ON oud.pid = ou.id
            WHERE {' AND '.join(sales_where)}
        """)
        sales_results = db.execute(sales_query, sales_params).fetchall()
        sales_goods_ids = [str(r[0]) for r in sales_results] if sales_results else []

        # 滞销商品查询
        inventory_where = ["i.count > 0"]
        inventory_params = {}

        if dept_id:
            # 获取该部门的所有仓库ID
            warehouse_query = text("SELECT id FROM warehouse WHERE dept_id = :dept_id")
            warehouse_results = db.execute(warehouse_query, {"dept_id": dept_id}).fetchall()
            if warehouse_results:
                warehouse_ids = [str(w[0]) for w in warehouse_results]
                inventory_where.append(f"i.warehouse_id IN ({','.join(warehouse_ids)})")

        # 入库时间超过30天
        inventory_where.append("FROM_UNIXTIME(i.create_date, '%Y-%m-%d') <= :days_30_before")
        inventory_params["days_30_before"] = days_30_before

        # 排除当月有销售的商品
        if sales_goods_ids:
            inventory_where.append(f"i.goods_id NOT IN ({','.join(sales_goods_ids)})")

        query = text(f"""
            SELECT
                g.id as goods_id,
                g.goods_no,
                g.name as goods_name,
                g.price,
                g.photo,
                g.material,
                g.fabric,
                g.painting,
                g.size,
                g.barcode,
                g.stop,
                g.property,
                b.name as brand_name,
                SUM(i.count) as stock_quantity
            FROM inventory i
            INNER JOIN goods g ON i.goods_id = g.id
            LEFT JOIN brand b ON g.brand_id = b.id
            WHERE {' AND '.join(inventory_where)}
            GROUP BY g.id
            ORDER BY stock_quantity DESC
            LIMIT :limit
        """)

        inventory_params["limit"] = limit
        results = db.execute(query, inventory_params).fetchall()

        items = []
        for row in results:
            goods_id = row[0]
            goods_no = row[1]
            goods_name = row[2]
            price = float(row[3]) if row[3] else 0
            photo = process_image_url(row[4])
            material = row[5]
            fabric = row[6]
            painting = row[7]
            size = row[8]
            barcode = row[9] if row[9] else ""
            stop = row[10]
            property = row[11] if row[11] else "正常"
            brand_name = row[12]
            stock_quantity = int(row[13]) if row[13] else 0

            items.append({
                "id": goods_id,
                "code": goods_no,
                "goods_id": goods_id,
                "goods_no": goods_no,
                "goods_name": goods_name,
                "name": goods_name,
                "price": price,
                "photo": photo,
                "material": material,
                "fabric": fabric,
                "painting": painting,
                "size": size,
                "barcode": barcode,
                "stop": stop,
                "property": property,
                "brand_name": brand_name,
                "stock_quantity": stock_quantity,
                "stock": stock_quantity,
                "sales_quantity": 0,
                "sales_amount": 0,
                "month_sales": 0
            })

        return items

    @staticmethod
    def get_low_stock_goods(db: Session, threshold: int = 10, dept_id: int = None) -> list:
        """
        获取库存预警商品

        Args:
            db: 数据库会话
            threshold: 库存阈值
            dept_id: 部门ID（可选，用于筛选特定仓库）

        Returns:
            低库存商品列表
        """
        # 构建WHERE条件
        where_conditions = ["g.show = '1'", "g.stop = 0"]
        params = {"threshold": threshold}

        # 如果指定了部门，筛选该部门的仓库
        if dept_id:
            warehouse_query = text("SELECT id FROM warehouse WHERE dept_id = :dept_id")
            warehouse_results = db.execute(warehouse_query, {"dept_id": dept_id}).fetchall()
            if warehouse_results:
                warehouse_ids = [str(w[0]) for w in warehouse_results]
                where_conditions.append(f"i.warehouse_id IN ({','.join(warehouse_ids)})")

        where_clause = " AND ".join(where_conditions)

        query = text(f"""
            SELECT
                g.id,
                g.goods_no,
                g.name,
                g.price,
                COALESCE(SUM(i.count), 0) as stock
            FROM goods g
            LEFT JOIN inventory i ON g.id = i.goods_id AND i.type = 3
            WHERE {where_clause}
            GROUP BY g.id
            HAVING stock < :threshold AND stock >= 0
            ORDER BY stock ASC
        """)

        results = db.execute(query, params).fetchall()

        return [
            {
                "id": row[0],
                "code": row[1],
                "name": row[2],
                "price": float(row[3]) if row[3] else 0,
                "stock": int(row[4]) if row[4] else 0
            }
            for row in results
        ]

    @staticmethod
    def get_inventory_stats(db: Session, dept_id: int = None) -> dict:
        """
        获取库存统计信息

        Args:
            db: 数据库会话
            dept_id: 部门ID（可选，用于筛选特定仓库）

        Returns:
            库存统计数据
        """
        # 构建WHERE条件
        where_conditions = ["g.show = '1'"]
        params = {}

        # 如果指定了部门，筛选该部门的仓库
        if dept_id:
            warehouse_query = text("SELECT id FROM warehouse WHERE dept_id = :dept_id")
            warehouse_results = db.execute(warehouse_query, {"dept_id": dept_id}).fetchall()
            if warehouse_results:
                warehouse_ids = [str(w[0]) for w in warehouse_results]
                where_conditions.append(f"i.warehouse_id IN ({','.join(warehouse_ids)})")

        where_clause = " AND ".join(where_conditions)

        query = text(f"""
            SELECT
                COUNT(DISTINCT id) as total,
                SUM(CASE WHEN stock >= 10 THEN 1 ELSE 0 END) as normal,
                SUM(CASE WHEN stock > 0 AND stock < 10 THEN 1 ELSE 0 END) as low,
                SUM(CASE WHEN stock = 0 THEN 1 ELSE 0 END) as `out`
            FROM (
                SELECT
                    g.id,
                    COALESCE(SUM(i.count), 0) as stock
                FROM goods g
                LEFT JOIN inventory i ON g.id = i.goods_id AND i.type = 3
                WHERE {where_clause}
                GROUP BY g.id
            ) goods_with_stock
        """)

        result = db.execute(query, params).first()

        return {
            "total": int(result[0]) if result and result[0] else 0,
            "normal": int(result[1]) if result and result[1] else 0,
            "low": int(result[2]) if result and result[2] else 0,
            "out": int(result[3]) if result and result[3] else 0
        }
