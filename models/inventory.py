

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func, Index
from sqlalchemy.orm import relationship
from connections.database import Base

class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(String(100), primary_key=True, index=True)
    change_amount = Column(Integer, nullable=False)
    reason = Column(String(255), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    
    product_id = Column(String(100), ForeignKey("products.id"))
    product = relationship("Product", back_populates="inventory")

    __table_args__ = (
        Index('idx_inventory_product_date', product_id, created_at.desc()),
        Index('idx_inventory_change', change_amount),
        Index('idx_inventory_reason', reason, mysql_length=50), 
        Index('idx_product_created_at', "product_id", "created_at"),  
    )


