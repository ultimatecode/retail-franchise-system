"""认证相关 API"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.core.database import get_db
from app.schemas.user import UserLogin, Token, ApiResponse, UserInfo
from app.services.user_service import UserService
from app.api.deps import get_current_user

router = APIRouter(prefix="/auth", tags=["认证"])


@router.post("/login", response_model=Token, summary="用户登录")
def login(user_login: UserLogin, db: Session = Depends(get_db)):
    """
    用户登录接口

    - **user_login_account**: 登录账号
    - **password**: 密码
    """
    # 验证用户
    success, user, error_msg = UserService.authenticate(
        db,
        user_login.user_login_account,
        user_login.password
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=error_msg or "登录失败",
        )

    # 获取员工信息
    name = None
    dept_id = None
    position_id = None
    position_name = None
    is_admin = False
    if user.user_class == "E":
        from app.models.employee import Employee
        employee = db.query(Employee).filter(Employee.user_id == user.id).first()
        if employee:
            name = employee.name
            dept_id = employee.dept_id
            position_id = employee.position_id
            is_admin = employee.admin == 1
            # 获取职位名称
            position = db.execute(
                text("SELECT name FROM position WHERE id = :pid"),
                {"pid": position_id}
            ).first()
            if position:
                position_name = position[0]

    # 生成 Token
    access_token = UserService.create_token(user)

    # 构建用户信息
    user_dict = {
        "id": user.id,
        "user_login_account": user.user_login_account,
        "user_class": user.user_class,
        "name": name,
        "dept_id": dept_id,
        "position_id": position_id,
        "position_name": position_name,
        "is_admin": is_admin,
        "vip_code": user.vip_code,
        "score": user.score,
        "user_status": user.user_status,
        "level": user.level,
        "last_login_time": user.last_login_time,
        "create_date": user.create_date,
    }

    return Token(
        access_token=access_token,
        user_info=UserInfo(**user_dict)
    )


@router.get("/me", response_model=UserInfo, summary="获取当前用户信息")
def get_current_user_info(current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    """获取当前登录用户信息"""
    # 获取员工信息
    name = None
    dept_id = None
    position_id = None
    position_name = None
    is_admin = False
    if current_user.user_class == "E":
        from app.models.employee import Employee
        employee = db.query(Employee).filter(Employee.user_id == current_user.id).first()
        if employee:
            name = employee.name
            dept_id = employee.dept_id
            position_id = employee.position_id
            is_admin = employee.admin == 1
            # 获取职位名称
            position = db.execute(
                text("SELECT name FROM position WHERE id = :pid"),
                {"pid": position_id}
            ).first()
            if position:
                position_name = position[0]

    user_dict = {
        "id": current_user.id,
        "user_login_account": current_user.user_login_account,
        "user_class": current_user.user_class,
        "name": name,
        "dept_id": dept_id,
        "position_id": position_id,
        "position_name": position_name,
        "is_admin": is_admin,
        "vip_code": current_user.vip_code,
        "score": current_user.score,
        "user_status": current_user.user_status,
        "level": current_user.level,
        "last_login_time": current_user.last_login_time,
        "create_date": current_user.create_date,
    }

    return UserInfo(**user_dict)
