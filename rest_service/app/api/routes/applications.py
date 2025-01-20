import json

from fastapi import APIRouter
from fastapi_pagination import Page, paginate

from sqlalchemy import select

from aiokafka import AIOKafkaProducer

from app.core.datebase import async_session_factory
from app.models import ApplicationModel
from app.dto_schemas import ApplicationDTO, ApplicationAddDTO

from app.core.config import settings

router = APIRouter(prefix="/applications")


def aiokafka_value_serializer(value) -> bytes:
    return json.dumps(value, default=str).encode()


@router.get("/", tags=["get_apps"])
async def get_apps(username: str) -> Page[ApplicationDTO]:
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


@router.post("/", tags=["create_app"], status_code=201)
async def create_app(new_app: ApplicationAddDTO):
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
        created_app_data = new_app_model.as_dict()
        await session.commit()

    kafka_producer = AIOKafkaProducer(
        bootstrap_servers=f"{settings.KAFKA_IP}:{settings.KAFKA_PORT}",
        enable_idempotence=True,
        value_serializer=aiokafka_value_serializer
    )

    await kafka_producer.start()
    await kafka_producer.send(
        topic=settings.KAFKA_NEW_APP_TOPIC,
        value=created_app_data
    )
    await kafka_producer.stop()

    return {"message": "New application has been created"}
