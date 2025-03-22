import os
from datetime import datetime
import logging
from celery_app import celery_app

# Dynamically get the current directory of this script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Log file will be stored inside `celery_app/`
LOG_FILE_PATH = os.path.join(BASE_DIR, "celery_cron_log.txt")

# Configure logging
logging.basicConfig(filename=LOG_FILE_PATH, level=logging.INFO, format="%(asctime)s - %(message)s")


@celery_app.task
def log_timestamp_task():
    """Celery task to log timestamp."""
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"Task executed at {timestamp}"

    # Write to log file
    with open(LOG_FILE_PATH, "a") as f:
        f.write(log_message + "\n")

    # Print log (visible in Celery worker logs)
    logging.info(log_message)
    print(log_message)
