"""API v1 路由"""
from fastapi import APIRouter
from app.api.v1 import auth, stats

api_router = APIRouter()

# 注册认证路由
api_router.include_router(auth.router)
api_router.include_router(stats.router)

# 导入 get_current_user 供其他模块使用
from app.api.deps import get_current_user, get_current_active_user
