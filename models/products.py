from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, func, Index
from sqlalchemy.orm import relationship
from connections.database import Base

class Product(Base):
    __tablename__ = "products"
    id = Column(String(100), primary_key=True, index=True)
    name = Column(String(100), index=True)
    description = Column(String(255))
    cost_price = Column(Float)
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    
    remaining_items = Column(Integer, default=0)

    # These are for create one to many relationship between category and product
    category_id = Column(String(100), ForeignKey("category.id"))
    category = relationship("Category", back_populates="products")
    # These are for create one to one relationship between inventory and product
    sale_items = relationship("SaleItem", back_populates="product")

    inventory= relationship("Inventory", back_populates="product")
    __table_args__ = (
            Index('idx_product_name', name),
            Index('idx_product_category', category_id), 
            Index('idx_product_stock', remaining_items),  
            Index('idx_product_price', cost_price), 
            Index('idx_product_created_at', created_at),
        )
   

