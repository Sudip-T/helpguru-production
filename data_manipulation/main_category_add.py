import os
import sys
import django
import csv

sys.path.append(r'C:\Users\user\Desktop\Office\dummy vend')
os.environ['DJANGO_SETTINGS_MODULE'] = 'ven.settings'
django.setup()

from vendors.models import MainCategory

# # main category adding
# CSV file path
csv_file = r'C:\Users\user\Desktop\Office\dummy vend\vendors\main_categories.csv'

# Open the CSV file and read data
with open(csv_file, 'r', newline='', encoding='utf-8') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        for row in csv_reader:
            main_category_name = row[0]
            _,created = MainCategory.objects.get_or_create(main_category_name=main_category_name)
            if created:
                print(f'created : ', main_category_name)



for data in MainCategory.objects.all():
    print(f"{data.id} : {data.main_category_name}")
