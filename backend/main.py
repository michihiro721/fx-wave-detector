
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db, test_db_connection
import asyncio

app = FastAPI(
    title="FX Wave Detector API",
    description="FX第3波検出システムのバックエンドAPI",
    version="1.0.0"
)

# CORS設定（フロントエンドからのアクセス許可）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 開発時は全て許可
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ルートエンドポイント
@app.get("/")
async def root():
    return {
        "message": "FX Wave Detector API へようこそ！",
        "status": "running",
        "version": "1.0.0",
        "endpoints": ["/health", "/api/test"]
    }

# 健康状態チェック
@app.get("/health")
async def health_check():
    # データベース接続テスト
    db_status = await test_db_connection()
    
    return {
        "status": "healthy" if db_status else "unhealthy",
        "service": "fx-wave-detector-backend",
        "message": "バックエンドサービスは正常に動作しています",
        "database": "connected" if db_status else "disconnected"
    }

# テスト用エンドポイント
@app.get("/api/test")
async def test_endpoint():
    return {
        "message": "API接続テスト成功！",
        "data": {
            "timestamp": "2025-01-15 10:00:00",
            "test_value": 12345,
            "connection": "OK"
        }
    }

# データベーステスト用エンドポイント
@app.get("/api/db-test")
async def test_database_operations(db: AsyncSession = Depends(get_db)):
    try:
        # 簡単なクエリ実行テスト
        from sqlalchemy import text
        result = await db.execute(text("SELECT 1 as test_value"))
        test_value = result.scalar()
        
        return {
            "status": "success",
            "message": "データベース操作テスト成功",
            "test_query_result": test_value,
            "database": "operational"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"データベース操作エラー: {str(e)}",
            "database": "error"
        }

# 将来のFX価格エンドポイント（仮）
@app.get("/api/fx/usdjpy")
async def get_usdjpy_price():
    return {
        "pair": "USD/JPY",
        "price": 150.123,
        "timestamp": "2025-01-15 10:00:00",
        "status": "mock_data"
    }
