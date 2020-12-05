from django.db import models
from django.db.models import Count
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime

# BASE HOTEL

class Hotel(models.Model):
  hotel_name = models.CharField(max_length=50)
  address = models.CharField(max_length=200)

  def __str__(self):
    return self.hotel_name


class RoomType(models.Model):
  name = models.CharField(max_length=50)

  def __str__(self):
    return self.name


class Room(models.Model):
  hotel_id = models.ForeignKey(Hotel, on_delete=models.PROTECT)
  room_type_id = models.ForeignKey(RoomType, on_delete=models.PROTECT)
  room_status = models.BooleanField(default=True)
  room_number = models.IntegerField()

  def __str__(self):
    return self.hotel_id.hotel_name + ' - ' + self.room_type_id.name + ' - ' + str(self.room_number)


class Price(models.Model):
  room_type_id = models.ForeignKey(RoomType, on_delete=models.PROTECT)
  price = models.IntegerField()
  date = models.DateField()

  def __str__(self):
    return self.room_type_id.name + ' ' + str(self.price)

    

# PROMOTION

class Promo(models.Model):

  CURRENCY_TYPE = 1
  PERCENT_TYPE = 2
  PROMO_TYPE_CHOICES = [(CURRENCY_TYPE, 'Currency'), (PERCENT_TYPE, 'Percentage'), ]

  name = models.CharField(max_length=50)
  value = models.IntegerField()
  promo_type = models.IntegerField(choices=PROMO_TYPE_CHOICES, default=CURRENCY_TYPE)
  quota = models.IntegerField(default=1, validators=[MinValueValidator(1)])
  promo_date_start = models.DateField()
  promo_date_end = models.DateField()
  stay_date_start = models.DateField()
  stay_date_end = models.DateField()

  def __str__(self):
    return self.name + ' - ' + str(self.value) + ' - ' + str(self.promo_type) + ' - ' + str(self.quota)
    

class PromoRule(models.Model):
  promo_id = models.ForeignKey(Promo, on_delete=models.PROTECT)
  min_nights = models.IntegerField(default=1, validators=[MinValueValidator(1)])
  min_rooms = models.IntegerField(default=1, validators=[MinValueValidator(1)])
  checkin_day = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(6)])
  booking_day = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(6)])
  booking_hour_start = models.TimeField()
  booking_hour_end = models.TimeField()

  def __str__(self):
    return self.promo_id.name + ' - ' + str(self.min_nights) + ' - ' + str(self.min_rooms)

    

# RESERVATION

class Reservation(models.Model):

  customer_name = models.CharField(max_length=50)
  hotel_id = models.ForeignKey(Hotel, on_delete=models.PROTECT)
  checkin_date = models.DateField()
  checkout_date = models.DateField()
  reserve_date = models.DateField(default='2020-12-01')
  promo_id = models.ForeignKey(Promo, on_delete=models.PROTECT, null=True, blank=True)

  def __str__(self):
    return self.customer_name + ' - ' + str(self.checkin_date)

  @property
  def booked_room_count(self):
    stay_ids = Stay.objects.filter(reservation_id=self.id).values_list('pk', flat=True)
    result = StayRoom.objects.filter(stay_id__in=stay_ids).aggregate(num_of_rooms=Count('room_id', distinct=True))
    return result.get('num_of_rooms', 0)


class Stay(models.Model):
  guest_name = models.CharField(max_length=50)
  reservation_id = models.ForeignKey(Reservation, on_delete=models.PROTECT)

  def __str__(self):
    return self.reservation_id.customer_name + ' - ' + self.guest_name


class StayRoom(models.Model):
  stay_id = models.ForeignKey(Stay, on_delete=models.PROTECT)
  room_id = models.ForeignKey(Room, on_delete=models.PROTECT)
  date = models.DateField()

  def __str__(self):
    return self.stay_id.guest_name + ' - ' + str(self.date) + ' - ' + str(self.room_id.room_number)
