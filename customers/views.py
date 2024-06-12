from core.utils import *
from .serializers import *
from rest_framework import status
from rest_framework import filters
from vendors.models import Category
from rest_framework import viewsets
from rest_framework import generics
from core.pagination import CustomPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from vendors.serializers import CategorySerializer
from rest_framework.exceptions import MethodNotAllowed
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.parsers import MultiPartParser, FormParser
from core.permissions import IsVerified, IsObjectOwner
from rest_framework.permissions import IsAuthenticated, IsAdminUser, SAFE_METHODS

from authentication.serializers import UserSerializer
from general.models import Events
from general.serializers import EventsSerializer

from rest_framework.parsers import JSONParser


class CustomerAddressView(ModelViewSet):
    serializer_class = AddressSerializer
    queryset = Address.objects.all()
    pagination_class = CustomPagination
    filter_backends = [ DjangoFilterBackend, filters.SearchFilter ]
    search_fields = ['address_line','district','province']
    filterset_fields = ['profile','id']

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated]
        elif self.action == 'get':
            permission_classes = [IsAuthenticated, IsAdminUser]
        elif self.action in ['retrieve', 'update']:
            permission_classes = [IsAuthenticated, IsObjectOwner]
        else:
            raise MethodNotAllowed(self.action)

        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=add_user_info(request, key='profile'))
        serializer.is_valid(raise_exception=True)
        serializer.save()
        customer = serializer.validated_data['profile']
        customer.user_status = 'Verified'
        customer.save()
        return Response( serializer.data, status=status.HTTP_201_CREATED )

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=add_user_info(request, key='profile'))
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response( serializer.data, status=status.HTTP_200_OK )


class CustomerProfileView(ModelViewSet):
    queryset = CustomerProfile.objects.all()
    pagination_class = CustomPagination
    parser_classes = [MultiPartParser, FormParser]
    filter_backends = [ DjangoFilterBackend, filters.SearchFilter ]
    search_fields = ['full_name','gender','is_verified']
    filterset_fields = ['id']
    parser_classes = (FormParser,MultiPartParser, JSONParser)

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return CustomerProfileSerializer
        return GetCustomerProfileSerializer

    def get_permissions(self):
        if self.action in ['retrieve','list']:
            permission_classes = [IsAuthenticated]
        elif self.action in ['update','partial_update']:
            permission_classes = [IsAuthenticated, IsObjectOwner]
        else:
            raise MethodNotAllowed(self.request.method)

        return [permission() for permission in permission_classes]
    
    def list(self, request, *args, **kwargs):
        if request.user.is_superuser or request.user.user_type == 'vendor':
            customers = CustomerProfile.objects.all()
            serializer = self.get_serializer(customers, many=True)
        else:
            customer = CustomerProfile.objects.get(user=request.user)
            serializer = self.get_serializer(customer)

        return Response(serializer.data, status=status.HTTP_200_OK)

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=add_user_info(request, key='user'))
    #     serializer.is_valid(raise_exception=True)
    #     customer = serializer.save()
    #     # customer.user_status = 'Pending'
    #     # customer.save()
    #     return Response( serializer.data, status=status.HTTP_201_CREATED )

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=add_user_info(request, key='user'))
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response( serializer.data, status=status.HTTP_200_OK )
    

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=add_user_info(request, key='user'), partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class ServiceBookingView(generics.ListCreateAPIView):
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated, IsVerified]
    filter_backends = [ DjangoFilterBackend, filters.SearchFilter ]
    filterset_fields = ['id', 'customer', 'vendor', 'service', 'appointment_status']
    # search_fields = []

    # def get_permissions(self):
    #     permission_classes = [IsAuthenticated, IsAdminUser] if self.request.method \
    #           in SAFE_METHODS else [IsAuthenticated]
    #     return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return GetAppointmentSerializer
        return AppointmentSerializer
    
    def get_queryset(self):
        user = self.request.user
        queryset = Appointment.objects.all()

        try:
            if user.is_superuser:
                return self.filter_queryset(queryset)
            elif user.user_type == 'customer':
                return self.filter_queryset(queryset.filter(customer=user.customer))
            elif user.user_type == 'vendor':
                return self.filter_queryset(queryset.filter(vendor=user.vendor))
        except:
            return Appointment.objects.none()
        
        return None

    def post(self, request, *args, **kwargs):
        if self.request.user.is_superuser:
            serializer = self.get_serializer(data=request.data)
        elif self.request.user.user_type == 'customer':
            try:
                data = request.data.copy()
                data['customer'] = self.request.user.customer.id
                serializer = self.get_serializer(data=data)
            except Exception as e:
                return Response(
                    {
                        'error':'no customer account found'}, 
                         status=status.HTTP_400_BAD_REQUEST
                    )
        else:
            return Response(
                { 'error':'Only Admin or Customer user can this action' },
                      status=status.HTTP_403_FORBIDDEN )
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class ServiceBookingObjView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Appointment.objects.all()

    def get_permissions(self):
        if self.request.method in ['GET','PATCH']:
            permission_classes = [IsAuthenticated, IsVerified, IsObjectOwner]
        elif self.request.method in ['DELETE']:
            permission_classes = [IsAuthenticated, IsAdminUser]
        else:
            raise MethodNotAllowed(self.request.method)

        return [permission() for permission in permission_classes]
    
    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return AppointmentSerializer
        elif self.request.method == 'GET':
            return GetAppointmentSerializer
        elif self.request.method == 'PATCH':
            return PartialUpdateAppointmentSerializer

    def update(self, request, *args, **kwargs):
        # partial = kwargs.pop('partial', False)
        instance = self.get_object()

        serializer = self.get_serializer(instance, data=request.data)
        # if self.request.user.is_superuser:
        #     serializer = self.get_serializer(instance, data=request.data, partial=partial)
        # elif self.request.user.is_authenticated:
        #     data = request.data.copy()
        #     data['vendor'] = self.request.user.vendor.id
        #     serializer = self.get_serializer(instance, data=data, partial=partial)

        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
    

class FeedbackView(generics.ListCreateAPIView):
    queryset = Feedback.objects.all()
    permission_classes = [IsAuthenticated, IsVerified]
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return GetFeedbackSerializer
        return FeedbackSerializer
    
    def get_queryset(self):
        user = self.request.user
        queryset = Feedback.objects.all()
        if user.is_superuser:
            return self.filter_queryset(queryset)
        elif user.user_type == 'customer':
            return self.filter_queryset(queryset.filter(appointment__customer=user.customer))
        elif user.user_type == 'vendor':
            return self.filter_queryset(queryset.filter(appointment__vendor=user.vendor))
        return None

    def post(self, request, *args, **kwargs):
        if self.request.user.is_superuser:
            serializer = self.get_serializer(data=request.data)
        elif self.request.user.user_type == 'customer':
            data = request.data.copy()
            data['customer'] = self.request.user.customer.id
            serializer = self.get_serializer(data=data)
        else:
            return Response(
                { 'error':'Only Admin or Customer user can this action' },
                      status=status.HTTP_403_FORBIDDEN )

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        vendor = serializer.validated_data['appointment'].vendor.id
        vendor = Vendor.objects.get(id=vendor)
        _ = vendor.calculate_average_rating()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class FeedbackObjectView(generics.RetrieveDestroyAPIView):
    queryset = Feedback.objects.all()
    serializer_class = GetFeedbackSerializer

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            permission_classes = [IsAuthenticated, IsVerified, IsObjectOwner]
        elif self.request.method == 'destroy':
            permission_classes = [IsAuthenticated, IsAdminUser]
        else:
            raise MethodNotAllowed(self.request.method)
        
        return [permission() for permission in permission_classes]


class DashBoardViewSet(viewsets.ViewSet):
    # permission_classes = [IsAuthenticated]

    def list(self, request):
        # user = self.request.user
        # queryset = Appointment.objects.all()

        # try:
        #     if user.user_type == 'customer':
        #         queryset = queryset.filter(customer=user.customer)[:2]
        #         # service_history = [{'id': item.id, 'vendor': item.vendor.company_name} for item in queryset]
        #         service_history = GetAppointmentSerializer(queryset, many=True).data
        #     elif user.user_type == 'vendor':
        #         queryset = queryset.filter(vendor=user.vendor)[:2]
        #         # service_history = [{'id': item.id, 'customer': item.customer.full_name} for item in queryset]
        #         service_history = GetAppointmentSerializer(queryset, many=True).data
        #     else:
        #         service_history = None
        # except:
        #     service_history = None

        categories = Category.objects.all()
        events = Events.objects.all()
        categories = CategorySerializer(categories, many=True)
        events = EventsSerializer(events, many=True)

        return Response(
            {
                'success': 'true',
                'results': {
                    'categories': categories.data,
                    'events':events.data
                    # 'service_history': service_history
                }
            }, status=status.HTTP_200_OK
        )
