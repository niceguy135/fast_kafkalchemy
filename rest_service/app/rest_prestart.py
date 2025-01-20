import logging

from sqlalchemy import select
from tenacity import retry, stop_after_attempt, wait_fixed

from app.core.datebase import sync_session_factory

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

max_tries = 60 * 2  # 2 минуты
wait_seconds = 1


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
)
def check_connection() -> None:
    """
    Банальная проверка на возможность отправки запрос в базу данных (просто пытаемся вызвать ``SELECT 1`` у БД)

    Проверка проводиться либо пока не будет достигнут успех, либо пока количество проверок не достигнет ``max_tries``
    :return: None
    """
    try:
        with sync_session_factory() as session:
            session.exec(select(1))
    except Exception as e:
        logger.error(e)
        raise e


def main() -> None:
    logger.info("Checking DB connection...")
    check_connection()
    logger.info("Connection is good!")


if __name__ == "__main__":
    main()
