import os
import sys
import csv
import django
from tqdm import tqdm

sys.path.append(r'C:\Users\user\Desktop\Office\HG-Production\HelpGuru-R\helpguru')
os.environ['DJANGO_SETTINGS_MODULE'] = 'helpguru.settings'
django.setup()


from django.contrib.auth import get_user_model
from vendors.models import Category, Vendor

User = get_user_model()



class BaseManager:
    def __init__(self):
        self.processed_numbers = set()
        self.processed_vendor = 0

    def process_row(self, row):
        """Process each row. To be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement this method")


class UserManager(BaseManager):
    def get_or_create_user(self, phone_number):
        """Get or create a user by phone number."""
        user, created = User.objects.get_or_create(phone_number=phone_number)
        action = "created" if created else "already exists"
        print(f"User with phone number {phone_number} {action}.")
        return user
    
    def process_row(self, row):
        """Process user creation from the CSV row data."""
        unique_number = row['Unique Mobile Number']
        
        if unique_number in self.processed_numbers:
            return None
        
        self.processed_numbers.add(unique_number)
        
        return self.get_or_create_user(unique_number)
    

class VendorManager(BaseManager):
    def get_or_create_vendor(self, row, user):
        """Get or create a vendor based on the CSV row data and user."""
        sub_category = row['Subcategory']
        try:
            sub_category_obj = Category.objects.get(category_name=sub_category)
        except Category.DoesNotExist:
            print(f"Subcategory '{sub_category}' not found. Skipping!")
            return None
        
        company_name = row['Name']
        unique_number = row['Unique Mobile Number']
        website = row['Website']
        location = row['Location']
        map_coords = row['Map Coordinates'].split(',')
        latitude = map_coords[0]
        longitude = map_coords[-1]

        company_name = row['Name']
        unique_number = row['Unique Mobile Number']
        website = row['Website']
        location = row['Location']
        map_coords = row['Map Coordinates'].split(',')
        latitude = map_coords[0]
        longitude = map_coords[-1]

        _, created = Vendor.objects.get_or_create(
            company_name=company_name,
            category=sub_category_obj,
            contact_number=unique_number,
            defaults={
                'user': user,
                'website': website,
                'location': location,
                'latitude': latitude,
                'longitude': longitude
            }
        )
        action = "created" if created else "already exists"
        print(f"Vendor with phone number {unique_number} {action}.")
        return _

    def process_row(self, row, user):
        """Process vendor creation from the CSV row data."""
        self.processed_vendor +=1
        return self.get_or_create_vendor(row, user)



class MainController:
    def __init__(self, csv_file_path):
        self.csv_file_path = csv_file_path
        self.csv_data = self.load_csv_data()
        self.user_manager = UserManager()
        self.vendor_manager = VendorManager()

    def run(self):
        """Run the main process."""
        try:
            data = self.csv_data
            total_rows = len(data)
            for row in tqdm(data, total=total_rows, desc="Processing"):
                user = self.user_manager.process_row(row)
                if user:
                    vendor = self.vendor_manager.process_row(row, user)
                    if not vendor:
                        user_instance = User.objects.get(id=user.id)
                        user_instance.delete()
        except Exception as e:
            print('error occured', e)

    def load_csv_data(self):
        with open(self.csv_file_path, 'r', newline='', encoding='utf-8') as file:
            return list(csv.DictReader(file))




if __name__ == "__main__":
    csv_file = r'C:\Users\user\Office\clean_business_data.csv'
    controller = MainController(csv_file)
    controller.run()
    print(f"Total Number of User processed : ", len(controller.user_manager.processed_numbers))
    print(f"Total Number of vendor processed : ", controller.vendor_manager.processed_vendor)