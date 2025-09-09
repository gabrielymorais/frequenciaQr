# Dockerfile
FROM python:3.12-slim


ENV PYTHONDONTWRITEBYTECODE=1 \
PYTHONUNBUFFERED=1 \
PIP_NO_CACHE_DIR=1


WORKDIR /app


# deps do sistema (Pillow e build basico)
RUN apt-get update && apt-get install -y --no-install-recommends \
build-essential libjpeg62-turbo-dev zlib1g-dev \
&& rm -rf /var/lib/apt/lists/*


COPY requirements.txt .
RUN pip install -r requirements.txt


COPY . .


# coleta estáticos (caso use)
RUN mkdir -p /app/staticfiles


EXPOSE 8000


CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]