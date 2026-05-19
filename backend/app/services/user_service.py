"""用户服务"""
from datetime import datetime
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.employee import Employee
from app.core.security import verify_password_old, create_access_token


class UserService:
    """用户服务类"""

    @staticmethod
    def authenticate(db: Session, username: str, password: str) -> tuple[bool, User | None, str | None]:
        """
        验证用户登录

        Args:
            db: 数据库会话
            username: 用户名
            password: 密码

        Returns:
            (是否成功, 用户对象, 错误信息)
        """
        # 查询用户
        user = db.query(User).filter(User.user_login_account == username).first()

        if not user:
            return False, None, "用户不存在"

        # 验证密码
        if not verify_password_old(password, user.password):
            return False, None, "密码错误"

        # 检查用户状态
        if user.user_status == 0:
            return False, None, "账号已被禁用"

        # 如果是员工类型，检查员工表
        if user.user_class == "E":
            employee = db.query(Employee).filter(Employee.user_id == user.id).first()
            if not employee:
                return False, None, "该用户没有员工档案记录"
            if employee.deleted == "1":
                return False, None, "该员工账号已删除"

        # 更新最后登录时间
        user.last_login_time = datetime.now()
        db.commit()

        return True, user, None

    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> User | None:
        """根据ID获取用户"""
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def get_user_with_employee(db: Session, user_id: int):
        """获取用户及员工信息"""
        user = db.query(User).filter(User.id == user_id).first()
        if user and user.user_class == "E":
            employee = db.query(Employee).filter(Employee.user_id == user_id).first()
            return user, employee
        return user, None

    @staticmethod
    def create_token(user: User) -> str:
        """创建用户 Token"""
        data = {
            "user_id": user.id,
            "user_login_account": user.user_login_account,
            "user_class": user.user_class,
        }
        return create_access_token(data)
