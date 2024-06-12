import os
import sys
import django
import csv

sys.path.append(r'C:\Users\user\Desktop\Office\dummy vend')
os.environ['DJANGO_SETTINGS_MODULE'] = 'ven.settings'
django.setup()

from vendors.models import MainCategory, Category

# CSV file path
csv_file = r'C:\Users\user\Desktop\Office\dummy vend\vendors\sub_categories.csv'

# Open the CSV file and read data
with open(csv_file, 'r', newline='', encoding='utf-8') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        for row in csv_reader:
            main_category_name = row[-1]
            sub_category_name = row[0]

            try:
                main_category = MainCategory.objects.get(main_category_name=main_category_name)
            except MainCategory.DoesNotExist:
                print(f"Main Category '{main_category_name}' not found. Skipping.")
                continue

            # Create or get Subcategory and associate with MainCategory
            sub_category, created = Category.objects.get_or_create(category_name=sub_category_name, main_category=main_category)

            if created:
                print(f"Subcategory '{sub_category_name}' created under Main Category '{main_category_name}'.")
            else:
                print(f"Subcategory '{sub_category_name}' already exists.")



print("Subcategory import completed.")