
from schemas.inventory import GetInventory,InventoryUpdate
from models import  Product, Category, Inventory
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
        Product.id.label("product_id"),
        Product.name.label("product_name"),
        Product.remaining_items.label("remaining_items"),
        Product.cost_price,
        Category.name.label("category_name"),
        Product.updated_at.label("last_updated")
    ).join(Category, Product.category_id == Category.id)
    
    
    if data.low_stock_only:
        query = query.filter(Product.remaining_items <= 20)
    
    if data.category:
        query = query.filter(Category.name == data.category)
    
    if data.start_date:
        query = query.filter(Inventory.created_at >= data.start_date)
    
    if data.end_date:
        query = query.filter(Inventory.created_at <= data.end_date)

    transactions = query.all()
    print(transactions,'TRANSACTION')

    return serialize_result(transactions)


async def update_inventory_level(
        data: InventoryUpdate,
        db: db_dependency,
):
    try:
        data = InventoryUpdate(**data)
        is_deduction = data.amount < 0
        if data.product_id is None:
            raise ValueError("Product ID is required")
        if data.amount is None:
            raise ValueError("Change amount is required")
        
        product = db.query(Product).filter(Product.id == data.product_id).first()
        
        # Update stock
        product.remaining_items += data.amount

        if product.remaining_items < 0:
            raise ValueError("Cannot have negative stock levels")
        history = Inventory(
            id=str(uuid.uuid4()),
            change_amount=data.amount,
            reason=data.reason if data.reason else ("Stock deduction" if is_deduction else "Stock addition"),
            created_at=datetime.now(),
            product_id=data.product_id,
        )
        
        db.add(history)
        db.commit()
        return {
            "message": "Inventory updated successfully"
        }

    except Exception as e:
        db.rollback()
        print(f"Inventory Update Error: {e}")
        raise e


async def get_history(
        data: GetInventory,
        db: db_dependency,
):
    try:
        data = GetInventory(**data)
        query = db.query(
            Inventory.id,
            Inventory.change_amount,
            Inventory.reason,
            Inventory.created_at,
            Inventory.product_id,
            Product.name.label("product_name"),
            Category.name.label("category_name")
        ).join(Product, Inventory.product_id == Product.id)\
         .outerjoin(Category, Product.category_id == Category.id)

    
        if data.product_id:
            query = query.filter(Inventory.product_id == data.product_id)
        
        if data.start_date:
            query = query.filter(Inventory.created_at >= data.start_date)
        
        if data.end_date:
            query = query.filter(Inventory.created_at <= data.end_date)
        
        result= query.order_by(Inventory.created_at.desc()).all()
        return serialize_result(result)

    except Exception as e:
        print(f"Revenue Analysis Error: {e}")
        raise e
