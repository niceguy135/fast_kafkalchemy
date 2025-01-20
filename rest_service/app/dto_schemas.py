from datetime import datetime

from pydantic import BaseModel, Field


class ApplicationAddDTO(BaseModel):
    """
    Схема данных для создания запроса от пользователя
    """
    user_name: str = Field(..., min_length=5, max_length=50)
    description: str = Field(..., max_length=150)


class ApplicationDTO(ApplicationAddDTO):
    """
    Схема данных запроса пользователя
    """
    id: int
    created_at: datetime
