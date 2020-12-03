from django.db import models
from django.db.models import Count

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
    

# RESERVATION

class Reservation(models.Model):

  customer_name = models.CharField(max_length=50)
  hotel_id = models.ForeignKey(Hotel, on_delete=models.PROTECT)
  checkin_date = models.DateField()
  checkout_date = models.DateField()

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
