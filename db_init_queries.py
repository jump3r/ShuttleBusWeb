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
	        'last_hb': datetime.datetime.utcnow(),
	        'prev_loc': "",
	        'lonlat': [43.662892,-79.395656]
	    },
	    {
	      	'bus_id': 2,
	      	'last_hb': datetime.datetime.utcnow(),
	      	'prev_loc': "",
		    'lonlat': [43.548043,-79.66095]
	    },
	    {
	        'bus_id': 3,
	        'last_hb': datetime.datetime.utcnow(),
	        'prev_loc': "",
	        'lonlat': [43.784712,-79.185998]
	    }
	]

	client = pymongo.MongoClient(MONGODB_URI)
	db = client.get_default_database()

	songs = db['bus_status']
	songs.insert(SEED_DATA)

	client.close()	

def clearAllCollections():
	client = pymongo.MongoClient(MONGODB_URI)
	db = client.get_default_database()

	db.busid_map.remove({})
	db.bus_stops.remove({})
	db.bus_status.remove({})

	client.close()

'''
	time() -- return current time in seconds since the Epoch as a float
    clock() -- return CPU time since process start as a float
    sleep() -- delay for a number of seconds given as a float
    gmtime() -- convert seconds since Epoch to UTC tuple
    localtime() -- convert seconds since Epoch to local time tuple
    asctime() -- convert time tuple to string
    ctime() -- convert time in seconds to string
    mktime() -- convert local time tuple to seconds since Epoch
    strftime() -- convert time tuple to string according to format specification
    strptime() -- parse string to time tuple according to format specification
    tzset() -- change the local timezone
'''

def HTTPpost():
	payload = {'user': 'username'}
	r = requests.get('http://localhost:5000/usercount',data=payload)
	print r.text

if __name__ == '__main__':
	clearAllCollections()
	addBusMap()
	addBusStops()	
	addStatus()