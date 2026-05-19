"""FastAPI 主应用"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.v1 import api_router
from app.api.v1.auth import router as auth_router

# 创建 FastAPI 应用
app = FastAPI(
    title=settings.APP_NAME,
    description="Sunday Space零售管理系统 API",
    version="1.0.0",
    debug=settings.DEBUG,
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境需要限制
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(api_router, prefix=settings.API_V1_PREFIX)
app.include_router(auth_router, prefix=settings.API_V1_PREFIX)


@app.get("/", tags=["系统"])
def root():
    """根路径"""
    return {
        "app": settings.APP_NAME,
        "version": "1.0.0",
        "status": "running",
    }


@app.get("/health", tags=["系统"])
def health_check():
    """健康检查"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )
