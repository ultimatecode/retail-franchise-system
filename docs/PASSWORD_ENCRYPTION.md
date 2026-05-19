# 密码加密方式

## 现有系统加密算法

```php
md5(base64_encode(C('SITE_ENCRYPTION_KEY_BEGIN')) . md5($str) . base64_encode(C('SITE_ENCRYPTION_KEY_END')))
```

## 加密参数

| 参数 | 值 |
|------|-----|
| SITE_ENCRYPTION_KEY_BEGIN | sunmy_begin |
| SITE_ENCRYPTION_KEY_END | sunmy_end |

## 加密逻辑

1. `base64_encode('sunmy_begin')` = `c3VubXlfYmVnaW4=`
2. `md5($password)` - 原始密码的MD5
3. `base64_encode('sunmy_end')` = `c3VubXlfZW5k=`
4. 三者拼接后再次 MD5

**最终公式：**
```
md5('c3VubXlfYmVnaW4=' + md5($password) + 'c3VubXlfZW5k=')
```

## Python 实现示例

```python
import hashlib
import base64

def encrypt_password(password: str) -> str:
    """
    兼容现有系统的密码加密
    """
    key_begin = base64.b64encode('sunmy_begin'.encode()).decode()
    key_end = base64.b64encode('sunmy_end'.encode()).decode()

    pwd_md5 = hashlib.md5(password.encode()).hexdigest()

    encrypted = hashlib.md5(f"{key_begin}{pwd_md5}{key_end}".encode()).hexdigest()
    return encrypted

# 示例
print(encrypt_password("123456"))
```

## 使用说明

- 新系统用户认证时需要使用此加密方式验证密码
- 用户表: `user`
- 密码字段: `password`
