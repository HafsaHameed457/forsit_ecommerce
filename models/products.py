from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, func
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

    # These are for create one to many relationship between category and product
    category_id = Column(String(100), ForeignKey("category.id"))
    category = relationship("Category", back_populates="products")
    # These are for create one to one relationship between inventory and product
    inventory = relationship("Inventory", uselist=False, back_populates="product")
    sale_items = relationship("SaleItem", back_populates="product")
    inventory_tracking = relationship("InventoryHistory", back_populates="product")
