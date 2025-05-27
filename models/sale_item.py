from sqlalchemy import Column, Integer, String, Float, ForeignKey, func, DateTime, Index
from sqlalchemy.orm import relationship
from connections.database import Base
class SaleItem(Base):
    __tablename__ = "sale_items"
    
    id = Column(String(100), primary_key=True, index=True)
    order_id = Column(String(100), ForeignKey("orders.id"))
    product_id = Column(String(100), ForeignKey("products.id"))
    quantity = Column(Integer)
    selling_price = Column(Float)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    order = relationship("Orders", back_populates="items")
    product = relationship("Product", back_populates="sale_items")
    
    __table_args__ = (
        Index('idx_saleitem_order', order_id),
        Index('idx_saleitem_product', product_id), 
        Index('idx_saleitem_price_quantity', selling_price, quantity),
        Index('idx_saleitem_product_order', product_id, order_id),
    )