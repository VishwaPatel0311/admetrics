# AdMetrics

AdMetrics is a FastAPI-based application that provides advertisement metrics with filtering options. It supports PostgreSQL for database management and includes an asynchronous cron job for logging timestamps every 6 hours.

## Features
- FastAPI framework for API development
- PostgreSQL with SQLAlchemy for database management
- Optional API pagination
- Asynchronous cron job using Celery and Redis
- Structured project architecture

## This application has been hosted on https://admetrics.onrender.com/ and its endpoints can be accessed by swagger https://admetrics.onrender.com/docs#/

## Prerequisites
- Python 3.10+
- PostgreSQL
- Redis (for Celery tasks)

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/VishwaPatel0311/admetrics.git
cd app
```

### 2. Create and Activate a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables
Set following environment variables in settings.py:
```env
DB_NAME=admetrics
DB_USER=admetrics_user
DB_PASSWORD=password
DB_PORT=5432
DB_HOST=localhost
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

### 5. Start the Development Server
```bash
uvicorn main:app --host 0.0.0.0 --port 14011 --reload
```

### 6. Run celery and worker for cron job
```bash
celery -A celery_app worker --loglevel=info
celery -A celery_app beat --loglevel=info
```

## Swagger can be accessed by localhost:port/docs#/

## API Endpoints
- **POST** `admetrics/add_metrics_data` - API will create tables fact_ad_metrics_daily, dim_gender, dim_age_group,
    dim_date, dim_device_type, dim_placement, dim_platform, dim_region and inserts dummy data in them. 
    Curl:
        curl -X 'POST' \
          'https://admetrics.onrender.com/admetrics/add_metrics_data' \
          -H 'accept: application/json' \
          -d ''
    Sample Response:
        {
          "status": "success",
          "data": {
            "message": "Dummy data inserted successfully!"
          }
        }

  - **GET** `admetrics/get_ad_metrics` - A GET endpoint to retrieve ad metrics based on filters (date range, region,
  platform, etc.)
        ### Parameters
        | DataType | Parameter            | Required/optional  |
        |----------|----------------------|--------------------|
        | object   | filters              |  Optional          |
        | int      | page                 |  Optional          |
        | int      | size                 |  Optional          |

      Curl:
           curl -X 'GET' \
           'https://admetrics.onrender.com//admetrics/get_ad_metrics?filters=%7B%20%20%20%22region_id%22%3A%20%5B1%2C%202%5D%2C%20%20%20%20%22age_id%22%3A%20%5B3%2C%204%5D%2C%20%20%20%20%22gender_id%22%3A%20%5B1%5D%2C%20%20%20%20%22platform_id%22%3A%20%5B2%2C%203%5D%2C%20%20%20%20%22placement_id%22%3A%20%5B5%5D%2C%20%20%20%20%22min_impression%22%3A%201000%2C%20%20%20%20%22max_impression%22%3A%2050000%2C%20%20%20%20%22min_clicks%22%3A%2050%2C%20%20%20%20%22max_clicks%22%3A%20500%2C%20%20%20%20%22min_cost%22%3A%2010.5%2C%20%20%20%20%22max_cost%22%3A%201000.75%2C%20%20%20%20%22min_conversions%22%3A%205%2C%20%20%20%20%22max_conversions%22%3A%2050%2C%20%20%20%20%22min_likes%22%3A%2020%2C%20%20%20%20%22max_likes%22%3A%20200%2C%20%20%20%20%22start_date%22%3A%20%222024-01-01%22%2C%20%20%20%20%22end_date%22%3A%20%222024-12-31%22%20%7D&page=1&size=10' \
           -H 'accept: application/json'
      Sample Response:
          {
            "status": "success",
            "data": {
              "metrics": [
                {
                  "id": 2,
                  "date": {
                    "id": 3,
                    "name": "2025-03-20T19:49:03.782823"
                  },
                  "region": {
                    "id": 1,
                    "name": "North"
                  },
                  "gender": {
                    "id": 2,
                    "name": "Female"
                  },
                  "platform": {
                    "id": 2,
                    "name": "Instagram"
                  },
                  "placement": {
                    "id": 1,
                    "name": "Feed"
                  },
                  "device_type": {
                    "id": 1,
                    "name": "Mobile"
                  },
                  "age_group": {
                    "id": 5,
                    "name": "55+"
                  },
                  "impressions": 6782,
                  "clicks": 341,
                  "cost": 32.07,
                  "conversions": 45,
                  "likes": 591
                }
              ],
              "total_count": 517
            }
          }

## Cron Job For Logging a TimeStamp
- Cron job runs every 6 hours.
- Logs are written into app/celery_app/celery_cron_job_log.txt. UTC time stamp is logged into file.
 








