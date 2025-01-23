from celery import Celery

from app.core.config import settings

app = Celery(settings.PROJECT_NAME,
             broker=settings.CELERY_BROKER,
             backend=settings.CELERY_BACKEND,
             include=['app.core.celery_tasks'])

if __name__ == '__main__':
    app.start()
