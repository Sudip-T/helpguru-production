from math import radians, sin, cos, sqrt, atan2


def haversine(lat1, lon1, lat2, lon2):
    # Convert latitude and longitude from degrees to radians
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    radius_of_earth = 6371  # Radius of Earth in kilometers
    distance = radius_of_earth * c

    return distance


# Coordinates
lat1, lon1 = 27.693028, 85.271435
lat2, lon2 = 27.687898, 85.279288

# Calculate distance
distance = haversine(lat1, lon1, lat2, lon2)
print("Distance:", distance, "kilometers")
