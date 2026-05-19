"""安全相关 - 密码加密、JWT 生成"""
import base64
import hashlib
from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

# 密码加密上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def encrypt_password_old(password: str) -> str:
    """
    兼容旧系统的密码加密方式
    md5(base64_encode(KEY_BEGIN) . md5(password) . base64_encode(KEY_END))
    """
    key_begin = base64.b64encode(settings.PWD_KEY_BEGIN.encode()).decode()
    key_end = base64.b64encode(settings.PWD_KEY_END.encode()).decode()
    pwd_md5 = hashlib.md5(password.encode()).hexdigest()
    return hashlib.md5(f"{key_begin}{pwd_md5}{key_end}".encode()).hexdigest()


def verify_password_old(plain_password: str, hashed_password: str) -> bool:
    """验证密码（兼容旧系统）"""
    return encrypt_password_old(plain_password) == hashed_password


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """创建 JWT Token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.JWT_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> Optional[dict]:
    """解码 JWT Token"""
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except JWTError:
        return None
