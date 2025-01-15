from typing import Any

from fastapi import APIRouter

router = APIRouter(prefix="/applications", tags=["apps"])


@router.get("/", tags=["get_apps"])
def get_apps() -> Any:
    """
    Получить список заявок от всех пользователей или от конкретного пользователя
    """
    pass


@router.post("/", tags=["create_app"])
def create_app() -> Any:
    """
    Создать заявку от пользователя
    """
    pass
