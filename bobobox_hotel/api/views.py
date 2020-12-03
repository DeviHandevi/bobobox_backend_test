from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response

# Index Page
@api_view(['GET'])
def index(request):
	project_info = {
		'project_name': 'Bobobox Backend Engineer Test',
		'author': 'Devi Handevi',
  }
	return Response(project_info)
  
# Room Search
@api_view(['GET'])
def roomsearch(request):
  room = {
    "room_id":1,
    "room_number":"101",
    "price":[
      {
        "date":"2020-01-10",
        "price":100000
      },
      {
        "date":"2020-01-11",
        "price":120000
      },
    ]
  }
  available_rooms = [room]
  search_result = {
    'room_qty': 1,
    'room_type_id': 1,
    'checkin_date': '2020-01-10',
    'checkout_date': '2020-01-11',
    'total_price': 100000,
    'available_room': available_rooms,
  }
  return Response(search_result)
  