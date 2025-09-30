from typing import Annotated
from fastapi import Depends, HTTPException, status, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.biz.ai import AIBiz
from app.biz.hero import HeroBiz

# Bearer Token 认证配置（保留以支持swagger文档显示）
security = HTTPBearer()

def get_current_user_id(
    x_user_id: str = Header(..., alias="X-User-ID"),
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> str:
    """从网关解析的header中获取用户ID"""
    if not x_user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID not found in header",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return x_user_id

# 用户ID依赖项
UserIdDep = Annotated[str, Depends(get_current_user_id)]

# 全局 AIBiz 实例，将在应用启动时初始化
_ai_biz_instance = None

def get_ai_biz() -> AIBiz:
    """获取 AIBiz 实例的依赖函数"""
    global _ai_biz_instance
    if _ai_biz_instance is None:
        raise RuntimeError("AIBiz not initialized. Make sure the application has started properly.")
    return _ai_biz_instance

def set_ai_biz_instance(ai_biz: AIBiz):
    """设置全局 AIBiz 实例"""
    global _ai_biz_instance
    _ai_biz_instance = ai_biz

HeroBizDep = Annotated[HeroBiz, Depends(HeroBiz)]
AIBizDep = Annotated[AIBiz, Depends(get_ai_biz)]
