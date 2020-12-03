# For Bobobox tester
Some notes while I was doing the task:
- I assumed that the second task was more focused on the search functionality, not on the database model. For that reason, I am not too detail on the data validation and assume that they are all valid. For example:
  - Check-in date should be before check-out date
  - Room selection in the Stay model should be from the reservation hotel
  - Date in the Stay model should be between check-in and checkout-date
  - Unique room numbers
- I made an assumption that the `room_id` in the Stay is the same as the `room_id` in the StayRoom and I apply only in StayRoom instead.
- I did not add `order_id` to the Registration model because of the lack of information about the Order model and that the Order model was not needed to finish the task.
- I assumed that the given table structure cannot be changed (have to be used as is). In my humble opinion, there are some things that could be changed to make the data management better, e.g. the Stay and StayRoom are merged into one table and it would still have the same functionality. However, it is only within my assumptions context, I do not know the overall considerations that made the decision.

# For Users
## Requirements
- Python 3.8
- Django
- Django REST Framework

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
Make migrations for project app(s) such as models `python manage.py makemigrations`
Run Project `python manage.py runserver`
Start app `python manage.py startapp api`
Create superuser `python manage.py createsuperuser` (admin, admin)

## Install Django REST Framework
Install `pipenv install djangorestframework`
