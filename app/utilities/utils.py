from typing import Dict, Optional
from datetime import datetime
from sqlalchemy import and_, func
from typing_extensions import Any

def apply_filters_ordering_pagination(
        query,
        filters: Dict[str, Any] = None,
        page: Optional[int] = None,
        size: Optional[int] = None,
):
    """
    Applies filters, ordering, and pagination on the provided query.

    :param query: SQLAlchemy query object with model(s)
    :param filters: Dictionary of filters {model.field_name: value}
    :param page: Page number for pagination
    :param size: Page size for pagination
    :return: Tuple (filtered, ordered, paginated results, total count)
    """
    # Apply filters dynamically
    if filters:
        filter_conditions = []
        for key, value in filters.items():
            try:
                if isinstance(value, dict):  # Range filters
                    if "from" in value:
                        from_value = value["from"]
                        if isinstance(from_value, str):  # Check if it's a date string
                            try:
                                from_value = datetime.strptime(from_value, "%Y-%m-%d").date()
                                filter_conditions.append(func.date(key) >= from_value)  # Convert to DATE
                            except ValueError:
                                filter_conditions.append(key >= from_value)  # Use as number or datetime
                        else:
                            filter_conditions.append(key >= from_value)

                    if "to" in value:
                        to_value = value["to"]
                        if isinstance(to_value, str):  # Check if it's a date string
                            try:
                                to_value = datetime.strptime(to_value, "%Y-%m-%d").date()
                                filter_conditions.append(func.date(key) <= to_value)  # Convert to DATE
                            except ValueError:
                                filter_conditions.append(key <= to_value)  # Use as number or datetime
                        else:
                            filter_conditions.append(key <= to_value)

                elif isinstance(value, list):  # IN filter
                    filter_conditions.append(key.in_(value))
                else:  # Exact match
                    filter_conditions.append(key == value)
            except Exception as e:
                print(f"Invalid filter format: {key}, Error: {e}")

        if filter_conditions:
            query = query.filter(and_(*filter_conditions))

    # Get total count before pagination
    total_count = query.count()

    # Apply pagination if needed
    if page and size:
        query = query.limit(size).offset((page - 1) * size)

    result = query.all()

    return result, total_count

