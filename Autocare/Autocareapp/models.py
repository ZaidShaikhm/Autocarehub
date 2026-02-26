from django.db import models
from django.contrib.auth.models import User
from django.conf import settings






class AdminUser(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.email

# Optional: Custom user model (if you want to extend authentication)
class UserProfile(models.Model):
    user_id = models.CharField(max_length=10, unique=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.user_id


class Vehicle(models.Model): 
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True)
    vehicle_number = models.CharField(max_length=20, unique=True)
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.CharField(max_length=10, null=True, blank=True)
    


    def __str__(self):
        return f"{self.brand} {self.model} ({self.vehicle_number})"
    

class Service(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.DurationField(help_text="Format: hh:mm:ss")

    def __str__(self):
        return self.name

class Service_status(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    service_type = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    remarks = models.TextField(blank=True)

    def __str__(self):
        return f"{self.vehicle.vehicle_number} - {self.service_type} - {self.status}"


class Booking(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True)
    vehicle_number = models.ForeignKey(Vehicle, on_delete=models.CASCADE)  # <-- renamed from vehicle_number to vehicle
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"{self.service.name} on {self.booking_date}"



class Mechanic(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.name


class ServiceAssignment(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    mechanic = models.ForeignKey(Mechanic, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.booking} -> {self.mechanic}"
