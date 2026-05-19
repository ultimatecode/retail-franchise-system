"""用户相关 Schema"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    """用户基础 Schema"""
    user_login_account: str = Field(..., description="登录账号")


class UserLogin(UserBase):
    """用户登录 Schema"""
    password: str = Field(..., min_length=1, description="密码")


class UserInfo(BaseModel):
    """用户信息 Schema"""
    id: int
    user_login_account: str
    user_class: str
    name: Optional[str] = None  # 员工姓名
    dept_id: Optional[int] = None  # 部门ID
    position_id: Optional[int] = None  # 职位ID
    position_name: Optional[str] = None  # 职位名称
    is_admin: bool = False  # 是否管理员
    vip_code: Optional[str] = None
    score: int = 0
    user_status: int
    level: Optional[int] = None
    last_login_time: Optional[datetime] = None
    create_date: Optional[datetime] = None

    class Config:
        from_attributes = True


class Token(BaseModel):
    """Token Schema"""
    access_token: str
    token_type: str = "bearer"
    user_info: UserInfo


class TokenData(BaseModel):
    """Token 数据 Schema"""
    user_id: Optional[int] = None
    user_login_account: Optional[str] = None


class ApiResponse(BaseModel):
    """通用响应 Schema"""
    code: int = 200
    message: str = "success"
    data: Optional[dict] = None
