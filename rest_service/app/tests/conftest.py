from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import delete
from sqlalchemy.orm import Session

from app.core.datebase import sync_session_factory
from app.initial_data import init_db
from app.main import app
from app.models import ApplicationModel


@pytest.fixture(scope="function", autouse=True)
def db() -> Generator[Session, None, None]:
    with sync_session_factory() as session:
        init_db()
        yield session
        statement = delete(ApplicationModel)
        session.execute(statement)
        session.commit()


@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as c:
        yield c
