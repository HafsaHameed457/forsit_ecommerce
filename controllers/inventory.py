
from schemas.inventory import GetInventory,InventoryUpdate
from models import  Product, Category, Inventory, InventoryHistory
from connections.database import db_dependency
from utlis.common import serialize_result
from datetime import datetime
import uuid

async def get_all_inventory(
    data: GetInventory,
    db: db_dependency,
):
    data = GetInventory(**data)
    
    query = db.query(
        Inventory.product_id,
        Product.name.label("product_name"),
        Inventory.remaining_items.label("remaining_items"),
        Inventory.last_updated,
        # Category.name.label("category_name")
    ).select_from(Inventory)\
     .join(Product, Inventory.product_id == Product.id)\
     .join(Category, Product.category_id == Category.id)
    
    if data.low_stock_only:
        query = query.filter(Inventory.remaining_items <= 20)
    
    if data.category:
        query = query.filter(Category.name == data.category)
    
    if data.start_date:
        query = query.filter(Inventory.last_updated >= data.start_date)
    
    if data.end_date:
        query = query.filter(Inventory.last_updated <= data.end_date)

    transactions = query.all()
    print(transactions,'TRANSACTION')

    return serialize_result(transactions)


async def update_inventory_level(
        data: InventoryUpdate,
        db: db_dependency,
):
    try:
        data = InventoryUpdate(**data)
        if data.product_id is None:
            raise ValueError("Product ID is required")
        if data.change_amount is None:
            raise ValueError("Change amount is required")
        inventory = db.query(Inventory).filter(Inventory.product_id == data.product_id).first()
        
        # Update stock
        inventory.remaining_items += data.change_amount
        inventory.last_updated = datetime.now()
        
        history = InventoryHistory(
            id=str(uuid.uuid4()),
            change_amount=data.change_amount,
            reason=data.reason if data.reason else "Restock",
            changed_at=datetime.now(),
            product_id=data.product_id,
        )
        
        db.add(history)
        db.commit()
    
        return {
            "message": "Inventory updated successfully"
        }

    except Exception as e:
        print(f"Revenue Analysis Error: {e}")
        raise e


async def get_history(
        data: GetInventory,
        db: db_dependency,
):
    try:
        data = GetInventory(**data)
        query = db.query(
            InventoryHistory.id,
            InventoryHistory.change_amount,
            InventoryHistory.reason,
            InventoryHistory.changed_at,
            InventoryHistory.product_id,
            Product.name.label("product_name")
        ).join(Product)

    
        if data.product_id:
            query = query.filter(InventoryHistory.product_id == data.product_id)
        
        if data.start_date:
            query = query.filter(InventoryHistory.changed_at >= data.start_date)
        
        if data.end_date:
            query = query.filter(InventoryHistory.changed_at <= data.end_date)
        
        return query.order_by(InventoryHistory.changed_at.desc()).all()
        
        r

    except Exception as e:
        print(f"Revenue Analysis Error: {e}")
        raise e
