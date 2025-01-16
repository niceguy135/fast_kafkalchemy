import logging

from sqlalchemy import select

from app.core.datebase import sync_session_factory
from tenacity import retry, stop_after_attempt, wait_fixed

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

max_tries = 60 * 2  # 2 минуты
wait_seconds = 1


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
)
def check_connection() -> None:
    try:
        with sync_session_factory as session:
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
