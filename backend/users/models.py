from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=15, unique=True)
    city = models.CharField(max_length=100)
    terms_accepted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.user.username

# ADD THIS NEW MODEL FOR SCANS AND LOCATION
class SoilScan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.URLField() # Stores the Cloudinary link
    soil_type = models.CharField(max_length=100)
    ph_value = models.FloatField()
    moisture = models.CharField(max_length=50)
    crop = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    is_visible = models.BooleanField(default=True)
    
    # LOCATION FIELDS
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.soil_type} ({self.date.date()})"