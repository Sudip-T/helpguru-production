import random
from .models import CustomUser
# from customer.models import CustomerProfile
from rest_framework import serializers
from django.core.validators import RegexValidator



def alphabetical_letters_validator(value):
    if not value.isalpha():
        raise serializers.ValidationError('Only alphabetical letters allowed')


class PhoneNumberSerializer(serializers.Serializer):
    phone_number = serializers.CharField(validators=[
        RegexValidator(regex=r'^\d{10}$', message='10 digits NTC, NCELL and SMART number only')
    ])
    # first_name = serializers.CharField(required=True, max_length=200, 
    #                     validators=[alphabetical_letters_validator])
    # last_name = serializers.CharField(required=True, max_length=200, 
    #                     validators=[alphabetical_letters_validator])

    def create(self, validated_data):
        return validated_data



class OTPVerifySerializer(serializers.Serializer):
    phone_number = serializers.CharField(validators=[
        RegexValidator(regex=r'^\d{10}$', message='10 digits NTC, NCELL and SMART number only')
    ])
    otp = serializers.CharField(validators=[RegexValidator(regex=r'^\d{4}$', message='OTP must be 4 digits')])



# class CustomerProfileSerializer(serializers.ModelSerializer):
#     email = serializers.EmailField(write_only=True)

#     class Meta:
#         model = CustomerProfile
#         fields = ['full_name', 'email', 'birth_date', 'gender','user']

#     def validate_email(self, value):
#         """
#         Validate that the email is not already associated with an existing user.
#         """
#         if CustomerProfile.objects.filter(user__email=value).exists():
#             raise serializers.ValidationError("This email is already in use.")
#         return value


#     def create(self, validated_data):
#         email = validated_data.pop('email')

#         profile = CustomerProfile.objects.create(**validated_data)

#         user = validated_data['user']
#         user.user_status = 'Pending'
#         user.email = email
#         user.save()

#         return profile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','is_superuser','first_name','last_name','email','phone_number','user_type']