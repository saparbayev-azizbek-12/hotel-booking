from django.contrib import admin
from .models import Room, Order, Facilities, Images

admin.site.register(Order)
admin.site.register(Room)
admin.site.register(Images)
admin.site.register(Facilities)