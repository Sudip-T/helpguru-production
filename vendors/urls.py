from .views import *
from rest_framework import routers
from django.urls import path,include


router = routers.DefaultRouter()
router.register(r'vendors', VendorsView, basename='vendors')
router.register(r'category', CategoryView, basename='category')
router.register(r'sub-category', SubCategoryView, basename='sub-category')
router.register(r'service-type', ServiceTypeView, basename='service-type')

urlpatterns = [
    path('', include(router.urls)),
    path('vendor/create/', VendorCreateAPIView.as_view(), name='vendor-create'),
    path('vendor/update/<int:pk>/', VendorUpdateAPIView.as_view(), name='vendor-update'),
    
    path('vendor-address/', VendorAddressView.as_view(), name='vendor-address'),
    path('vendor-address/<int:pk>/', VendorAddressObjectView.as_view(), name='vendor-adddress-obj'),

    path('vendor-document/', VendorDocumentView.as_view(), name='vendor-documents'),
    path('vendor-document/<int:pk>/', VendorDocumentObjectView.as_view(), name='vendor-document-obj'),

    path('vendor-service/', VendorServiceView.as_view(), name='vendor-services'),
    path('vendor-service/<int:pk>/', VendorServiceObjectView.as_view(), name='vendor-service-obj'),

    path('vendor-gallery/', VendorGalleryView.as_view(), name='vendor-galleries'),
    path('vendor-gallery/<int:pk>/', VendorGalleryObjectView.as_view(), name='vendor-gallery-obj'),

    path('vendor-facility/', VendorFacilityView.as_view(), name='vendor-facilities'),
    path('vendor-facility/<int:pk>/', VendorFacilityObjectView.as_view(), name='vendor-facility-obj'),

    path('see-result/', ResultsView.as_view(), name='see-result'),


    # path('vendor/', VendorListCreateAPIView.as_view(), name='vendor'),
    # path('vendor/<int:pk>/', VendorObjectAPIView.as_view(), name='vendor-object'),
    # path('nearby-vendor/', NearbyServiceProvider.as_view(), name='find_service_providers'),
]

