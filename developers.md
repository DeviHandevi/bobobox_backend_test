# For Developers
## Install Django App
``` bash
# Prepare pip environment
pipenv shell
# Install Django
pipenv install django
# Start Django Project
django-admin startproject bobobox_hotel
# Change directory
cd bobobox_hotel
# Apply the migrations for project app(s)
python manage.py migrate
# Make migrations for project app(s) such as models
python manage.py makemigrations
# Run Project
python manage.py runserver
# Start app
python manage.py startapp api
# Create superuser
python manage.py createsuperuser  # (admin, admin)
```

## Install Django REST Framework
``` bash
pipenv install djangorestframework
```
