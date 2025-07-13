from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from decimal import Decimal
import uuid

# ユーザー関連のスキーマ
class UserBase(BaseModel):
    line_user_id: str
    display_name: Optional[str] = None
    picture_url: Optional[str] = None
    email: Optional[str] = None
    line_notifications_enabled: bool = True

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    display_name: Optional[str] = None
    picture_url: Optional[str] = None
    email: Optional[str] = None
    line_notifications_enabled: Optional[bool] = None

class User(UserBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# FX価格データ関連のスキーマ
class FXPriceBase(BaseModel):
    pair: str
    timestamp: datetime
    open_price: Optional[Decimal] = None
    high_price: Optional[Decimal] = None
    low_price: Optional[Decimal] = None
    close_price: Optional[Decimal] = None
    volume: Optional[int] = None

class FXPriceCreate(FXPriceBase):
    pass

class FXPrice(FXPriceBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# 波アラート関連のスキーマ
class WaveAlertBase(BaseModel):
    pair: str
    wave_type: int  # 1,2,3波
    price: Optional[Decimal] = None
    timestamp: datetime

class WaveAlertCreate(WaveAlertBase):
    user_id: uuid.UUID

class WaveAlert(WaveAlertBase):
    id: uuid.UUID
    user_id: uuid.UUID
    sent_at: datetime
    status: str
    
    class Config:
        from_attributes = True

# API レスポンス用のスキーマ
class APIResponse(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None

class PriceResponse(BaseModel):
    pair: str
    price: Decimal
    bid: Decimal
    ask: Decimal
    timestamp: datetime
    spread: Optional[Decimal] = None

# リアルタイムデータ用のスキーマ
class RealtimePriceData(BaseModel):
    pair: str
    prices: List[FXPrice]
    latest_price: Decimal
    change_24h: Optional[Decimal] = None
    volume_24h: Optional[int] = None

# ダウ理論分析結果のスキーマ
class WaveAnalysis(BaseModel):
    pair: str
    timestamp: datetime
    wave_1_detected: bool
    wave_2_detected: bool
    wave_3_detected: bool
    current_trend: str  # "bullish", "bearish", "sideways"
    analysis_confidence: float  # 0.0-1.0
    
class DowTheoryResult(BaseModel):
    pair: str
    analysis: WaveAnalysis
    signals: List[WaveAlert]
    recommendation: str