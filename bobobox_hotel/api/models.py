from django.db import models

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
