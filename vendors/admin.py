from django.contrib import admin
from .models import *


admin.site.register(Category)
admin.site.register(Service)
admin.site.register(ServiceType)
admin.site.register(Facility)
admin.site.register(VendorAddress)
admin.site.register(Documents)
admin.site.register(Gallery)
admin.site.register(MainCategory)


class VendorAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'category', 'contact_number', 'website', 'created_at')
    search_fields = ('company_name', 'contact_number', 'location')

    fieldsets = (
    (None, {
        'fields': ('cover_photo', 'company_name', 'category', 'contact_number', 'description', 'website', 'email', 'location')
    }),
    ('Additional Info', {
        'fields': ('ratings', 'vendor_status', 'available', 'user'),
        'classes': ('collapse',)  # This section will be initially collapsed
    }),
    ('Geolocation', {
        'fields': ('latitude', 'longitude'),
        'classes': ('collapse',)  # This section will be initially collapsed
    }),
)


admin.site.register(Vendor, VendorAdmin)