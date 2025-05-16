from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func, Index
from sqlalchemy.orm import relationship
from connections.database import Base

class InventoryHistory(Base):
    __tablename__ = "inventory_history"

    id = Column(String(100), primary_key=True, index=True)
    change_amount = Column(Integer, nullable=False)
    reason = Column(String(255), nullable=True)
    changed_at = Column(DateTime, server_default=func.now())
    product_id = Column(String(100), ForeignKey("products.id"))
    product = relationship("Product", back_populates="inventory_tracking")
    __table_args__ = (
        Index("idx_product_changed_at", "product_id", "changed_at"),
    )


