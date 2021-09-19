from django.contrib import admin
from .models import NewUser, Room, RoomType, RoomStatus, Booking, PaymentType, Payment

admin.site.register(NewUser)
admin.site.register(Room)
admin.site.register(RoomType)
admin.site.register(RoomStatus)
admin.site.register(Booking)
admin.site.register(Payment)
admin.site.register(PaymentType)

