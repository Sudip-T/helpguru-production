from .views import *
from django.urls import path
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'address', CustomerAddressView, basename='customer-address')
router.register(r'customer', CustomerProfileView, basename='customer-profile')
router.register(r'dashboard', DashBoardViewSet, basename='dashboard')

urlpatterns = [
        path('service-booking/', ServiceBookingView.as_view(), name='service_booking'),
        path('service-booking/<int:pk>/', ServiceBookingObjView.as_view(), name='service_booking'),
        # path('service-booking/', ServiceBookingHistoryView.as_view(), name='service_booking'),
        path('feedback/', FeedbackView.as_view(), name='feedbacks'),
        path('feedback/<int:pk>/', FeedbackObjectView.as_view(), name='feedback-object'),
] + router.urls