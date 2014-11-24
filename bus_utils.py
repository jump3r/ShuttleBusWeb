from math import radians, cos, sin, asin, sqrt
import datetime
from queryDAO import QueryDAO


IS_BUS_CLOSE_ENOUGH = 0.3 #within 300 meters
BUS_INACTIVE_MIN = 5 #number of minutes without HB after which bus becomes inactive
TOOLTIP_FOR_QUESTION_MARK = "Number of students that showed their intention to be on the next bus"
TOOLTIP_FOR_BUTTON = "If you want to disclose your intention to be on the next bus so that everyone can benefit by knowing an approximate bus load"

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
        '''
        if mins >= BUS_INACTIVE_MIN and buses_geo[bi]['status'] == "active": #if it is inactive dont have to change it again
            buses_geo[bi]['status'] = "inactive"
            QueryDAO.updateBusById(buses_geo[bi])
        '''
    return buses_geo


def parse_bushb_gsm(bushb):
    #mode:gsm,busid:1, -79,43,2014//11/23,20:04:50
    busid,lon,lat = None, None, None
    
    busid = int(bushb[0].strip().split(':')[1])
    lon = float(bushb[2].strip())
    lat = float(bushb[1].strip())

    return (busid,lon,lat)

def parse_bushb_gps(bushb_list):
    #mode:gps,busid:1,lon:12.3,lat:12.3
    #adjust lon lat
    busid,lon,lat = None, None, None
    for key_val in bushb_list:

        k, v = key_val.split(':')
        k, v = k.strip(), v.strip()

        if k == "busid":
            busid = int(v)
        elif k == "lon":
            lon = float(v)
            lon = lon/100 + 0.26600651
        elif k == "lat":
            lat = float(v)
            lat = lat/100 + 0.21974639
    
    return (busid,lon,lat)
   
def getBusesSubscribedTo(session):
    ''' int(k) makes sure that we only fetch buses and not other info'''
    busids = {}
    for k in session:
        try:            
            busids[int(k)] = session[k]
        except:
            continue
    return busids    
