from sqlalchemy import Column, String, Float, DateTime, func
from sqlalchemy.orm import relationship
from connections.database import Base
class Orders(Base):
    __tablename__ = "orders"
    
    id = Column(String(100), primary_key=True, index=True) 
    sale_date = Column(DateTime, server_default=func.now())
    total_amount = Column(Float)
    
    items = relationship("SaleItem", back_populates="order")