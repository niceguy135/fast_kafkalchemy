FROM python:3.12

ENV PYTHONUNBUFFERED=1

WORKDIR /app/

ENV PYTHONPATH=/app

COPY ./requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY ./alembic.ini ./prestart.sh /app/

COPY ./app /app/app

CMD ["fastapi", "run", "--workers", "4", "app/main.py"]
