from sqlalchemy import Column, Integer, String, Float, ForeignKey, func
from sqlalchemy.orm import relationship
from connections.database import Base
class SaleItem(Base):
    __tablename__ = "sale_items"
    
    id = Column(String(100), primary_key=True, index=True)
    order_id = Column(String(100), ForeignKey("orders.id"))
    product_id = Column(String(100), ForeignKey("products.id"))
    quantity = Column(Integer)
    selling_price = Column(Float)
    
    order = relationship("Orders", back_populates="items")
    product = relationship("Product", back_populates="sale_items")
    