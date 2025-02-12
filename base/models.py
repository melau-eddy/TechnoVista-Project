from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone




class Room(models.Model):
    room_name = models.CharField(max_length=200, null=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    image = models.ImageField(null=True, blank=True)
    description = models.TextField(null=True)

    def __str__(self):
        return self.room_name

    @property

    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url



class Reserve(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255, null=True) 
    email = models.EmailField(null=True,blank=True)
    arrival_date = models.DateField(default=timezone.now)
    due_date = models.DateField(default=timezone.now)
    population = models.IntegerField(null=True)

    def __str__(self):
        return f"Reservation by {self.name} for {self.arrival_date}"


class Contact(models.Model):
    first_name = models.CharField(null=True, blank=True, max_length=200)