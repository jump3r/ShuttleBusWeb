import time
import datetime
import pymongo
import requests

MONGODB_URI = 'mongodb://shuttlebus:uftshuttle@ds048537.mongolab.com:48537/mongo_db1' 

def addBusMap():
	SEED_DATA = [
	    {
	        'bus_id': 1,
	        'bus_map': 11        
	    },
	    {
	        'bus_id': 2,
	        'bus_map': 22
	    },
	    {
	        'bus_id': 3,
	        'bus_map': 33
	    }
	]

	client = pymongo.MongoClient(MONGODB_URI)
	db = client.get_default_database()

	songs = db['busid_map']
	songs.insert(SEED_DATA)

	client.close()


def addBusStops():
	SEED_DATA = [
	    {
	        'name': 'UFT',
	        'lonlat': [43.662892,-79.395656]
	    },
	    {
	      	'name': 'UTM',
		    'lonlat': [43.548043,-79.66095]
	    },
	    {
	        'name': 'UFTS',
	        'lonlat': [43.784712,-79.185998]
	    }
	]

	client = pymongo.MongoClient(MONGODB_URI)
	db = client.get_default_database()

	songs = db['bus_stops']
	songs.insert(SEED_DATA)

	client.close()	

def addStatus():
	SEED_DATA = [
    {
        'bus_id': 1,	 
        'last_hb_time': datetime.datetime.utcnow(),
        'stops_list': [['UTM',[43.548043,-79.66095]],['UFT',[43.662892,-79.395656]]],
        'next_stop_index': 0,
        'lonlat': [43.662892,-79.395656],
        'status': 'active',        
    }
    ]

	client = pymongo.MongoClient(MONGODB_URI)
	db = client.get_default_database()

	bus_status = db['bus_status']
	bus_status.insert(SEED_DATA)


	bus_reservations = db['bus_reservations']
	all_reservations = []
	for bus in SEED_DATA:
		d = {
			'bus_id': bus['bus_id'],
			'reserved_seats_by': [],
		}
		all_reservations.append(d)
	bus_reservations.insert(all_reservations)

	client.close()	

def clearAllCollections():
	client = pymongo.MongoClient(MONGODB_URI)
	db = client.get_default_database()

	db.busid_map.remove({})
	db.bus_stops.remove({})
	db.bus_status.remove({})
	db.bus_reservations.remove({})

	client.close()

'''
{
  	'bus_id': 2,
  	'last_hb_time': datetime.datetime.utcnow(),
  	'stops_list': [['UTM',[43.548043,-79.66095]],['UFT',[43.662892,-79.395656]]],
  	'next_stop_index': 1,
    'lonlat': [43.548043,-79.66095],
    'status': ''
},
{
    'bus_id': 3,
    'last_hb_time': datetime.datetime.utcnow(),
    'stops_list': [['UFT',[43.662892,-79.395656]], ['UFTS', [43.784712,-79.185998]]],
    'next_stop_index': 0,
    'lonlat': [43.784712,-79.185998],
    'status': ''
}
]
'''
if __name__ == '__main__':
	clearAllCollections()
	addBusMap()
	addBusStops()	
	addStatus()