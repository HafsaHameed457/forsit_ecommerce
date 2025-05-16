from fastapi import APIRouter

router = APIRouter()
from fastapi.responses import JSONResponse
from utlis.res import create_success_response, create_error_response
from connections.database import get_db
from controllers.sales import get_sales_records, get_revenue_analysis
from datetime import date
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import Depends

@router.get("/get_sales")
async def get_sales(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    product_id: Optional[str] = None,
    category_id: Optional[str] = None,
    sort: str = "date",
    limit: int = 100,
    page: int = 1,
    db: Session = Depends(get_db)
):
    try:
        data=await get_sales_records(
            {
                "start_date": start_date,
                "end_date": end_date,
                "product_id": product_id,
                "category_id": category_id,
                "sort": sort,
                "limit": limit,
                "page": page
            },
            db
        )
        response_content = create_success_response(
            status_code=200,
            content={
                "message": "Sales records retrieved successfully",
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


@router.get("/revenue-analysis")
async def get_revenue(
    period: str = "monthly",
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    compare_with_previous: bool = False,
    db: Session = Depends(get_db)
):
    try:
        data = await get_revenue_analysis(
            {
                "period": period,
                "start_date": start_date,
                "end_date": end_date,
                "compare_with_previous": compare_with_previous
            },
            db
        )
        response_content = create_success_response(
            status_code=200,
            content={
                "message": "Revenue analysis retrieved successfully",
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
    

