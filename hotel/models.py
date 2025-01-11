from django.db import models
from users.models import CustomUser


ROOM_TYPE = (
    ('standart', 'Standard'),
    ('lux', 'Lux'),
    ('economy', 'Economy'),
)


class Room(models.Model):
    number = models.CharField(max_length=10, unique=True)
    room_type = models.CharField(max_length=50, choices=ROOM_TYPE)
    adults = models.IntegerField()
    children = models.IntegerField()
    beds = models.IntegerField()
    price_per_night = models.PositiveIntegerField()
    is_available = models.BooleanField(default=True)

    def room_images(self):
        return Images.objects.filter(room=self)
    
    def room_facilities(self):
        return Facilities.objects.filter(room=self)

    def __str__(self):
        return f"Room {self.number} - {self.room_type}"


class Images(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    image = models.FileField(upload_to='rooms/')

    def __str__(self):
        return f"Image for {self.room}"


class Facilities(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    wifi = models.BooleanField(default=True)
    aircondition = models.BooleanField(default=True)
    parking = models.BooleanField(default=True)
    minibar = models.BooleanField(default=True)
    coffee_maker = models.BooleanField(default=True)
    smarttv = models.BooleanField(default=True)
    bathroom = models.BooleanField(default=True)
    stars = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Facilities for {self.room}"


class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    booking_date = models.DateField(auto_now_add=True)
    checkin_date = models.DateField()
    checkout_date = models.DateField()
    number_of_adults = models.IntegerField()
    number_of_children = models.IntegerField()
    total_price = models.PositiveIntegerField()

    def __str__(self):
        return str(f"{(self.user.username).title()} Checkin: {self.checkin_date} - Checkout: {self.checkout_date}") if self.user else "Anonymous"

    def room_detail(self):
        return self.room
    