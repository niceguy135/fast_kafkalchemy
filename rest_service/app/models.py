import datetime
from typing import Annotated

from sqlalchemy import String, text
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase

str_100 = Annotated[str, String(100)]
intpk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime.datetime, mapped_column(server_default=text("now()"))]


class BaseModel(DeclarativeBase):
    """
    Абстрактный класс модели
    """

    repr_cols_num = 3
    repr_cols = tuple()

    def __repr__(self):
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f"{col}={getattr(self, col)}")

        return f"<{self.__class__.__name__} {', '.join(cols)}>"


class ApplicationModel(BaseModel):
    """
    Модель заявки (таблица applications)
    """
    __tablename__ = "applications"

    id: Mapped[intpk]
    user_name: Mapped[str_100]
    description: Mapped[str]
    created_at: Mapped[created_at]

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
