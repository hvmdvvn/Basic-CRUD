# Makefile

DJANGO_DIR=pizza_project

.PHONY: run test lint migrate makemigrations superuser

run:
	cd $(DJANGO_DIR) && python manage.py runserver 0.0.0.0:8000

migrate:
	cd $(DJANGO_DIR) && python manage.py migrate

makemigrations:
	cd $(DJANGO_DIR) && python manage.py makemigrations

superuser:
	cd $(DJANGO_DIR) && python manage.py createsuperuser

test:
	cd $(DJANGO_DIR) && pytest -v --disable-warnings

lint:
	flake8 . --exclude=venv,migrations
