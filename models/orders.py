from sqlalchemy import Column, String, Float, DateTime, func, Index
from sqlalchemy.orm import relationship
from connections.database import Base
class Orders(Base):
    __tablename__ = "orders"
    
    id = Column(String(100), primary_key=True, index=True) 
    sale_date = Column(DateTime, server_default=func.now())
    total_amount = Column(Float)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    items = relationship("SaleItem", back_populates="order")


    __table_args__ = (
        Index('idx_order_date', sale_date), 
        Index('idx_order_total_amount', total_amount),
        Index('idx_order_date_amount', sale_date, total_amount), 
    )
