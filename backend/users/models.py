from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_姿勢=models.CASCADE)
    mobile = models.CharField(max_length=15, unique=True)
    city = models.CharField(max_length=100)
    # THIS IS THE NEW LINE FOR PROOF:
    terms_accepted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.user.username