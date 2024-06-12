import requests
import os

# def generate_otp(length=4):
#     characters = string.digits
#     otp = ''.join(random.choice(characters) for _ in range(length))
#     return otp

# SparrowSMS
def push_to_sparrow(otp, phone_number):
    response_data = requests.post(
        "http://api.sparrowsms.com/v2/sms/",
        data={'token': os.environ.get('SPARROW_SMS'),
                'from': 'InfoAlert',
                'to': phone_number,
                'text': "Your OTP code is : " + str(otp)
            }
        )
    status_code = response_data.status_code
    # response = response_data.text
    response_json = response_data.json()
    return status_code, response_json['response']




def get_user_profile(request):
    if request.user.is_superuser:
        return request.data
    
    # elif 'profile' not in data:
    data = request.data.copy()
    try:
        profile = request.user.customer.id
        data['profile'] = profile
    except Exception as e:
        print(f"Error getting user profile: {str(e)}")

    return data
    


def add_user_info(request, key=''):
    if request.user.is_superuser:
        return request.data

    data = request.data.copy()

    try:
        if key == 'user':
            user_info = getattr(request.user, 'id')
        elif key == 'profile':
            user_info = getattr(request.user.customer, 'id')
        elif key == 'customer':
            user_info = getattr(request.user.customer, 'id')
        data[key] = user_info
    except Exception as e:
        print(f"Not Found: {str(e)}")

    return data

