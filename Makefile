run:
	python3 manage.py runserver

mig:
	python3 manage.py makemigrations
	python3 manage.py migrate

test:
	python3 manage.py test

