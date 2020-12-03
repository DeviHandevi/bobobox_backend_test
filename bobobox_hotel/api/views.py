from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Hotel, RoomType, Room, Price, Reservation, Stay, StayRoom

from datetime import datetime, timedelta

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
  # Prepare query parameters
  q_checkin_date_str = request.data.get('checkin_date', 0)
  q_checkout_date_str = request.data.get('checkout_date', 0)
  q_room_qty = request.data.get('room_qty', 0)
  q_room_type_id = request.data.get('room_type_id', 0)

  # Get rooms with the specified room_type_id
  specified_room_ids = Room.objects.filter(room_type_id=q_room_type_id).values_list('pk', flat=True)

  # Get unavailable room ids from stay room where the date is between the booking date 
  # (checkout date not included, should be minus one day)
  unavailable_room_ids = StayRoom.objects.filter(date__gte=q_checkin_date_str, date__lt=q_checkout_date_str).values_list('room_id', flat=True)

  # Get available rooms
  available_rooms_objs = Room.objects.filter(pk__in=specified_room_ids).exclude(pk__in=unavailable_room_ids)
  available_rooms = []
  # For date iteration
  checkin_date = datetime.strptime(q_checkin_date_str, '%Y-%m-%d')
  checkout_date = datetime.strptime(q_checkout_date_str, '%Y-%m-%d')
  day_delta = timedelta(days=1)
  # Set min_total_price
  min_total_price = -1
  # Iterate all available rooms to get the prices and minimum total price
  for available_room in available_rooms_objs:
    # Get all prices for each date (last price updated for each date)
    room_prices = []
    cur_date = checkin_date
    room_total_price = 0
    while cur_date < checkout_date:
      cur_date_str = cur_date.strftime('%Y-%m-%d')
      cur_price_obj = Price.objects.filter(date__lte=cur_date_str, room_type_id=q_room_type_id).order_by('-date')[:1]
      cur_price = cur_price_obj[0].price if cur_price_obj and len(cur_price_obj) > 0 else 0
      room_prices.append({
        'date': cur_date_str,
        'price': cur_price,
      })
      room_total_price += cur_price
      cur_date += day_delta

    available_rooms.append({
      "room_id": available_room.id,
      "room_number": available_room.room_number,
      "price": room_prices,
    })

    # Get minimal of total_prices
    if (min_total_price == -1) or (room_total_price < min_total_price):
        min_total_price = room_total_price

  search_result = {
    'room_qty': q_room_qty,
    'room_type_id': q_room_type_id,
    'checkin_date': q_checkin_date_str,
    'checkout_date': q_checkout_date_str,
    'total_price': min_total_price,
    'available_room': available_rooms,
  }
  return Response(search_result)
  