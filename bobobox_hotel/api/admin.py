from django.contrib import admin

from .models import Hotel, RoomType, Room, Price

admin.site.site_header = "Bobobox Admin"
admin.site.site_title = "Bobobox Admin Area"
admin.site.index_title = "Welcome to Bobobox admin area"


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


admin.site.register(Hotel, HotelAdmin)
admin.site.register(RoomType, RoomTypeAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Price, PriceAdmin)
