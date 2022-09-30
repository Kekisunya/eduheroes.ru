import googlemaps
import pprint
import time

API_KEY = 'AIzaSyADF-w6RvO0Yn39VeeXRW1L7mOeMZncx7A'

gmaps = googlemaps.Client(key=API_KEY)

places_result = gmaps.find_place(input='Цахкадзор', input_type='textquery')
pprint.pprint(places_result['candidates'][0]['place_id'])


