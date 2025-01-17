import json

from fastapi import APIRouter, HTTPException
from fastapi_pagination import Page, paginate

from sqlalchemy import select

from aiokafka import AIOKafkaProducer

from app.core.datebase import async_session_factory
from app.models import ApplicationModel
from app.dto_schemas import ApplicationDTO, ApplicationAddDTO

from app.core.config import settings

router = APIRouter(prefix="/applications", tags=["apps"])


kafka_producer = AIOKafkaProducer(
    bootstrap_servers=f"{settings.KAFKA_IP}:{settings.KAFKA_PORT}",
    enable_idempotence=True
)


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
        await session.flush()

        kafka_app_value = json.dumps(new_app_model.as_dict(), default=str).encode()
        await kafka_producer.send(
            topic=settings.KAFKA_NEW_APP_TOPIC,
            value=kafka_app_value
        )

        await session.commit()

    return HTTPException(status_code=201, detail="New application has been created")
