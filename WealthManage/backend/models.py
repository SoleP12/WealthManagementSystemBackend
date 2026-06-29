from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey
from backend.database import Base
from sqlalchemy.orm import relationship
from datetime import datetime, UTC



class WealthManager(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True, index= True)
    name = Column(String, index = True, nullable=False)
    email = Column(String, unique = True, nullable=False)
    hashed_password = Column(String, nullable = False)
    net_worth = Column(Float, default = 0.0)

    reset_tokens = relationship("PasswordResetToken", back_populates="user", cascade="all, delete-orphan")


class PasswordResetToken(Base):
    __tablename__ = "password_reset_tokens"

    id = Column(Integer, primary_key = True, index= True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    token_hash = Column(String(64), unique = True, nullable = False)

    expires_at = Column(DateTime(timezone = True), nullable = False)
    created_at = Column(DateTime(timezone = True), default=lambda: datetime.now(UTC))

    user = relationship("WealthManager", back_populates = "reset_tokens")
    