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
        (SaleItem.quantity * SaleItem.selling_price).label("total_amount")
    ).join(SaleItem, Orders.id == SaleItem.order_id)\
     .join(Product, SaleItem.product_id == Product.id)\
     .join(Category, Product.category_id == Category.id)
    if data.start_date is not None:
        query = query.filter(Orders.sale_date >= data.start_date)
    if data.end_date is not None:
        query = query.filter(Orders.sale_date <= data.end_date)
    if data.product_id is not None:
        query = query.filter(SaleItem.product_id == data.product_id)
    if data.category_id is not None:
        query = query.filter(Category.id == data.category_id)

    if data.sort == SortField.date:
        query = query.order_by(Orders.sale_date.desc())
    elif data.sort == SortField.amount:
        query = query.order_by((SaleItem.quantity * SaleItem.selling_price).desc())
    elif data.sort == SortField.quantity:
        query = query.order_by(SaleItem.quantity.desc())

    transactions = query.offset((data.page - 1) * data.limit)\
                       .limit(data.limit)\
                       .all()
    print(transactions,'TRANSACTION')

    return serialize_result(transactions)


async def get_revenue_analysis(
        data: GetRevenueAnalysis,
        db: db_dependency,
):
    try:
        data = GetRevenueAnalysis(**data)

        trunc_expr = {
            "daily": func.date(Orders.sale_date),
            "weekly": func.date_sub(Orders.sale_date, func.weekday(Orders.sale_date)),
            "monthly": func.date_format(Orders.sale_date, "%Y-%m-01"),
            "annual": func.date_format(Orders.sale_date, "%Y-01-01")
        }[data.period]

        query = db.query(
            trunc_expr.label("period"),
            func.sum(
                (SaleItem.selling_price * SaleItem.quantity) - 
                (Product.cost_price * SaleItem.quantity)
            ).label("revenue"),
            func.count(Orders.id).label("orders_count")
        ).join(SaleItem, Orders.id == SaleItem.order_id)\
         .join(Product, SaleItem.product_id == Product.id)\
         .group_by("period")

        if data.start_date:
            query = query.filter(Orders.sale_date >= data.start_date)
        if data.end_date:
            query = query.filter(Orders.sale_date <= data.end_date)

        results = query.order_by("period").all()

        response = []
        for row in results:
            revenue = float(row.revenue or 0)
            response.append({
                "period": str(row.period),
                "revenue": revenue,
                "orders_count": row.orders_count
            })

        if data.compare_with_previous:
            for i in range(1, len(response)):
                prev = response[i - 1]
                curr = response[i]
                prev_rev = prev["revenue"]
                curr_rev = curr["revenue"]
                if prev_rev > 0:
                    growth = ((curr_rev - prev_rev) / prev_rev) * 100
                    curr["previous_period_revenue"] = prev_rev
                    curr["growth_percentage"] = round(growth, 2)

        return response

    except Exception as e:
        print(f"Revenue Analysis Error: {e}")
        raise e
