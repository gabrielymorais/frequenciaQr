.PHONY: help setup run migrate makemigrations superuser docker-build docker-up docker-down docker-logs docker-superuser


help:
@echo "Targets:" \
"\n setup -> cria venv e instala deps" \
"\n run -> roda o servidor dev" \
"\n makemigrations -> cria migrações" \
"\n migrate -> aplica migrações" \
"\n superuser -> cria superusuário" \
"\n docker-build -> build da imagem" \
"\n docker-up -> sobe com docker compose" \
"\n docker-down -> derruba serviços" \
"\n docker-logs -> logs" \
"\n docker-superuser -> cria superusuário no container"


setup:
python -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt


run:
python manage.py runserver


makemigrations:
python manage.py makemigrations


migrate:
python manage.py migrate


superuser:
python manage.py createsuperuser


docker-build:
docker compose build


docker-up:
docker compose up --build


docker-down:
docker compose down


docker-logs:
docker compose logs -f


docker-superuser:
docker compose exec web python manage.py createsuperuser