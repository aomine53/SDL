from django.db import models
from app.models import UserProfile


# Create your models here.

# class Owner(models.Model):
#     first_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)
#     username = models.CharField(max_length=100)
#     phone_number = models.IntegerField()
#     email = models.CharField(max_length=100)
#     created_date = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return self.first_name


class Vehicle(models.Model):
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True)
    license_plate = models.CharField(max_length=100)
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    automatic = models.BooleanField(default=False)
    color = models.CharField(max_length=100)
    fuel_type = models.CharField(max_length=100)

    def __str__(self):
        return self.make


class Driver(models.Model):
    # vehicle = models.ManyToManyField(Vehicle)
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.IntegerField()
    email = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now_add=True)
    photo = models.ImageField(upload_to='driverimage/%Y/')
    license_number = models.CharField(max_length=50)
    aadhar_number = models.IntegerField()

    def __str__(self):
        return self.first_name


class Device(models.Model):
    # owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    # vehicle = models.OneToOneField(Vehicle, on_delete=models.CASCADE)
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True)
    device_id = models.CharField(max_length=100, primary_key=True)
    device_parameters = models.TextField()

    def __str__(self):
        return self.device_id
