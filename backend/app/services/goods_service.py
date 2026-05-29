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
    def get_hot_goods(db: Session, limit: int = 10) -> list:
        """
        获取热销商品（本月销量Top）

        Args:
            db: 数据库会话
            limit: 返回数量

        Returns:
            热销商品列表
        """
        month_start = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        query = text("""
            SELECT
                g.id,
                g.goods_no,
                g.name,
                g.price,
                g.photo,
                g.material,
                g.fabric,
                g.painting,
                g.size,
                COALESCE(SUM(i.count), 0) as stock,
                COALESCE(SUM(odi.absolute_quantity), 0) as month_sales
            FROM goods g
            LEFT JOIN inventory i ON g.id = i.goods_id AND i.type = 3
            LEFT JOIN order_delivery_item odi ON g.id = odi.goods_id
            LEFT JOIN order_delivery od ON odi.pid = od.id
                AND od.status >= 3
                AND od.create_time >= :month_start
            WHERE g.show = '1' AND g.stop = 0
            GROUP BY g.id
            HAVING month_sales > 0
            ORDER BY month_sales DESC
            LIMIT :limit
        """)

        results = db.execute(query, {
            "month_start": int(month_start.timestamp()),
            "limit": limit
        }).fetchall()

        items = []
        for row in results:
            # 处理图片 URL
            photo = process_image_url(row[4])
            items.append({
                "id": row[0],
                "code": row[1],
                "name": row[2],
                "price": float(row[3]) if row[3] else 0,
                "photo": photo,
                "material": row[5],
                "fabric": row[6],
                "painting": row[7],
                "size": row[8],
                "stock": int(row[9]) if row[9] else 0,
                "month_sales": int(row[10]) if row[10] else 0
            })

        return items

    @staticmethod
    def get_slow_goods(db: Session, limit: int = 10) -> list:
        """
        获取滞销商品（低销量高库存）

        Args:
            db: 数据库会话
            limit: 返回数量

        Returns:
            滞销商品列表
        """
        month_start = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        query = text("""
            SELECT
                g.id,
                g.goods_no,
                g.name,
                g.price,
                g.photo,
                g.material,
                g.fabric,
                g.painting,
                g.size,
                COALESCE(SUM(i.count), 0) as stock,
                COALESCE(SUM(odi.absolute_quantity), 0) as month_sales
            FROM goods g
            LEFT JOIN inventory i ON g.id = i.goods_id AND i.type = 3
            LEFT JOIN order_delivery_item odi ON g.id = odi.goods_id
            LEFT JOIN order_delivery od ON odi.pid = od.id
                AND od.status >= 3
                AND od.create_time >= :month_start
            WHERE g.show = '1' AND g.stop = 0
            GROUP BY g.id
            HAVING stock > 10 AND (month_sales IS NULL OR month_sales < 5)
            ORDER BY month_sales ASC
            LIMIT :limit
        """)

        results = db.execute(query, {
            "month_start": int(month_start.timestamp()),
            "limit": limit
        }).fetchall()

        items = []
        for row in results:
            # 处理图片 URL
            photo = process_image_url(row[4])
            items.append({
                "id": row[0],
                "code": row[1],
                "name": row[2],
                "price": float(row[3]) if row[3] else 0,
                "photo": photo,
                "material": row[5],
                "fabric": row[6],
                "painting": row[7],
                "size": row[8],
                "stock": int(row[9]) if row[9] else 0,
                "month_sales": int(row[10]) if row[10] else 0
            })

        return items

    @staticmethod
    def get_low_stock_goods(db: Session, threshold: int = 10) -> list:
        """
        获取库存预警商品

        Args:
            db: 数据库会话
            threshold: 库存阈值

        Returns:
            低库存商品列表
        """
        query = text("""
            SELECT
                g.id,
                g.goods_no,
                g.name,
                g.price,
                COALESCE(SUM(i.count), 0) as stock
            FROM goods g
            LEFT JOIN inventory i ON g.id = i.goods_id AND i.type = 3
            WHERE g.show = '1' AND g.stop = 0
            GROUP BY g.id
            HAVING stock < :threshold AND stock >= 0
            ORDER BY stock ASC
        """)

        results = db.execute(query, {"threshold": threshold}).fetchall()

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
    def get_inventory_stats(db: Session) -> dict:
        """
        获取库存统计信息

        Args:
            db: 数据库会话

        Returns:
            库存统计数据
        """
        query = text("""
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
                WHERE g.show = '1'
                GROUP BY g.id
            ) goods_with_stock
        """)

        result = db.execute(query).first()

        return {
            "total": int(result[0]) if result[0] else 0,
            "normal": int(result[1]) if result[1] else 0,
            "low": int(result[2]) if result[2] else 0,
            "out": int(result[3]) if result[3] else 0
        }
