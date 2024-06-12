from django.db import models
from core.validators import *
from authentication.models import CustomUser
from django.core.validators import MinLengthValidator
# from django.contrib.gis.db.models import PointField
# from django.contrib.gis.geos import Point
from core.choices import DISTRICT_CHOICES, PROVINCE_CHOICES
from django.conf import settings


class MainCategory(models.Model):
    main_category_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.main_category_name

    class Meta:
        ordering = ['id']


class Category(models.Model):
    category_name = models.CharField(max_length=255, unique=True)
    img = models.ImageField(upload_to='vendors/category/', null=True)
    main_category = models.ForeignKey(MainCategory, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.category_name

    def img_url(self):
        if self.img:
            return settings.MEDIA_URL + self.img.name
        return None

    class Meta:
        ordering = ['category_name']


class ServiceType(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class Facility(models.Model):
    facility_name = models.CharField(max_length=255)
    vendor = models.ForeignKey('Vendor', on_delete=models.CASCADE, related_name='facility')

    def __str__(self):
        return self.facility_name


class Vendor(models.Model):
    STATUS = [
        ('New','New'),
        ('Pending','Pending'),
        ('Verified','Verified'),
    ]
    cover_photo = models.ImageField(blank=True, null=True)
    company_name = models.CharField(max_length=255, validators=[MinLengthValidator(3)], unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='vendors')
    contact_number = models.BigIntegerField(validators=[validate_phone_number], unique=True)
    description = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    ratings = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    vendor_status = models.CharField(max_length=10, choices=STATUS, default='New')
    available = models.BooleanField(default=False, choices=[(True, 'Available'), (False, 'Not Available')])
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='vendor')
    website = models.URLField(null=True, blank=True)
    location = models.CharField(max_length=200)
    email = models.EmailField(unique=True, max_length=100, null=True, blank=True)

    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    # location = PointField(blank=True, null=True)
    # service_types = models.ManyToManyField(ServiceType)
    # subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, related_name='vendors', null=True)
    # emergency_contact = models.BigIntegerField(validators=[validate_phone_number], null=True)
    # service_days = models.TextField(null=True)
    # service_start_time = models.TimeField(null=True)
    # service_end_time = models.TimeField(null=True)

    def __str__(self):
        return self.company_name
    
    def calculate_average_rating(self):
        total_rating = 0
        appointments_with_feedback = 0

        for appointment in self.appointments.all():
            try:
                feedback = appointment.feedback
                total_rating += feedback.user_rating
                appointments_with_feedback += 1
            # except Feedback.DoesNotExist:
            except:
                pass

        if appointments_with_feedback > 0:
            average_rating = total_rating / appointments_with_feedback
        else:
            average_rating = 0
        
        self.ratings = average_rating
        self.save()

    # def save(self, *args, **kwargs):
    #     if self.latitude and self.longitude:
    #         self.location = Point(self.longitude, self.latitude)
    #     super().save(*args, **kwargs)


class VendorAddress(models.Model):
    district = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default='Nepal')
    province = models.CharField(max_length=100, blank=True, null=True)
    address_line = models.TextField(max_length=200, help_text="Municipality, Ward No, Tole")
    nearest_landmark = models.TextField(blank=True, null=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='address')
    # province = models.CharField(max_length=100, blank=True, null=True, choices=PROVINCE_CHOICES)
    # district = models.CharField(max_length=100, choices=DISTRICT_CHOICES)

    def __str__(self):
        return f'{self.address_line}, {self.district}'
    

class Documents(models.Model):
    # TYPES = [
    #     ('RC','Registration Certificate'),
    #     ('LP','License or Permit'),
    # ]
    document_type = models.CharField(max_length=255)
    document = models.ImageField(upload_to='vendor/document/')
    is_verified = models.BooleanField(default=False)
    pan_number = models.BigIntegerField(validators=[validate_pan_number], unique=True, null=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='documents')

    def __str__(self):
        return self.vendor.company_name


class Service(models.Model):
    service_name = models.CharField(max_length=255)
    description = models.TextField(null=True)
    price = models.IntegerField()
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='services')

    def __str__(self):
        return self.vendor.company_name


class Gallery(models.Model):
    image = models.ImageField(upload_to='vendor/gallery/')
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='galleries')

    def __str__(self):
        return self.vendor.company_name



# class Subscription(models.Model):
#     package_name = models.CharField(max_length=255, unique=True, null=False)
#     package_price = models.IntegerField(null=False)
#     discount_price = models.IntegerField(null=True)
#     description = models.TextField(null=True)
#     features = models.TextField(null=False)
#     validity = models.IntegerField(null=False)
    

# class Payment(models.Model):
#     appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='payments', null=False)
#     amount = models.FloatField(null=False)
#     payment_method = models.CharField(max_length=255, null=False)
#     payment_status = models.CharField(max_length=255, null=False)
#     date_time = models.DateTimeField()
#     receipt_number = models.CharField(max_length=255, null=False)