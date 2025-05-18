from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, func, Index
from sqlalchemy.orm import relationship
from connections.database import Base

class Inventory(Base):
    __tablename__ = "inventory"
    id = Column(String(100), primary_key=True, index=True)
    remaining_items = Column(Integer, default=10)
    last_updated = Column(DateTime, server_default=func.now(), onupdate=func.now())

    product_id = Column(String(100), ForeignKey("products.id"), unique=True)
    product = relationship("Product", back_populates="inventory")

    __table_args__ = (
    Index("idx_inventory_remaining", "remaining_items"),
)
