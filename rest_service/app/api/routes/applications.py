from typing import Any

from fastapi import APIRouter
from fastapi_pagination import Page, paginate

from sqlalchemy import select

from app.core.datebase import async_session_factory
from app.models import ApplicationModel
from app.dto_schemas import ApplicationDTO


router = APIRouter(prefix="/applications", tags=["apps"])


@router.get("/", tags=["get_apps"])
async def get_apps(username: str = None) -> Page[ApplicationDTO]:
    """
    Получить список заявок от всех пользователей или от конкретного пользователя
    """
    async with async_session_factory() as session:
        if username is None:
            query = select(ApplicationModel)
        else:
            query = (
                select(ApplicationModel)
                .where(ApplicationModel.user_name == username)
            )

        query_result = await session.execute(query)
        achievements = query_result.scalars().all()

    return paginate([ApplicationDTO.model_validate(row, from_attributes=True) for row in achievements])


@router.post("/", tags=["create_app"])
def create_app() -> Any:
    """
    Создать заявку от пользователя
    """
    pass
