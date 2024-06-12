import os
import sys
import django
import json

# Append the path to your Django project
sys.path.append(r'C:\Users\user\Desktop\Office\dummy vend')

# Set the settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'ven.settings'

# Setup Django
django.setup()

# Import your models
from vendors.models import MainCategory, Category, Vendor

def model_to_dict(instance):
    """Convert a Django model instance into a dictionary."""
    opts = instance._meta
    data = {}
    for field in opts.get_fields():
        if not field.is_relation or (field.one_to_one or field.many_to_one) and field.related_model:
            value = getattr(instance, field.name)
            if isinstance(value, django.db.models.Model):
                data[field.name] = value.pk
            else:
                data[field.name] = value
    return data

# Fetch data from the database
main_categories = MainCategory.objects.all()

# Structure the data
data = []

for main_category in main_categories:
    main_cat_dict = model_to_dict(main_category)
    main_cat_dict['categories'] = []

    categories = main_category.category_set.all()
    for category in categories:
        cat_dict = model_to_dict(category)
        vendors = category.vendors.all()
        cat_dict['vendor_count'] = vendors.count()  # Add vendor count to the category dictionary
        cat_dict['vendors'] = []  # Initialize vendors list

        for vendor in vendors:
            vendor_dict = model_to_dict(vendor)
            vendor_dict['created_at'] = vendor.created_at.strftime('%Y-%m-%d %H:%M:%S')  # Convert datetime to string
            cat_dict['vendors'].append(vendor_dict)

        main_cat_dict['categories'].append(cat_dict)

    data.append(main_cat_dict)

# Convert the data to JSON
json_data = json.dumps(data, indent=4, default=str)  # Use default=str to handle any non-serializable values

# Define the path to the JSON file
output_file_path = r'C:\Users\user\Desktop\Office\helpguru-production\data_manipulation\vendor_data.json'

# Write the JSON data to the file
with open(output_file_path, 'w', encoding='utf-8') as json_file:
    json_file.write(json_data)

print(f"Data has been successfully saved to {output_file_path}")


current_path = os.getcwd()
print(current_path)