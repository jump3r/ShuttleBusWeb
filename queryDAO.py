import time
import datetime
import pymongo
import requests

MONGODB_URI = 'mongodb://shuttlebus:uftshuttle@ds048537.mongolab.com:48537/mongo_db1' 


class QueryDAO:

	@staticmethod
	def BusHBLog(busid, lonlat):
		client = pymongo.MongoClient(MONGODB_URI)
		db = client.get_default_database()

		#Verify bus_id
		collection = db['busid_map']
		busmap = collection.find({'bus_map': busid})
		
		if busmap.count() == 0:
			return
		bus_id = busmap.next()['bus_id']
	
		#Update bus status
		dt = datetime.datetime.utcnow()
		collection = db['bus_status']
		collection.update({'bus_id': bus_id}, {'$set': {'last_hb_time': dt, 'prev_loc' : '', 'lonlat' : lonlat}})

		#Add new log
		buslog = [
			{'bus_id': busid, 'lonlat': lonlat, 'hb_time' : dt}
		]

		collection = db['bus_geo_log']
		collection.insert(buslog)

		client.close()


#QueryDAO.BusHBLog(11,33)