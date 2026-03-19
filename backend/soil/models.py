from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=15)
    city = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username


class SoilScan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    user_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="soil_images/")
    soil_type = models.CharField(max_length=50)
    ph_value = models.FloatField()
    moisture = models.CharField(max_length=20)
    crop = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)
    is_visible = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.soil_type} - {self.user_name}"