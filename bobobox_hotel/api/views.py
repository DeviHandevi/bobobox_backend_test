from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Count
from .models import Hotel, RoomType, Room, Price, Reservation, Stay, StayRoom, Promo, PromoRule

from datetime import datetime, timedelta
import json, math

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
  q_room_qty = int(request.data.get('room_qty', 0))
  q_room_type_id = request.data.get('room_type_id', 0)

  # Get rooms with the specified room_type_id
  specified_room_ids = Room.objects.filter(room_type_id=q_room_type_id).values_list('pk', flat=True)

  # Get unavailable room ids from stay room where the date is between the booking date 
  # (checkout date not included, should be minus one day)
  unavailable_room_ids = StayRoom.objects.filter(date__gte=q_checkin_date_str, date__lt=q_checkout_date_str).values_list('room_id', flat=True)

  # Get available rooms
  available_rooms_objs = Room.objects.filter(pk__in=specified_room_ids, room_status=True).exclude(pk__in=unavailable_room_ids)
  available_rooms = []
  # For date iteration
  checkin_date = datetime.strptime(q_checkin_date_str, '%Y-%m-%d')
  checkout_date = datetime.strptime(q_checkout_date_str, '%Y-%m-%d')
  day_delta = timedelta(days=1)
  # Iterate all available rooms to get the prices and minimum total price
  room_total_prices = []
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

    room_total_prices.append(room_total_price)

  # Get minimal of total_prices with the number of room qty requested
  room_total_prices.sort()
  min_total_price = sum(room_total_prices[:q_room_qty])

  num_of_available_room = len(available_rooms)
  search_result = {
    'room_qty': q_room_qty,
    'room_type_id': q_room_type_id,
    'checkin_date': q_checkin_date_str,
    'checkout_date': q_checkout_date_str,
    'total_price': min_total_price,
    'available_room': available_rooms,
    'available_room_qty': num_of_available_room if num_of_available_room >= int(q_room_qty) \
      else 'Sorry, we only have ' + str(num_of_available_room) + ' available rooms..',
  }
  return Response(search_result)
  
  
# Promo Application
@api_view(['GET'])
def applypromo(request):
  # Prepare query parameters
  params_json = request.data.get('params', False)
  params = json.loads(params_json) if params_json else False

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
        continue
    # If all valid to rule
    is_promo_valid_for_booking = True
    break
  
  # If no valid rules, return error
  if not is_promo_valid_for_booking:
    return Response({'error': 'No promo rule valid for this request.',})
  
  # Check if the quota is available
  # Get number of reservation for this promo all time
  reservation_promo = Reservation.objects.filter(promo_id=promo_id, reserve_date__lt=current_date).aggregate(num=Count('id', distinct=True))
  number_of_reservation_promo = reservation_promo.get('num', 0)

  # Get number of reservation today
  reservation_promo_today = Reservation.objects.filter(promo_id=promo_id, reserve_date=current_date)\
    .aggregate(num=Count('id', distinct=True))
  number_of_reservation_today = reservation_promo_today.get('num', 0)

  # Get allowed quota for today
  promo_day_left = (promo.promo_date_end - current_date).days + 1
  promo_quota_left = promo.quota - number_of_reservation_promo
  allowed_quota_per_day = math.floor(promo_quota_left / promo_day_left)
  allowed_quota_today = allowed_quota_per_day - number_of_reservation_today
  if allowed_quota_today < 1:
    return Response({'error': 'No promo quota left.',})

  # For debugging
  # return Response({
  #   'num_of_rooms_booked': num_of_rooms_booked,
  #   'promo_rule.min_rooms': promo_rule.min_rooms,
  #   'nights_booked': nights_booked,
  #   'promo_rule.min_nights': promo_rule.min_nights,
  #   'current_date': int(current_date.strftime("%w")),
  #   'promo_rule.booking_day': promo_rule.booking_day,
  #   'current_time': current_time,
  #   'promo_rule.booking_hour_start': promo_rule.booking_hour_start,
  #   'promo_rule.booking_hour_end': promo_rule.booking_hour_end,
  #   'room_date_and_price_list[0]["date"].strftime("%w")': int(room_date_and_price_list[0]['date'].strftime("%w")),
  #   'promo_rule.checkin_day': promo_rule.checkin_day,
  #   'promo.quota': promo.quota,
  #   'promo.promo_date_end': promo.promo_date_end,
  #   'promo.promo_date_start': promo.promo_date_start,
  #   'promo_day_left': promo_day_left,
  #   'promo_quota_left': promo_quota_left,
  #   'number_of_reservation_today': number_of_reservation_today,
  #   'allowed_quota_per_day': allowed_quota_per_day,
  #   'allowed_quota_today': allowed_quota_today,
  # })

  # Count discounts
  total_promo_price = 0
  total_final_price = params['total_price']
  for room in rooms:
    room_date_and_price_list = room.get('price', [])
    for room_date_and_price in room_date_and_price_list:
      if promo.promo_type == 1:  # currency
        promo_price = promo.value * (room_date_and_price['price'] / params['total_price'])
      else:  # percentage
        promo_price = (room_date_and_price['price'] * promo.value) / 100
      # Making sure that no promo price larger than the price itself
      if promo_price > room_date_and_price['price']:
        promo_price = room_date_and_price['price']
      # Adding the promo and final price data
      room_date_and_price['promo_price'] = int(promo_price)
      room_date_and_price['final_price'] = int(room_date_and_price['price'] - promo_price)
      total_promo_price += promo_price
      # Reformat the date 
      room_date_and_price['date'] = room_date_and_price['date'].strftime('%Y-%m-%d')
  total_final_price -= total_promo_price

  # Add total promo and final price
  params['total_promo_price'] = int(total_promo_price)
  params['total_final_price'] = int(total_final_price)
  
  return Response(params)