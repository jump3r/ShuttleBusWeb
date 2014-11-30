import time
import datetime
import pymongo
import requests
import os

MONGODB_URI = 'mongodb://shuttlebus:ST.Gshuttle@ds048537.mongolab.com:48537/mongo_db1' 
if 'RUN_LOCAL' in os.environ and os.environ['RUN_LOCAL'] == 'yes':
	MONGODB_URI = 'mongodb://localhost:27017'

#MONGODB_URI = 'mongodb://localhost:27017'

DEFAULT_DB = 'mongo_db1'

def addBusRefreshRateDEMO():
	SEED_DATA = [
		{
			'js_update': 2000, 	#2 sec
			'db_update': 0.5 	#0.5 sec
		}
	]
	client = pymongo.MongoClient(MONGODB_URI)
	db = client[DEFAULT_DB]
	
	col = db['bus_update_params']
	col.insert(SEED_DATA)

	client.close()


def addBusStops():
	SEED_DATA = [
	    {
	        'name': 'ST.G',
	        'lonlat': [43.662892,-79.395656]
	    },
	    {
	      	'name': 'UTM',
		    'lonlat': [43.548043,-79.66095]
	    },
	    {
	        'name': 'SHER',
	        'lonlat': [43.468645,-79.699958]
	    }
	]

	client = pymongo.MongoClient(MONGODB_URI)
	db = client[DEFAULT_DB]

	col = db['bus_stops']
	col.insert(SEED_DATA)

	client.close()	

def addImageDB():
	import datetime
	client = pymongo.MongoClient(MONGODB_URI)
	db = client[DEFAULT_DB]

	col = db['bus_images']
	col.insert([{'time': datetime.datetime.utcnow(), 'image': 'None'}])

	client.close()

def addStatus():
	SEED_DATA = [
    {
        'bus_id': 1,	 
        'last_hb_time': datetime.datetime.utcnow(),
        'stops_list': [['UTM',[43.548043,-79.66095]],['ST.G',[43.662892,-79.395656]]],
        'next_stop_index': 0, #1, #0,
        'lonlat': [43.6170021,-79.506403],#middle
        'status': 'On Route',        
    },    
    {
        'bus_id': 3,	 
        'last_hb_time': datetime.datetime.utcnow(),
        'stops_list': [['UTM',[43.548043,-79.66095]],['ST.G',[43.662892,-79.395656]]],
        'next_stop_index': 0,
        'lonlat': [43.662048, -79.396069],
        'status': 'Inactive',        
    }, 
    {
	  	'bus_id': 2,
	  	'last_hb_time': datetime.datetime.utcnow(),
	  	'stops_list': [['SHER',[43.548043,-79.66095]],['ST.G',[43.662892,-79.395656]]],
	  	'next_stop_index': 1,
	    'lonlat': [43.487488, -79.687614],
	    'status': 'Inactive'
	}
    ]


	client = pymongo.MongoClient(MONGODB_URI)
	db = client[DEFAULT_DB]

	bus_status = db['bus_status']
	bus_status.insert(SEED_DATA)

	
	bus_reservations = db['bus_reservations']
	all_reservations = []
	for bus in SEED_DATA:
		d = {
			'bus_id': bus['bus_id'],
			'seats_counter': 0,
			'trips_counter': 0,
			'sms_listeners': [],
		}
		all_reservations.append(d)
	bus_reservations.insert(all_reservations)
	
	client.close()	

def clearAllCollections():
	client = pymongo.MongoClient(MONGODB_URI)
	db = client[DEFAULT_DB]

	#db.busid_map.remove({})
	db.bus_stops.remove({})
	db.bus_status.remove({})
	db.bus_reservations.remove({})
	db.bus_images.remove({})

	client.close()

'''
{
  	'bus_id': 2,
  	'last_hb_time': datetime.datetime.utcnow(),
  	'stops_list': [['UTM',[43.548043,-79.66095]],['ST.G',[43.662892,-79.395656]]],
  	'next_stop_index': 1,
    'lonlat': [43.548043,-79.66095],
    'status': ''
},
{
    'bus_id': 3,
    'last_hb_time': datetime.datetime.utcnow(),
    'stops_list': [['ST.G',[43.662892,-79.395656]], ['ST.GS', [43.784712,-79.185998]]],
    'next_stop_index': 0,
    'lonlat': [43.784712,-79.185998],
    'status': ''
}
]


    {
        'bus_id': 2,	 
        'last_hb_time': datetime.datetime.utcnow(),
        'stops_list': [['UTM',[43.548043,-79.66095]],['ST.G',[43.662892,-79.395656]]],
        'next_stop_index': 1,
        'lonlat': [43.548043,-79.66095], #43.6335225,-79.5410157
        'status': 'active',        
    },
    
'''
if __name__ == '__main__':
	clearAllCollections()
	addBusRefreshRateDEMO()
	#addBusMap()
	addBusStops()	
	addStatus()
	addImageDB()