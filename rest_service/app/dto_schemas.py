from datetime import datetime
from pydantic import BaseModel


class ApplicationAddDTO(BaseModel):
    """
    Схема данных для создания запроса от пользователя
    """
    user_name: str
    description: str


class ApplicationDTO(ApplicationAddDTO):
    """
    Схема данных запроса пользователя
    """
    id: int
    created_at: datetime
