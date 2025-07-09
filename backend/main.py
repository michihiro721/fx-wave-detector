
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# FastAPIアプリケーション作成
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
    return {
        "status": "healthy",
        "service": "fx-wave-detector-backend",
        "message": "バックエンドサービスは正常に動作しています"
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

# 将来のFX価格エンドポイント（仮）
@app.get("/api/fx/usdjpy")
async def get_usdjpy_price():
    return {
        "pair": "USD/JPY",
        "price": 150.123,
        "timestamp": "2025-01-15 10:00:00",
        "status": "mock_data"
    }
