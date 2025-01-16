FROM python:3.12

ENV PYTHONUNBUFFERED=1

WORKDIR /app/

ENV PYTHONPATH=/app

COPY ./alembic.ini /app/

COPY ./app /app/app

CMD ["fastapi", "run", "--workers", "4", "app/main.py"]
