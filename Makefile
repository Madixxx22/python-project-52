install:
	poetry install

lint:
	poetry run flake8 task_manager

test:
	poetry run python3 manage.py test

dev:
	poetry run python manage.py runserver

migrate:
	poetry run python manage.py makemigrations
	poetry run python manage.py migrate

db-start:
	service postgresql start

db-stop:
	service postgresql stop

PORT ?= 8000
start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) task_manager.wsgi
