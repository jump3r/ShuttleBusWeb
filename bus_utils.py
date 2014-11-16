from math import radians, cos, sin, asin, sqrt
import datetime
from queryDAO import QueryDAO


IS_BUS_CLOSE_ENOUGH = 0.3 #within 300 meters
BUS_INACTIVE_MIN = 20 #number of minutes without HB after which bus becomes inactive

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

def process_user(user):
    pass

def changeNextStopIndex(stop_index):
    if stop_index == 0:
        return 1    
    return 0

def check_next_bus_stop(bus):
    
    #bus = QueryDAO.GetBusesStatus()[0]
    print bus['bus_id']
    curr_loc = bus['lonlat']
    ns_name, ns_loc = bus['stops_list'][bus['next_stop_index']]

    if haversine(curr_loc, ns_loc) <= IS_BUS_CLOSE_ENOUGH:        
        bus['next_stop_index'] = changeNextStopIndex(bus['next_stop_index'])        
        QueryDAO.UpdateBusStatus(bus) 
        
        return True

    return False  

def check_last_hb_within_min_time(buses_geo):

    #check if no hb for last 20 min
    for bi in range(len(buses_geo)):
        last_hb = buses_geo[bi]['last_hb_time']
        now_time = datetime.datetime.utcnow()
        mins = int(str(now_time - last_hb).split(':')[1]) #get minutes only
        if mins >= BUS_INACTIVE_MIN:
            buses_geo[bi]['status'] = "inactive"
            QueryDAO.updateBusById(buses_geo[bi])

    return buses_geo


