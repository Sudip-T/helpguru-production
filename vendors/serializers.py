from .models import *
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    img = serializers.ImageField(required=True)
    class Meta:
        model = Category
        fields = '__all__'

    def get_img(self, obj):
        request = self.context.get('request')
        if obj.img:
            return request.build_absolute_uri(obj.img.url)
        return None


class MainCategorySerializer(serializers.ModelSerializer):
    categories = serializers.SerializerMethodField()
    class Meta:
        model = MainCategory
        fields = '__all__'

    def get_categories(self, obj):
        categories = Category.objects.filter(main_category=obj)
        serializer = CategorySerializer(categories, many=True, context=self.context)
        return serializer.data

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        return {
            'id': ret['id'],
            'main_category_name': ret['main_category_name'],
            'categories': ret['categories']
        }


class ServiceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceType
        fields = '__all__'


class GetVendorFacilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Facility
        exclude = ['vendor']


class VendorFacilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Facility
        fields = '__all__'


class GetVendorAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorAddress
        fields = '__all__'


class VendorAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorAddress
        fields = '__all__'


class GetVendorSerializer(serializers.ModelSerializer):
    facilities = serializers.SerializerMethodField()
    # address = GetVendorAddressSerializer(many=True)

    class Meta:
        model = Vendor
        exclude = ['created_at', 'user']
        # fields = '__all__'
        # depth = 1

    def get_facilities(self, obj):
        facilities = Facility.objects.filter(vendor=obj)
        return GetVendorFacilitySerializer(facilities, many=True).data
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        facilities = instance.facility.all().values('facility_name')
        data['facilities'] = facilities
        return data


class VendorSerializer(serializers.ModelSerializer):
    # service_types = serializers.IntegerField(required=True)
    class Meta:
        model = Vendor
        fields = '__all__'

    
class NearbyVendorSerializer(serializers.ModelSerializer):
    address = GetVendorAddressSerializer(many=True)
    class Meta:
        model = Vendor
        fields = ['id', 'company_name', 'latitude', 'longitude','address']


class GetVendorDocumentSerializer(serializers.ModelSerializer):
    # vendor = GetVendorSerializer(read_only=True)
    class Meta:
        model = Documents
        fields = '__all__'

    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)

    #     limited_vendor_representation = {
    #         'id': representation['vendor']['id'],
    #         'company_name': representation['vendor']['company_name'],
    #         'contact_number': representation['vendor']['contact_number'],
    #         'email': representation['vendor']['email'],
    #         'category': representation['vendor']['category']['category_name']
    #     }

    #     representation['vendor'] = limited_vendor_representation
    #     return representation


class VendorDocumentSerializer(serializers.ModelSerializer):
    document = serializers.ImageField(required=True)
    class Meta:
        model = Documents
        fields = '__all__'


class GetVendorServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'


class VendorServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'


class GetVendorGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = '__all__'


class VendorGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = '__all__'

