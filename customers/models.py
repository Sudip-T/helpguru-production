from django.db import models
from authentication.models import CustomUser
from vendors.models import Vendor,Service
from core.validators import validate_rating


class CustomerProfile(models.Model):
    GENDER_CHOICES = [
        ('Male','Male'),
        ('Female','Female'),
        ('Other','Prefer not to say'),
    ]
    STATUS = [
        ('New','New'),
        ('Pending','Pending'),
        ('Verified','Verified'),
    ]
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='customer')
    full_name = models.CharField(max_length=100, null=True)
    birth_date = models.DateField(null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True)
    profile_pic = models.ImageField(upload_to='customer/profile_pics/', null=True, blank=True)
    prof_pic = models.FileField(upload_to='customer/profile_pics/', null=True, blank=True)
    user_status = models.CharField(max_length=10, choices=STATUS, default='New')
    # is_verified = models.BooleanField(default=False)
    # map_coordinates = models.CharField(max_length=255, null=False)
    
    def __str__(self):
        return self.user.phone_number
    
    class Meta:
        ordering = ['-id']


class Address(models.Model):
    profile = models.OneToOneField(CustomerProfile, on_delete=models.CASCADE, related_name='address')
    address_line = models.TextField(max_length=200, help_text="Municipality, Ward No, Tole")
    district = models.CharField(max_length=100)
    province = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, default='Nepal')

    def __str__(self):
        return f'{self.address_line}, {self.district}'


class Appointment(models.Model):
    STATUS = [
        ('New','New'),
        ('Confirmed','Confirmed'),
        ('Cancelled','Cancelled'),
        ('Completed','Completed'),
    ]
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE, related_name='appointments')
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='appointments')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='appointments')
    remarks = models.TextField(null=True)
    appointment_date = models.DateField()
    day = models.CharField(max_length=9, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    appointment_status = models.CharField(choices=STATUS,max_length=255, default='New')

    def __str__(self):
        return self.service.service_name
    
    def save(self, *args, **kwargs):
        if self.appointment_date:
            self.day = self.appointment_date.strftime("%A")

        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-id']


class Feedback(models.Model):
    feedback = models.TextField(null=True)
    user_rating = models.IntegerField(validators=[validate_rating])
    date_time = models.DateTimeField(auto_now_add=True)
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name='feedback')

    def __str__(self):
        return str(self.appointment)