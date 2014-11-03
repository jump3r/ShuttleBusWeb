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

	@staticmethod
	def GetStopsGeo():
		client = pymongo.MongoClient(MONGODB_URI)
		db = client.get_default_database()

		collection = db['bus_stops']
		print collection
				
		stops = []				
		records = collection.find()
		for rec in records:

			d = {'name' : rec['name'],
				'lonlat' : rec['lonlat'],
				}
			stops.append(d)

		client.close()

		return stops
		

	@staticmethod
	def GetBusesGeo():
		client = pymongo.MongoClient(MONGODB_URI)
		db = client.get_default_database()

		collection = db['busid_map']
		
		records = collection.find()
		key_map ={}		
		for rec in records:
			key_map[rec['bus_id']] = rec['bus_map']
		
		
		collection = db['bus_status']
				
		buses = []		
		records = collection.find()
		for rec in records:

			d = {'bus_id' : key_map[rec['bus_id']],
				'lonlat' : rec['lonlat'],
				'active' : 1}
			buses.append(d)

		client.close()

		return buses


#QueryDAO.BusHBLog(11,33)