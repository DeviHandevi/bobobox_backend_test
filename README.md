# For Users
## Requirements
Python 3.8

## How to Run
``` bash
# Install dependencies
pipenv install

cd bobobox_hotel

# Serve on localhost:8000
python manage.py runserver
```

# For Developers
## Install Django App
Run `pipenv shell`
Install Django `pipenv install django`
Start Django Project `django-admin startproject bobobox_hotel`
Change directory `cd bobobox_hotel`
Apply the migrations for project app(s) `python manage.py migrate`
Run Project `python manage.py runserver`
Start app `python manage.py startapp api`
Create superuser `python manage.py createsuperuser` (admin, admin)

## Install Django REST Framework
Install `pipenv install djangorestframework`
