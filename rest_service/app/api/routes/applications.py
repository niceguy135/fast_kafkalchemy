from typing import Any

from fastapi import APIRouter, HTTPException
from fastapi_pagination import Page, paginate
from fastapi_pagination.utils import await_if_async

from sqlalchemy import select

from app.core.datebase import async_session_factory
from app.models import ApplicationModel
from app.dto_schemas import ApplicationDTO, ApplicationAddDTO


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
async def create_app(new_app: ApplicationAddDTO) -> HTTPException:
    """
    Создать заявку от пользователя
    """
    async with async_session_factory() as session:
        new_app_model = ApplicationModel(
            user_name=new_app.user_name,
            description=new_app.description
        )
        session.add(new_app_model)
        await session.commit()

    return HTTPException(status_code=201, detail="New application has been created")
