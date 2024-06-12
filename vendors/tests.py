import os
import sys
import django
from django.db.models import Count

sys.path.append(r'C:\Users\user\Desktop\Office\HG-Production\HelpGuru-R\helpguru')
os.environ['DJANGO_SETTINGS_MODULE'] = 'helpguru.settings'
django.setup()

from vendors.models import Vendor, Category
from django.contrib.auth import get_user_model

User = get_user_model()

# def delete_duplicate_vendors():
#     vendors = Vendor.objects.all()
#     vendor_names = {}
#     duplicates = []

#     # Identify duplicates
#     for vendor in vendors:
#         name = vendor.company_name
#         if name in vendor_names:
#             vendor_names[name].append(vendor)
#         else:
#             vendor_names[name] = [vendor]

#     # Collect duplicates
#     for name, vendors_list in vendor_names.items():
#         if len(vendors_list) > 1:
#             duplicates.extend(vendors_list[1:])  # keep the first occurrence, mark the rest as duplicates

#     # Delete duplicates and associated users
#     for vendor in duplicates:
#         user = vendor.user
#         vendor.delete()
#         if user and not Vendor.objects.filter(user=user).exists():  # check if user is associated with any other vendor
#             user.delete()
#         print(f'Deleted vendor: {vendor.company_name} and associated user: {user.phone_number if user else "N/A"}')

# if __name__ == "__main__":
#     delete_duplicate_vendors()

category_vendor_counts = Category.objects.annotate(num_vendors=Count('vendors'))

# empty_sub = list()
sub_with_vendors = 0
sub_without_vendors = 0
total = 0
for category in category_vendor_counts:
    if category.num_vendors == 0:
        sub_without_vendors +=1
#     # print(f"Category: {category.category_name}, Number of Vendors: {category.num_vendors}")
    else:
        sub_with_vendors +=1
    total +=1

print(sub_with_vendors)
print(sub_without_vendors)
print(total)

# print(Category.objects.annotate(num_vendors=Count('vendors')).filter(num_vendors=0).count())