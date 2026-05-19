"""用户模型"""
from sqlalchemy import Column, Integer, String, DateTime, Enum, SmallInteger, Index, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class User(Base):
    """用户表"""
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="用户ID")
    company_id = Column(Integer, nullable=False, comment="公司ID")
    user_login_account = Column(String(255), nullable=False, comment="登录账号")
    password = Column(String(255), nullable=False, comment="密码")
    last_login_time = Column(DateTime, comment="最后登录时间")
    create_date = Column(DateTime, comment="创建时间")
    update_date = Column(DateTime, comment="更新时间")
    user_class = Column(
        Enum("A", "E", "D", "C", "Y", "L", "P"),
        nullable=False,
        default="E",
        comment="用户类型(A:管理员、E:员工、D:设计师、C:客户)",
    )
    vip_code = Column(String(100), comment="贵宾服务卡卡号")
    score = Column(Integer, nullable=False, default=0, comment="用户积分")
    user_status = Column(
        SmallInteger,
        nullable=False,
        default=2,
        comment="用户状态;0:禁用,1:正常,2:未激活",
    )
    wechat_open_id = Column(String(255), comment="微信ID")
    send_code_time = Column(Integer, comment="发送验证码时间")
    send_dept_id = Column(Integer, comment="发送部门ID")
    invite_code = Column(String(255), comment="邀请码")
    up_flg = Column(SmallInteger, nullable=False, default=0, comment="密码更新状态位")
    wx_user_id = Column(Integer, comment="微信用户ID")
    level = Column(Integer, comment="用户等级")

    __table_args__ = (
        Index("account", "user_login_account", unique=True),
        Index("openID", "user_class", "wechat_open_id", unique=True),
        {"comment": "用户表"},
    )

    def to_dict(self):
        """转换为字典"""
        return {
            "id": self.id,
            "company_id": self.company_id,
            "user_login_account": self.user_login_account,
            "user_class": self.user_class,
            "vip_code": self.vip_code,
            "score": self.score,
            "user_status": self.user_status,
            "level": self.level,
            "last_login_time": self.last_login_time.isoformat() if self.last_login_time else None,
            "create_date": self.create_date.isoformat() if self.create_date else None,
        }
