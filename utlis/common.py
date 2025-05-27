from datetime import datetime
from decimal import Decimal

def serialize_row(row):
    if hasattr(row, "_asdict"):  # NamedTuple or SQLAlchemy Row
        row = row._asdict()
    elif isinstance(row, dict):
        row = row
    else:
        row = dict(row)

    result = {}
    for key, value in row.items():
        if isinstance(value, datetime):
            result[key] = value.isoformat()
        elif isinstance(value, Decimal):
            result[key] = float(value)
        else:
            result[key] = value
    return result

def serialize_result(rows):
    return [serialize_row(row) for row in rows]


from decimal import Decimal
import json

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)


def serialize_to_json(data):
    return json.dumps(data, cls=DecimalEncoder)
