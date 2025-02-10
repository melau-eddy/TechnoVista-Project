from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Reserve(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255, null=True)  # Ensure this field exists
    email = models.EmailField(null=True,blank=True)
    arrival_date = models.DateField(default=timezone.now)
    due_date = models.DateField(default=timezone.now)
    population = models.IntegerField(null=True)

    def __str__(self):
        return f"Reservation by {self.name} for {self.arrival_date}"
