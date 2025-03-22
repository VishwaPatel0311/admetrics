import random
from datetime import datetime, timedelta

import constants
import db
from core import create_response
from db import Base, engine
from models import *
from utilities import apply_filters_ordering_pagination


def insert_dummy_ad_metrics_data(db):
    try:
        Base.metadata.create_all(engine)
        # Insert dummy data into dimension tables
        age_groups = ["18-24", "25-34", "35-44", "45-54", "55+"]
        dates = [datetime.now() - timedelta(days=i) for i in range(10)]
        device_types = ["Mobile", "Tablet", "Desktop"]
        genders = ["Male", "Female", "Other"]
        placements = ["Feed", "Story", "Search"]
        platforms = ["Facebook", "Instagram", "Google"]
        regions = ["North", "South", "East", "West"]
        # Insert data into tables
        for i, age in enumerate(age_groups, start=1):
            db.add(DimAgeGroupModel(age_id=i, age_range=age))
        for i, date in enumerate(dates, start=1):
            db.add(DimDateModel(date_id=i, date_value=date))
        for i, device in enumerate(device_types, start=1):
            db.add(DimDeviceTypeModel(device_type_id=i, device_type_name=device))
        for i, gender in enumerate(genders, start=1):
            db.add(DimGenderModel(gender_id=i, gender_name=gender))
        for i, placement in enumerate(placements, start=1):
            db.add(DimPlacementModel(placement_id=i, placement_name=placement))
        for i, platform in enumerate(platforms, start=1):
            db.add(DimPlatformModel(platform_id=i, platform_name=platform))
        for i, region in enumerate(regions, start=1):
            db.add(DimRegionModel(region_id=i, region_name=region))

        db.flush()

        # Insert 100 records into fact_ad_metrics_daily
        for _ in range(1000):
            record = FactAdMetricsDailyModel(
                date_id=random.randint(1, len(dates)),
                region_id=random.randint(1, len(regions)),
                age_id=random.randint(1, len(age_groups)),
                gender_id=random.randint(1, len(genders)),
                platform_id=random.randint(1, len(platforms)),
                placement_id=random.randint(1, len(placements)),
                device_type_id=random.randint(1, len(device_types)),
                impressions=random.randint(1000, 10000),
                clicks=random.randint(50, 500),
                cost=round(random.uniform(10, 500), 2),
                conversions=random.randint(1, 50),
                likes=random.randint(10, 1000)
            )
            db.add(record)

        db.commit()
        db.close()

        return create_response({"message": "Dummy data inserted successfully!"})
    except Exception as e:
        print(f"Exception occurred in insert_dummy_ad_metrics_data: {str(e)}")
        raise e


def get_ad_metrics_data(db, filters, page, size):
    """
    Queries and formats data for Ad metrics.
    @param db:
    @param filters:
    @param page:
    @param size:
    @return:
    """
    try:
        filter_dict = {
            "region_id": DimRegionModel.region_id,
            "age_id": DimAgeGroupModel.age_id,
            "gender_id": DimGenderModel.gender_id,
            "platform_id": DimPlatformModel.platform_id,
            "placement_id": DimPlacementModel.placement_id,
            "min_impression": FactAdMetricsDailyModel.impressions,
            "max_impression": FactAdMetricsDailyModel.impressions,
            "min_clicks": FactAdMetricsDailyModel.clicks,
            "max_clicks": FactAdMetricsDailyModel.clicks,
            "min_cost": FactAdMetricsDailyModel.cost,
            "max_cost": FactAdMetricsDailyModel.cost,
            "min_conversions": FactAdMetricsDailyModel.conversions,
            "max_conversions": FactAdMetricsDailyModel.conversions,
            "min_likes": FactAdMetricsDailyModel.likes,
            "max_likes": FactAdMetricsDailyModel.likes,
            "start_date": DimDateModel.date_value,
            "end_date": DimDateModel.date_value
        }
        filter_data = dict()

        if filters:
            filters = eval(filters)
            for filter_key, value in filters.items():
                if filter_key in filter_dict:
                    column = filter_dict[filter_key]

                    if filter_key in ["start_date", "end_date"]:
                        try:
                            date_value = datetime.strptime(value, "%Y-%m-%d").date()  # Convert string to date
                            if filter_key == "start_date":
                                filter_data[column] = {"from": date_value}
                            else:
                                if column in filter_data:
                                    filter_data[column]["to"] = date_value
                                else:
                                    filter_data[column] = {"to": date_value}
                        except ValueError:
                            print(f"Invalid date format for {filter_key}: {value}")
                    # Handle range filters
                    elif filter_key.startswith("min_"):
                        filter_data[column] = {"from": value}
                    elif filter_key.startswith("max_"):
                        if column in filter_data:
                            filter_data[column]["to"] = value
                        else:
                            filter_data[column] = {"to": value}
                    else:
                        filter_data[column] = value  # Exact match or `IN` condition

        # Base query with LEFT JOINs
        query = (db.query(
                FactAdMetricsDailyModel,
                DimRegionModel.region_name.label("region_name"),
                DimGenderModel.gender_name.label("gender_name"),
                DimPlatformModel.platform_name.label("platform_name"),
                DimPlacementModel.placement_name.label("placement_name"),
                DimDeviceTypeModel.device_type_name.label("device_type_name"),
                DimDateModel.date_value.label("date_value"),
                DimAgeGroupModel.age_range.label("age_range")
            )
            .join(DimRegionModel, FactAdMetricsDailyModel.region_id == DimRegionModel.region_id, isouter=True)
            .join(DimGenderModel, FactAdMetricsDailyModel.gender_id == DimGenderModel.gender_id, isouter=True)
            .join(DimPlatformModel, FactAdMetricsDailyModel.platform_id == DimPlatformModel.platform_id, isouter=True)
            .join(DimPlacementModel, FactAdMetricsDailyModel.placement_id == DimPlacementModel.placement_id, isouter=True)
            .join(DimDeviceTypeModel, FactAdMetricsDailyModel.device_type_id == DimDeviceTypeModel.device_type_id, isouter=True)
            .join(DimDateModel, FactAdMetricsDailyModel.date_id == DimDateModel.date_id, isouter=True)
             .join(DimAgeGroupModel, FactAdMetricsDailyModel.age_id == DimAgeGroupModel.age_id, isouter=True)
                 )

        result, total_count = apply_filters_ordering_pagination(
            query=query,
            filters=filter_data,
            page=page,
            size=size
        )

        # Format response
        response_data = list()
        for row in result:
            response_data.append({
                "id": row.FactAdMetricsDailyModel.id,
                "date": {"id": row.FactAdMetricsDailyModel.date_id, "name": row.date_value},
                "region": {"id": row.FactAdMetricsDailyModel.region_id, "name": row.region_name},
                "gender": {"id": row.FactAdMetricsDailyModel.gender_id, "name": row.gender_name},
                "platform": {"id": row.FactAdMetricsDailyModel.platform_id, "name": row.platform_name},
                "placement": {"id": row.FactAdMetricsDailyModel.placement_id, "name": row.placement_name},
                "device_type": {"id": row.FactAdMetricsDailyModel.device_type_id, "name": row.device_type_name},
                "age_group": {"id": row.FactAdMetricsDailyModel.age_id, "name": row.age_range},
                "impressions": row.FactAdMetricsDailyModel.impressions,
                "clicks": row.FactAdMetricsDailyModel.clicks,
                "cost": row.FactAdMetricsDailyModel.cost,
                "conversions": row.FactAdMetricsDailyModel.conversions,
                "likes": row.FactAdMetricsDailyModel.likes,
            })

        # # Return formatted response
        return create_response({"metrics": response_data,
                                "total_count": total_count})
    except Exception as e:
        print(f"Exception occurred in get_ad_metrics_data: {str(e)}")
        raise e