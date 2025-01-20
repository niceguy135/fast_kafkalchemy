import logging

from app.core.datebase import sync_session_factory
from app.models import ApplicationModel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init_db() -> None:
    """
    Функция инициализации начальных записей для базы данных.

    Запускать только после срабатывания миграции!
    """
    try:
        with sync_session_factory() as session:
            template_username = "Иван Иванович"

            for num in range(10):
                template_app = ApplicationModel(
                    user_name=template_username,
                    description=f"Тестовая заявка №{num}"
                )

                session.add(template_app)
                session.flush()

            session.commit()
    except Exception as e:
        logger.error(f"Cant initialize init data to database! Cause: {e}")


def main() -> None:
    logger.info("Creating initial data")
    init_db()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
