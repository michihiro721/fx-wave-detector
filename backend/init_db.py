"""
データベース初期化スクリプト
Render環境での初回デプロイ時に実行
"""
import asyncio
import os
import logging
from database import init_db, test_db_connection

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    """データベース初期化メイン処理"""
    logger.info("データベース初期化を開始します...")
    
    # 接続テスト
    logger.info("データベース接続をテストしています...")
    if await test_db_connection():
        logger.info("✅ データベース接続成功")
    else:
        logger.error("❌ データベース接続失敗")
        return
    
    # テーブル作成
    try:
        logger.info("テーブルを作成しています...")
        await init_db()
        logger.info("✅ データベース初期化完了")
    except Exception as e:
        logger.error(f"❌ データベース初期化エラー: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())