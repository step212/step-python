from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
from sqlmodel import SQLModel

from app.configs.config import settings

# 创建数据库引擎
engine = create_engine(settings.DATABASE_URI.replace('mysql://', 'mysql+pymysql://'))

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 获取数据库会话的依赖函数
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 创建所有表
def init_db():
    SQLModel.metadata.create_all(bind=engine)