from fastapi import APIRouter
router = APIRouter()
from utlis.res import create_success_response, create_error_response
from connections.database import get_db
from controllers.inventory import get_all_inventory,update_inventory_level,get_history
from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import Depends

@router.get("/get_inventory")
async def get_inventory(
    product_id: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    try:
        data=await get_all_inventory(
            {
                "start_date": start_date,
                "end_date": end_date,
                "product_id": product_id
            },
            db
        )
        response_content = create_success_response(
            status_code=200,
            content={
                "message": "All Inventory retrieved successfully",
                "content": data
            }
        )
        
        return  response_content
    except Exception as e:
        print(e)
        response_content = create_error_response(
            error=str(e)
        )
        return response_content


@router.get("/get_low_stock")
async def get_low_stock(
    low_stock_only: bool = True,
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    try:
        data = await get_all_inventory (
            {
    "low_stock_only": low_stock_only,
                "category": category
            },
            db
        )
        response_content = create_success_response(
            status_code=200,
            content={
                "message": "Low stock inventory retrieved successfully",
                "content": data
            }
        )
        
        return response_content
    except Exception as e:
        print(e)
        response_content = create_error_response(
            error=str(e)
        )
        return response_content
    
@router.put("/update_inventory")
async def update_inventory(
    amount: int,
    product_id: str,
    reason:Optional[str] = None,
    db: Session = Depends(get_db)
):
    try:
        data = await update_inventory_level(
            {
                "amount": amount,
                "product_id": product_id,
                "reason": reason
            },
            db
        )
        response_content = create_success_response(
            status_code=200,
            content={
                "message": "Inventory updated successfully",
                "content": data
            }
        )
        
        return response_content
    except Exception as e:
        print(e)
        response_content = create_error_response(
            error=str(e)
        )
        return response_content

@router.get("/inventory_history")
async def get_inventory_history(
    product_id: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    try:
        data = await get_history(
            {
                "product_id": product_id,
                "start_date": start_date,
                "end_date": end_date
            },
            db
        )
        response_content = create_success_response(
            status_code=200,
            content={
                "message": "Inventory history fetched successfully",
                "content": data
            }
        )
        
        return response_content
    except Exception as e:
        print(e)
        response_content = create_error_response(
            error=str(e)
        )
        return response_content