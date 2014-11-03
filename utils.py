from math import radians, cos, sin, asin, sqrt
import requests


def haversine(lon1, lat1, lon2, lat2):
    
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 

    # 6367 km is the radius of the Earth
    km = 6367 * c

    return km 


def HTTPpost():
	payload = {'busid': 11}
	r = requests.get('http://localhost:5000/UserCount',data=payload)
	print r.text


def BusHB():
	payload = {'busid': 11, 'lonlat': [1,1]}
	r = requests.post('http://localhost:5000/BusHB',data=payload)
	print r.text

def BusesGeo():
    r = requests.get('http://localhost:5000/BusesGeo',data={})
    print r.text    

BusesGeo()
#BusHB()
