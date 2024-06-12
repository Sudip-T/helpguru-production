from .models import *
from rest_framework import serializers

import base64
from django.core.files.base import ContentFile


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


class GetCustomerProfileSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField()
    phone = serializers.SerializerMethodField()
    address = AddressSerializer(read_only=True)
    class Meta:
        model = CustomerProfile
        fields = '__all__'

    def get_email(self, obj):
        return obj.user.email
    
    def get_phone(self, obj):
        return obj.user.phone_number
    

class Base64ImageField(serializers.ImageField):
    """
    A Django REST Framework field for handling base64-encoded image data.
    """
    def to_internal_value(self, data):
        # If the data is already a file-like object, return it unchanged
        if isinstance(data, str):
            # Decode base64 data
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class CustomerProfileSerializer(serializers.ModelSerializer):
    # profile_pic = serializers.ImageField()
    email = serializers.EmailField(write_only=True)
    class Meta:
        model = CustomerProfile
        fields = ['id','full_name','birth_date', 'email', 'gender','user','prof_pic']
        # ref_name = 'CustomerProfile 1'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.context['request'].method == 'POST':
            # self.fields['profile_pic'].required = False
            self.fields['email'].required = False
        elif self.context['request'].method == 'PUT':
            # self.fields['profile_pic'].required = True
            self.fields['email'].required = True
            self.fields['full_name'].required = True
            self.fields['birth_date'].required = True
            self.fields['gender'].required = True

    # def create(self, validated_data):
    #     email = validated_data.pop('email')
    #     user = validated_data['user']
    #     existing_user = CustomUser.objects.filter(email=email).first()
    #     if existing_user:
    #         raise serializers.ValidationError({'email': 'Email already exists'})
    #     user.email = email
    #     user.save()

    #     return super().create(validated_data)


# class UpdateCustomerProfileSerializer(serializers.ModelSerializer):
#     profile_pic = serializers.ImageField(required=True)
#     email = serializers.EmailField(required=True, write_only=True)
#     class Meta:
#         model = CustomerProfile
#         # fields = ['full_name','birth_date','gender','user','profile_pic']
#         fields = '__all__'
#         ref_name = 'CustomerProfile 2'

    
#     def to_representation(self, instance):
#         response = super().to_representation(instance)
#         response['address'] = AddressSerializer(instance.customer).data
#         return response
        

class GetAppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'
        # ref_name = 'Appointment 1'


class PartialUpdateAppointmentSerializer(serializers.ModelSerializer):
    remarks = serializers.CharField(required=True)
    class Meta:
        model = Appointment
        fields = ['appointment_status', 'remarks']
       
    def __init__(self, instance=None, data=..., **kwargs):
        super().__init__(instance, data, **kwargs)

        user = self.context['request'].user
        if user.user_type == 'customer':
            self.fields['appointment_status'].choices = [('Cancelled', 'Cancelled')]
        elif user.user_type == 'vendor':
            self.fields['appointment_status'].choices = [('Confirmed', 'Confirmed'), ('Cancelled', 'Cancelled')]


class GetFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'
