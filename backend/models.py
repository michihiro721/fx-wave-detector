from sqlalchemy import Column, String, Integer, Numeric, DateTime, Boolean, ForeignKey, Text, BigInteger
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
from database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    line_user_id = Column(String(100), unique=True, nullable=False, index=True)
    display_name = Column(String(255))
    picture_url = Column(Text)
    email = Column(String(255))
    line_notifications_enabled = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # リレーション
    wave_alerts = relationship("WaveAlert", back_populates="user")

class FXPrice(Base):
    __tablename__ = "fx_prices"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    pair = Column(String(10), nullable=False, index=True)
    timestamp = Column(DateTime(timezone=True), nullable=False, index=True)
    open_price = Column(Numeric(10, 5))
    high_price = Column(Numeric(10, 5))
    low_price = Column(Numeric(10, 5))
    close_price = Column(Numeric(10, 5))
    volume = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<FXPrice({self.pair}, {self.close_price}, {self.timestamp})>"

class WaveAlert(Base):
    __tablename__ = "wave_alerts"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False, index=True)
    pair = Column(String(10), nullable=False, index=True)
    wave_type = Column(Integer, nullable=False)  # 1,2,3波
    price = Column(Numeric(10, 5))
    timestamp = Column(DateTime(timezone=True), nullable=False)
    sent_at = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String(20), default='sent')  # sent, delivered, read
    
    # リレーション
    user = relationship("User", back_populates="wave_alerts")
    
    def __repr__(self):
        return f"<WaveAlert({self.pair}, Wave{self.wave_type}, {self.price})>"

# 価格データ集計用のビューテーブル（将来的な分析用）
class DailyPriceSummary(Base):
    __tablename__ = "daily_price_summaries"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    pair = Column(String(10), nullable=False, index=True)
    date = Column(DateTime(timezone=True), nullable=False, index=True)
    open_price = Column(Numeric(10, 5))
    high_price = Column(Numeric(10, 5))
    low_price = Column(Numeric(10, 5))
    close_price = Column(Numeric(10, 5))
    volume = Column(BigInteger)
    volatility = Column(Numeric(8, 5))  # ボラティリティ指標
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<DailyPriceSummary({self.pair}, {self.date.date()})>"