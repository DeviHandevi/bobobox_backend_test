from django.contrib import admin

from .models import Hotel, RoomType, Room, Price, Reservation, Stay, StayRoom

admin.site.site_header = "Bobobox Admin"
admin.site.site_title = "Bobobox Admin Area"
admin.site.index_title = "Welcome to Bobobox admin area"

# MODEL ADMIN
# Base Hotel

class HotelAdmin(admin.ModelAdmin):
  list_display = ('hotel_name', 'address',)
  fields = ('hotel_name', 'address',)


class RoomTypeAdmin(admin.ModelAdmin):
  fields = ('name',)


class RoomAdmin(admin.ModelAdmin):
  list_display = ('hotel_id', 'room_type_id', 'room_status', 'room_number',)
  fields = ('hotel_id', 'room_type_id', 'room_status', 'room_number',)


class PriceAdmin(admin.ModelAdmin):
  list_display = ('room_type_id', 'price', 'date',)
  fields = ('room_type_id', 'price', 'date',)

# Reservation


class StayInLine(admin.TabularInline):
    model = Stay
    extra = 0


class StayRoomInLine(admin.TabularInline):
    model = StayRoom
    extra = 0


class ReservationAdmin(admin.ModelAdmin):
  list_display = ('customer_name', 'hotel_id', 'checkin_date', 'checkout_date', 'booked_room_count',)
  fields = ('customer_name', 'hotel_id', 'checkin_date', 'checkout_date',)
  inlines = [StayInLine]


class StayAdmin(admin.ModelAdmin):
  list_display = ('guest_name', 'reservation_id',)
  fields = ('guest_name', 'reservation_id',)
  inlines = [StayRoomInLine]


class StayRoomAdmin(admin.ModelAdmin):
  list_display = ('stay_id', 'room_id', 'date',)
  fields = ('stay_id', 'room_id', 'date',)


# REGISTRATION
# Base Hotel
admin.site.register(Hotel, HotelAdmin)
admin.site.register(RoomType, RoomTypeAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Price, PriceAdmin)

# Reservation
admin.site.register(Stay, StayAdmin)
admin.site.register(StayRoom, StayRoomAdmin)
admin.site.register(Reservation, ReservationAdmin)