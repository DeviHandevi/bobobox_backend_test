# Bobobox Backend Engineer Test
## Requirements
- Python 3.8
- Django
- Django REST Framework

## How to Run
``` bash
# Install dependencies
pipenv install

cd bobobox_hotel

# Apply the migrations for project app(s)
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Serve on localhost:8000
python manage.py runserver
```

## URLs
### Admin
`http://127.0.0.1:8000/admin` (adjust the URL if the IP address or the port is changed)
To create, read, update, and delete (CRUD) data.
### Hotel Room Search
`http://127.0.0.1:8000/api/roomsearch/`
Expected inputs:
- checkin_date: date (YYYY-MM-DD)
- checkout_date: date (YYYY-MM-DD)
- room_qty: int
- room_type_id: int
Example output:
```json
{
    "room_qty": "1",
    "room_type_id": "2",
    "checkin_date": "2020-12-10",
    "checkout_date": "2020-12-12",
    "total_price": 250000,
    "available_room": [
        {
            "room_id": 5,
            "room_number": 111,
            "price": [
                {
                    "date": "2020-12-10",
                    "price": 100000
                },
                {
                    "date": "2020-12-11",
                    "price": 150000
                }
            ]
        },
        {
            "room_id": 8,
            "room_number": 111,
            "price": [
                {
                    "date": "2020-12-10",
                    "price": 100000
                },
                {
                    "date": "2020-12-11",
                    "price": 150000
                }
            ]
        }
    ]
}
```

### Promotion Service
`http://127.0.0.1:8000/api/applypromo/`
Expected inputs:
- params: string (JSON)
```json
{
    "promo_id": 1,
    "total_price": 170000,
    "rooms": [
        {
            "room_id": 3,
            "room_number": 201,
            "price": [
                {
                    "date": "2020-01-10",
                    "price": 30000
                },
                {
                    "date": "2020-01-11",
                    "price": 40000
                }
            ]
        },
        {
            "room_id": 4,
            "room_number": 202,
            "price": [
                {
                    "date": "2020-01-10",
                    "price": 50000
                },
                {
                    "date": "2020-01-11",
                    "price": 50000
                }
            ]
        }
    ]
}

```
Example output:
```json
{
    "promo_id": 1,
    "total_price": 170000,
    "rooms": [
        {
            "room_id": 3,
            "room_number": 201,
            "price": [
                {
                    "date": "2020-01-10",
                    "price": 30000,
                    "promo_price": 3000,
                    "final_price": 27000
                },
                {
                    "date": "2020-01-11",
                    "price": 40000,
                    "promo_price": 4000,
                    "final_price": 36000
                }
            ]
        },
        {
            "room_id": 4,
            "room_number": 202,
            "price": [
                {
                    "date": "2020-01-10",
                    "price": 50000,
                    "promo_price": 5000,
                    "final_price": 45000
                },
                {
                    "date": "2020-01-11",
                    "price": 50000,
                    "promo_price": 5000,
                    "final_price": 45000
                }
            ]
        }
    ],
    "total_promo_price": 17000,
    "total_final_price": 153000
}
```
