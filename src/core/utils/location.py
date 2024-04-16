from geopy.geocoders import Nominatim


def get_location(longitude: float, latitude: float):
    nominatim = Nominatim(user_agent="user")
    return nominatim.reverse(f'{latitude} {longitude}')
