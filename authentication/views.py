from .serializers import *
from datetime import timedelta
from rest_framework import status
from core.utils import push_to_sparrow
from rest_framework.views import APIView
from rest_framework.response import Response
from core.pagination import CustomPagination
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from customers.models import CustomerProfile

# import secrets
from django.utils import timezone


User=get_user_model()
      

class SendOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PhoneNumberSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        phone_number = serializer.validated_data['phone_number']
        user, created = CustomUser.objects.get_or_create(phone_number=phone_number)

        if user.otp_count == 3:
            time_since_last_otp = timezone.now() - user.last_otp_generated
            if time_since_last_otp < timedelta(seconds=120):
                return Response(
                    {'error': 'Please wait for 1 minute before regenerating OTP.'}, 
                    status=status.HTTP_425_TOO_EARLY )
            user.otp_count = 0

        if not created and user.last_otp_generated is not None:
            time_since_last_otp = timezone.now() - user.last_otp_generated
            if time_since_last_otp < timedelta(seconds=30):
                return Response(
                    {'error': 'Please wait for 30 seconds before regenerating OTP.'}, 
                    status=status.HTTP_425_TOO_EARLY )
            
        otp = random.randint(1000, 9999)

        status_code, response = push_to_sparrow(otp, phone_number)

        if status_code == 200:
            user.otp = otp
            user.otp_count +=1
            user.last_otp_generated = timezone.now()
            user.save()
            return Response(
                {
                    'success': True,
                    'phone_number': phone_number,
                }, status=status.HTTP_200_OK)
        else:
            return Response({'error': {response}})
            
            # try:


            # except Exception as e:
            #     return Response(
            #         {
            #             'error': f'Something went wrong, {e}'}, 
            #                 status=status.HTTP_500_INTERNAL_SERVER_ERROR
            #         )
        # else:
        #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class VerifyOtpView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        login_serializer = OTPVerifySerializer(data=request.data)
        login_serializer.is_valid(raise_exception=True)
        phone_number = login_serializer.data['phone_number']
        otp = login_serializer.data['otp']

        try:
            user = User.objects.get(phone_number=phone_number)
            # user = CustomUser.objects.get(token=token, otp=otp)
        except User.DoesNotExist:
            return Response(
                {
                    'error': 'not a valid phone number'
                },   status=status.HTTP_400_BAD_REQUEST)
        
        if user.otp and (timezone.now() - user.last_otp_generated).seconds <= 60:
            if user.otp == otp:
                user.otp = None
                user.save()

                response = {}
                if not getattr(user, 'customer', None):
                    # msg = get_msg('e-401')
                    response['new_user'] = 'true'
                    # response['msg'] = 'OTP verified successfully'
                # elif user.user_status in ['Pending','Complete']:
                    # todo : handle cases where refresh token is balcklisted but 
                    # access token still has valid lifeime
                refresh = RefreshToken.for_user(user)
                response['access_token'] = str(refresh.access_token)
                response['refresh'] = str(refresh)

                _ , _ = CustomerProfile.objects.get_or_create(user=user) 

                return Response(response, status=status.HTTP_200_OK)
            else:
                return Response(
                    {'error': 'Invalid OTP.'},
                    status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {'error': 'OTP has expired or is invalid.'},
                status=status.HTTP_400_BAD_REQUEST)


# class UserRegisterView(generics.CreateAPIView):
#     authentication_classes = [IsAuthenticated]
#     # serializer_class = CustomerProfileSerializer
#     pagination_class = None

#     def create(self, request, *args, **kwargs):
#         data = request.data.copy()
#         user = request.user.id
#         data['user'] = user

#         serializer = self.get_serializer(data=data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)

#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers
#         )


# class LogoutView(APIView):
#     permission_classes = []

#     def post(self, request):
#         try:
#             refresh_token = request.data['refresh']
#             print(refresh_token)
#             token = RefreshToken(refresh_token)
#             token.blacklist()
#             return Response(status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({'info':str(e)},status=status.HTTP_400_BAD_REQUEST)
        
class UersView(APIView):
    pagination = CustomPagination()

    def get(self, request):
        users = User.objects.all()

        # for _ in range(10):
        #     random_number = random.randint(1000,9999)
        #     new_number = f'980350{random_number}'
        #     User.objects.create(phone_number=new_number, otp=random_number)

        # Paginate the queryset using the pagination class
        paginated_queryset = self.pagination.paginate_queryset(users, request)

        # Serialize the paginated data (extract data attribute)
        serialized_data = UserSerializer(paginated_queryset, many=True).data

        # Return the paginated response
        return self.pagination.get_paginated_response(serialized_data)
    
        



