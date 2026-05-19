"""员工模型"""
from sqlalchemy import Column, Integer, String, Date, Enum, Text, DateTime
from sqlalchemy.sql import func

from app.core.database import Base


class Employee(Base):
    """员工表"""
    __tablename__ = "employee"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="员工ID")
    company_id = Column(Integer, nullable=False, comment="公司ID")
    user_id = Column(Integer, nullable=False, comment="用户ID")
    user_account = Column(String(50), comment="用户账号")
    name = Column(String(50), nullable=False, comment="姓名")
    gender = Column(Enum("女", "男"), default="女", comment="性别")
    dept_id = Column(Integer, nullable=False, comment="部门ID")
    position_id = Column(Integer, nullable=False, comment="职位ID")
    mobile = Column(String(20), comment="手机号")
    phone = Column(String(20), comment="电话")
    email = Column(String(100), comment="邮箱")
    admin = Column(Integer, default=0, comment="是否管理员")
    deleted = Column(Enum("0", "1"), default="0", comment="删除标记;0:未删除,1:已删除")
    create_date = Column(DateTime, comment="创建时间")
    update_date = Column(DateTime, comment="更新时间")

    __table_args__ = {"comment": "员工表"}
