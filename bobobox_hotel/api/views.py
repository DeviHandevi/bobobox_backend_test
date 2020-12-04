from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Hotel, RoomType, Room, Price, Reservation, Stay, StayRoom, Promo, PromoRule

from datetime import datetime, timedelta
import json, copy

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

  num_of_available_room = len(available_rooms)
  search_result = {
    'room_qty': q_room_qty,
    'room_type_id': q_room_type_id,
    'checkin_date': q_checkin_date_str,
    'checkout_date': q_checkout_date_str,
    'total_price': min_total_price,
    'available_room': available_rooms,
    'available_room_qty': num_of_available_room if num_of_available_room > int(q_room_qty) \
      else 'Sorry, we only have ' + str(num_of_available_room) + ' available rooms..',
  }
  return Response(search_result)
  
  
# Promo Application
@api_view(['GET'])
def applypromo(request):
  # Prepare query parameters
  params_json = request.data.get('params', False)
  params = json.loads(params_json) if params_json else False
  promo_result = copy.deepcopy(params)

  if not params:
    return Response({'error': 'Parameters not found'})

  # Get the promo
  promo_id = params.get('promo_id', 0)
  try:
    promo = Promo.objects.get(pk=promo_id)
  except Promo.DoesNotExist:
    return Response({'error': 'Promo not found',})

  # Get promo rules
  promo_rules = PromoRule.objects.filter(promo_id=promo_id)

  current_datetime = datetime.now()
  current_date = current_datetime.date()
  current_time = current_datetime.time()
  # Validate the request date to the promo date start and end    
  if current_date < promo.promo_date_start:
    return Response({'error': 'Promo has not started yet',})
  elif current_date > promo.promo_date_end:
    return Response({'error': 'Promo has finished',})
  
  # Validate the booking to the rules
  is_promo_valid_for_booking = False
  rooms = params.get('rooms', [])
  num_of_rooms_booked = len(rooms)
  for promo_rule in promo_rules:
    # Minimal rooms rule
    if num_of_rooms_booked < promo_rule.min_rooms:
      continue
    # Minimal nights rule
    nights_booked = len(rooms[0].get('price', []))
    if nights_booked < promo_rule.min_nights:
      continue
    # Booking day rule
    if int(current_date.strftime("%w")) != promo_rule.booking_day:
      continue
    # Booking hour range rule
    if current_time < promo_rule.booking_hour_start or current_time > promo_rule.booking_hour_end:
      continue
    # Checkin day rule
    for room in rooms:
      room_date_and_price_list = room.get('price', [])
      for room_date_and_price in room_date_and_price_list:
        room_date_and_price['date'] = datetime.strptime(room_date_and_price['date'], '%Y-%m-%d')
      room_date_and_price_list.sort(key=lambda x: x['date'])  # sorted by date ASC
      if int(room_date_and_price_list[0]['date'].strftime('%w')) != promo_rule.checkin_day:
        return Response({
          'num_of_rooms_booked': num_of_rooms_booked,
          'promo_rule.min_rooms': promo_rule.min_rooms,
          'nights_booked': nights_booked,
          'promo_rule.min_nights': promo_rule.min_nights,
          'current_date': int(current_date.strftime("%w")),
          'promo_rule.booking_day': promo_rule.booking_day,
          'current_time': current_time,
          'promo_rule.booking_hour_start': promo_rule.booking_hour_start,
          'promo_rule.booking_hour_end': promo_rule.booking_hour_end,
          'room_date_and_price_list[0]["date"].strftime("%w")': int(room_date_and_price_list[0]['date'].strftime("%w")),
          'promo_rule.checkin_day': promo_rule.checkin_day,
        })
        continue
    # If all valid to rule
    is_promo_valid_for_booking = True
    break
  
  # If no valid rules, return error
  if not is_promo_valid_for_booking:
    return Response({'error': 'No promo rule valid for this request.',})
  
  # Check if the quota is available
  

  # Count discounts
  
   

  
  
  return Response(promo_result)