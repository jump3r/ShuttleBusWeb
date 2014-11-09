import requests

def HTTPpost():
	payload = {'busid': 1}
	r = requests.get('http://localhost:5000/UserCount',data=payload)
	

def BusHB(lonlat):
	payload = {'busid': 1, 'lon': lonlat[0], 'lat':lonlat[1]}    
	r = requests.post('http://localhost:5000/BusHB',data=payload)
    
	print r.text

def BusRouteChangeHB():
    payload = {'busid': 1, 'route': 'UTM UFT'}
    r = requests.post('http://localhost:5000/BusRouteChangeHB',data=payload)

def BusesGeo():
    r = requests.get('http://localhost:5000/BusesGeo',data={})
       

#BusesGeo()
BusHB([43.548043,-79.66095])
#BusRouteChangeHB()
#print haversine([43.548043,-79.66095], [43.662892,-79.395656])
	