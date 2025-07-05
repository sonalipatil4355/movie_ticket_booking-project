from django.db import models
from django.contrib.auth.models import AbstractUser





# Create your models here.

class User(AbstractUser):
    phone = models.IntegerField(unique=True, null=True, blank=True)  # Phone number field
    is_theater_manager = models.BooleanField(default=False,null=True,blank=True)  # Flag to indicate if the user is a theatre
    is_approved = models.BooleanField(default=False)  # Flag to indicate if the user is approved
    otp = models.IntegerField(null=True, blank=True)  # Field to store OTP for verification
    otp_verified = models.BooleanField(default=False)  # Flag to indicate if OTP is verified
    otp_expired=models.DateTimeField(null=True,blank=True)

    def __str__(self):
        return self.username  
    
