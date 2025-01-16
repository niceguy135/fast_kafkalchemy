import logging

from sqlalchemy import select

from app.core.datebase import sync_session_factory
from app.models import ApplicationModel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init_db() -> None:
    """
    Функция инициализации начальных данных для базы данных.

    Запускать только после срабатывания миграции!
    """
    with sync_session_factory() as session:
        template_username = "Иван Иванович"
        template_app = ApplicationModel(
            user_name=template_username,
            description="Я хочу кушать("
        )

        user = session.execute(
            select(ApplicationModel).where(ApplicationModel.user_name == template_username)
        ).first()
        if not user:
            session.add(template_app)
            session.commit()


def main() -> None:
    logger.info("Creating initial data")
    init_db()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
