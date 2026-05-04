FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY app/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY app/ /app/app/

EXPOSE 8000

ENV APP_ENV=container

CMD ["gunicorn", "-b", "0.0.0.0:8000", "app.main:app"]
