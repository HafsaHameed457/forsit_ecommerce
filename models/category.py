from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from connections.database import Base

class Category(Base):
    __tablename__ = "category"
    id = Column(String(100), primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True)
    description = Column(String(255))
    
    products = relationship("Product", back_populates="category")