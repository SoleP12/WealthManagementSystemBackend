from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, func
from backend.database import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime, UTC


class WealthManager(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key =True, index = True)
    full_name: Mapped[str] = mapped_column(String(100), nullable = False)
    email: Mapped[str] = mapped_column(String(200), unique = True, nullable = False)
    hashed_password: Mapped[str] = mapped_column(String(200), nullable = False)
    net_worth: Mapped[float] = mapped_column(Float, nullable = False)
    phone_number: Mapped[str] = mapped_column(String(20), nullable = True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone = True), server_default = func.now(), nullable = False)

    reset_tokens = relationship("PasswordResetToken", back_populates="user", cascade="all, delete-orphan")


class PasswordResetToken(Base):
    __tablename__ = "password_reset_tokens"

    id = Column(Integer, primary_key = True, index= True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    token_hash = Column(String(64), unique = True, nullable = False)

    expires_at = Column(DateTime(timezone = True), nullable = False)
    created_at = Column(DateTime(timezone = True), default=lambda: datetime.now(UTC))

    user = relationship("WealthManager", back_populates = "reset_tokens")
    