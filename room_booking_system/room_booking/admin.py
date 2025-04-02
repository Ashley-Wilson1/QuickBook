from django.contrib import admin
from django.utils.timezone import localtime
from room_booking.models import RoomBooking,Room

class RoomBookingAdmin(admin.ModelAdmin):
    list_display = ('room', 'get_start_time', 'get_end_time', 'purpose')

    def get_start_time(self, obj):
        return localtime(obj.start_datetime).strftime('%Y-%m-%d %H:%M')

    def get_end_time(self, obj):
        return localtime(obj.end_datetime).strftime('%Y-%m-%d %H:%M')

    get_start_time.short_description = "Start Time (Local)"
    get_end_time.short_description = "End Time (Local)"

admin.site.register(RoomBooking, RoomBookingAdmin)
admin.site.register(Room)