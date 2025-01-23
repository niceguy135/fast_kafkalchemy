from celery.utils.log import get_task_logger

from app.core.celery_app import app
from app.core.config import settings
from app.core.datebase import sync_session_factory
from app.util_functions import check_connection

logger = get_task_logger(settings.PROJECT_NAME)


@app.task(bind=True)
def try_check_db_connection(self):
    try:
        logger.info("Trying to connect to DB...")
        with sync_session_factory() as session:
            check_connection(session)
        logger.info("DB connection established!")
    except Exception as exc:
        logger.info("DB connection has been failed!")
        self.retry(countdown=1, max_retries=10, exc=exc)
