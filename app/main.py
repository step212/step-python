from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.configs.config import settings
from app.routers import ai
from app.data.db import init_db
from app.routers import hero
from app.biz.ai import AIBiz
from app.dependencies import set_ai_biz_instance

# 全局变量存储 AIBiz 实例
ai_biz_instance = None

async def startup_event():
    """应用启动时的初始化"""
    global ai_biz_instance
    
    # 初始化 AIBiz
    ai_biz_instance = AIBiz()
    
    # 初始化 MCP 服务器
    #await ai_biz_instance.initialize_mcp_server()
    
    # 设置到依赖注入中
    set_ai_biz_instance(ai_biz_instance)
    
    print("AIBiz and MCP server initialized successfully")

async def shutdown_event():
    """应用关闭时的清理"""
    global ai_biz_instance
    if ai_biz_instance and ai_biz_instance.mcp_server:
        # 这里可以添加 MCP 服务器的清理逻辑
        print("Cleaning up AIBiz and MCP server")

def get_application():
    # 初始化数据库
    #init_db()

    _app = FastAPI(title=settings.PROJECT_NAME)

    # 添加启动和关闭事件处理器
    _app.add_event_handler("startup", startup_event)
    _app.add_event_handler("shutdown", shutdown_event)

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    _app.include_router(ai.router)
    #_app.include_router(hero.router)

    return _app


app = get_application()
