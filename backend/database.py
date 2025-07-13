from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

# データベースURL（環境変数から取得）
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://fx_user:fx_password@localhost:5432/fx_database")

# 非同期エンジンの作成
engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # SQL文をログ出力（本番環境では False に設定）
    future=True
)

# セッションファクトリーの作成
async_session = sessionmaker(
    engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

# ベースクラスの定義
Base = declarative_base()

# データベースセッションの依存性注入
async def get_db():
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()

# データベース初期化
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# データベース接続テスト
async def test_db_connection():
    try:
        async with engine.begin() as conn:
            await conn.execute("SELECT 1")
        return True
    except Exception as e:
        print(f"データベース接続エラー: {e}")
        return False