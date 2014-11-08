from math import radians, cos, sin, asin, sqrt
import requests

IS_BUS_CLOSE_ENOUGH = 0.3

def haversine(lonlat1, lonlat2):
        
    lon1,lat1 = lonlat1
    lon2,lat2 = lonlat2
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

def printByLine(json):
    for val in json:
        print val,':', json[val]

def changeNextStopIndex(stop_index):
    if stop_index == 0:
        return 1    
    return 0

def check_next_bus_stop(bus):
    from queryDAO import QueryDAO

    #bus = QueryDAO.GetBusesStatus()[0]
    print bus['bus_id']
    curr_loc = bus['lonlat']
    ns_name, ns_loc = bus['stops_list'][bus['next_stop_index']]

    if haversine(curr_loc, ns_loc) <= IS_BUS_CLOSE_ENOUGH:        
        bus['next_stop_index'] = changeNextStopIndex(bus['next_stop_index'])
        print "CHANGED STOP"
        QueryDAO.UpdateBusStatus(bus)        

#check_next_bus_stop(None)

def HTTPpost():
	payload = {'busid': 1}
	r = requests.get('http://localhost:5000/UserCount',data=payload)
	

def BusHB(lonlat):
	payload = {'busid': 1, 'lon': lonlat[0], 'lat':lonlat[1]}
    print "BusHB1"
	r = requests.post('http://localhost:5000/BusHB',data=payload)
    print "BusHB2"
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
