from django.db import models

# Create your models here.

class Room(models.Model):
    name = models.CharField(max_length=64)
    capacity = models.IntegerField()
    is_projector = models.BooleanField(default=False)

class Reservation(models.Model):
    date = models.DateField()
    room_id = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="room_reservation")
    comment = models.CharField(max_length=64, null=True)

