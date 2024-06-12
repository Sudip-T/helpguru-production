from django.db import models
from .manager import UserManager
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser


phone_regex = RegexValidator(
    regex=r"^\d{10}", message="10 digits NTC or NCELL number only"
)


class CustomUser(AbstractUser):
    USER_TYPES = [
        ('customer', 'Customer'),
        ('vendor', 'Vendor'),
    ]
    username = None
    email = models.EmailField(max_length=200, unique=True, null=True)
    phone_number = models.CharField(unique=True, max_length=10,validators=[phone_regex])
    otp = models.CharField(max_length=4, null=True)
    last_otp_generated = models.DateTimeField(blank=True, null=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='customer')
    otp_count = models.PositiveSmallIntegerField(default = 0)
    # token = models.CharField(max_length=255, blank=True, null=True)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    def __str__(self):
        return str(self.phone_number)

    objects = UserManager()



# class PhoneOTP(models.Model):
#     phone = models.CharField(validators=[phone_regex], max_length=17, unique=True)
#     otp = models.CharField(max_length = 9, blank = True, null= True)
#     count = models.PositiveSmallIntegerField(default = 0)
#     last_otp_generated = models.DateTimeField(blank=True, null=True)