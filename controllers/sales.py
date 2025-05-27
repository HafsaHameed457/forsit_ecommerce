from schemas.sales import GetSalesRecords, SortField
from schemas.revenue import GetRevenueAnalysis
from models import Orders, SaleItem, Product, Category
from connections.database import db_dependency
from utlis.common import serialize_result
from sqlalchemy import func

async def get_sales_records(
    data: GetSalesRecords,
    db: db_dependency,
):
    data=GetSalesRecords(**data)
    query = db.query(
        Orders.id.label("order_id"),
        Orders.sale_date,
        Product.name.label("product_name"),
        Category.name.label("category_name"),
        SaleItem.quantity,
        SaleItem.selling_price.label("unit_price"),
        (SaleItem.quantity * SaleItem.selling_price).label("sales_total_amount"),
        Orders.total_amount.label("order_total"), 
    ).join(SaleItem, Orders.id == SaleItem.order_id
    ).join(Product, SaleItem.product_id == Product.id
    ).join(Category, Product.category_id == Category.id)

    # Date filters
    if 'start_date' in data and data.start_date:
        query = query.filter(Orders.sale_date >= data.start_date)
    if 'end_date' in data and data.end_date:
        query = query.filter(Orders.sale_date <= data.end_date)

    # Product and category filters
    if 'product_id' in data and data.product_id:
        query = query.filter(SaleItem.product_id == data.product_id)
    if 'category_id' in data and data.category_id:
        query = query.filter(Category.id == data.category_id)

    # Sorting
    if 'sort' in data:
        if data.sort == 'date':
            query = query.order_by(Orders.sale_date.desc())
        elif data.sort == 'amount':
            query = query.order_by((SaleItem.quantity * SaleItem.selling_price).desc())
        elif data.sort == 'quantity':
            query = query.order_by(SaleItem.quantity.desc())

    total_records = None
    if 'page' in data and 'limit' in data and data.page and data.limit:
        total_records = query.count()
        query = query.offset((data.page - 1) * data.limit).limit(data.limit)

    results = query.all()

    return {
        "data": serialize_result(results),
        "pagination": {
            "total_records": total_records,
            "current_page": data.page if 'page' in data else 1,
            "per_page": data.limit if 'limit' in data else len(results),
            "total_pages": (total_records // data.limit) + 1 if total_records and 'limit' in data else None
        }
    }



async def get_revenue_analysis(
        data: GetRevenueAnalysis,
        db: db_dependency,
):
    try:
        data = GetRevenueAnalysis(**data)

        valid_periods = ["daily", "weekly", "monthly", "annual"]
        if data.period not in valid_periods:
            raise ValueError(f"Invalid period. Must be one of: {', '.join(valid_periods)}")

        period_map = {
            "daily": func.date(Orders.sale_date),
            "weekly": func.date_sub(Orders.sale_date, func.weekday(Orders.sale_date)),
            "monthly": func.date_format(Orders.sale_date, "%Y-%m-01"),
            "annual": func.date_format(Orders.sale_date, "%Y-01-01")
        }
        period = period_map[data.period]

        query = db.query(
            period.label("period"),
            func.sum(SaleItem.selling_price * SaleItem.quantity).label("gross_revenue"),
            func.sum(Product.cost_price * SaleItem.quantity).label("total_cost"),
            (func.sum(SaleItem.selling_price * SaleItem.quantity) - 
             func.sum(Product.cost_price * SaleItem.quantity)).label("net_revenue"),
            func.count(func.distinct(Orders.id)).label("orders_count"),
            func.sum(SaleItem.quantity).label("items_sold"),
            func.avg(SaleItem.selling_price).label("avg_item_price")
        ).join(SaleItem, Orders.id == SaleItem.order_id
        ).join(Product, SaleItem.product_id == Product.id
        ).group_by("period")


        if data.start_date:
            query = query.filter(Orders.sale_date >= data.start_date)
        if data.end_date:
            query = query.filter(Orders.sale_date <= data.end_date)

        results = query.order_by("period").all()

        response = []
        for row in results:
            gross = float(row.gross_revenue or 0)
            cost = float(row.total_cost or 0)
            net = float(row.net_revenue or 0)
            avg_price = float(row.avg_item_price or 0)
            
            item = {
                "period": row.period.isoformat() if hasattr(row.period, 'isoformat') else str(row.period),
                "gross_revenue": f"{gross:.2f}",
                "total_cost": f"{cost:.2f}",
                "net_revenue": f"{net:.2f}",
                "profit_margin": f"{(net / gross * 100) if gross > 0 else 0:.2f}",
            "orders_count": str(row.orders_count),
            "items_sold": str(row.items_sold),
            "avg_order_value": f"{(gross / row.orders_count) if row.orders_count > 0 else 0:.2f}",
                "avg_item_price": f"{avg_price:.2f}"
            }
            response.append(item)


        if 'compare_with_previous' in data and data.compare_with_previous and len(response) > 1:
            for i in range(1, len(response)):
                prev = response[i-1]
                curr = response[i]
                
                for metric in ["gross_revenue", "net_revenue", "orders_count"]:
                    prev_val = prev[metric]
                    curr_val = curr[metric]
                    if prev_val > 0:
                        growth = round(((curr_val - prev_val) / prev_val) * 100,2)
                        curr[f"growth_{metric}"] = f"{growth:.2f}"
                    else:
                        curr[f"growth_{metric}"] = float('inf') if curr_val > 0 else 0

        return response


    except Exception as e:
        print(f"Revenue Analysis Error: {e}")
        raise e
