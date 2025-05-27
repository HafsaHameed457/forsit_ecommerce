from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, func, Index
from sqlalchemy.orm import relationship
from connections.database import Base

class Category(Base):
    __tablename__ = "category"
    id = Column(String(100), primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True)
    description = Column(String(255))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    products = relationship("Product", back_populates="category")
    __table_args__ = (
        Index('idx_category_description', description, mysql_length=100),  # Partial index for description
        Index('idx_category_created_at', created_at),  # For time-based queries
    )