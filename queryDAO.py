import time
import datetime
import pymongo
import requests
import os

MONGODB_URI = 'mongodb://shuttlebus:uftshuttle@ds048537.mongolab.com:48537/mongo_db1' 
if 'RUN_LOCAL' in os.environ and os.environ['RUN_LOCAL'] == 'yes':
	MONGODB_URI = 'mongodb://localhost:27017'
DEFAULT_DB = 'mongo_db1'

class QueryDAO:
	@staticmethod
	def getMappedId(busid, db):
		
		collection = db['busid_map']

		busmap = collection.find({'bus_map': busid})
		bus_id = busmap.next()['bus_id']		

		return bus_id

	@staticmethod
	def BusRegisterRoute(busid, lonlat):
		client = pymongo.MongoClient(MONGODB_URI)
		db = client[DEFAULT_DB]

		bus_id = QueryDAO.getMappedId(busid, db)

		client.close()
		
		return bus_id

	@staticmethod
	def GetBusByID(bus_id):
		client = pymongo.MongoClient(MONGODB_URI)
		db = client[DEFAULT_DB]
		
		collection = db['bus_status']
		bus = collection.find({'bus_id': bus_id})	
		try:			
			bus = bus.next()
		except:			
			bus = {}

		client.close()

		return bus

	@staticmethod
	def BusHBLog(bus_id, lonlat):
		client = pymongo.MongoClient(MONGODB_URI)
		db = client[DEFAULT_DB]
		
		#UPDATE BUS STATUS
		dt = datetime.datetime.utcnow()
		collection = db['bus_status']
		
		collection.update({'bus_id': bus_id}, {'$set': {'last_hb_time': dt, 'lonlat' : lonlat}})

		#ADD NEW LOG
		buslog = [
			{'bus_id': bus_id, 'lonlat': lonlat, 'hb_time' : dt}
		]
		
		collection = db['bus_geo_log']
		collection.insert(buslog)

		client.close()

	@staticmethod
	def GetStopsGeo():
		client = pymongo.MongoClient(MONGODB_URI)
		db = client[DEFAULT_DB]

		collection = db['bus_stops']
		#print collection
				
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
		db = client[DEFAULT_DB]
		
		collection = db['bus_status']
				
		buses = []		
		records = collection.find()
		for rec in records:

			d = {'bus_id' : rec['bus_id'],
				'lonlat' : rec['lonlat'],
				'status' : rec['status'],
				'stops_list' : rec['stops_list'],
				'next_stop_index' : rec['next_stop_index'],								
				'last_hb_time': rec['last_hb_time'],
				}
			buses.append(d)

		client.close()

		return buses

	@staticmethod
	def GetBusesStatus():
		client = pymongo.MongoClient(MONGODB_URI)
		db = client[DEFAULT_DB]

		collection = db['bus_status']
				
		all_buses = []		
		records = collection.find()
		for rec in records:
			
			all_buses.append(rec)

		client.close()

		return all_buses

	@staticmethod
	def UpdateBusStatus(bus):
		client = pymongo.MongoClient(MONGODB_URI)
		db = client[DEFAULT_DB]

		col = db['bus_status']
		
		col.update({'_id':bus['_id']},bus)

		client.close()

	@staticmethod
	def updateBusById(bus):
		client = pymongo.MongoClient(MONGODB_URI)
		db = client[DEFAULT_DB]

		col = db['bus_status']
		
		col.update({'bus_id':bus['bus_id']},bus)

		client.close()
	

	@staticmethod
	def addNextTripBusLoad(bus_res):
		client = pymongo.MongoClient(MONGODB_URI)
		db = client[DEFAULT_DB]


		col = db['bus_reservations']
		col.update({'_id': bus_res['_id']}, bus_res)
		'''
		col = db['bus_status']

		bus = QueryDAO.GetBusByID(bus_id)
		bus['next_trip_bus_load'] += 1
		col.update({'_id':bus['_id']}, bus)
		'''
		client.close()

	
	@staticmethod
	def GetSeatsByBusID():
		client = pymongo.MongoClient(MONGODB_URI)
		db = client[DEFAULT_DB]
		
		collection = db['bus_reservations']
				
		reservations = {}		
		records = collection.find()		
		for rec in records:
			reservations[rec['bus_id']] = rec['seats_counter']

		client.close()
		return reservations

	@staticmethod
	def getBusReservationIDsByBus(bus_id):
		client = pymongo.MongoClient(MONGODB_URI)
		db = client[DEFAULT_DB]

		col = db['bus_reservations']
		all_reservations = col.find({'bus_id': bus_id})

		return all_reservations.next()

	@staticmethod
	def resetBusSeatsCounterAndStatus(bus_id):
		client = pymongo.MongoClient(MONGODB_URI)
		db = client[DEFAULT_DB]

		col = db['bus_reservations']
		res = col.find({'bus_id': bus_id})
		res = res.next()

		res['seats_counter'] = 0

		res['trips_counter'] += 1
		if res['trips_counter'] == 300:
			res['trips_counter'] = 0
		
		res["status"] = "active"

		col.update({'_id':res['_id']}, res )

		client.close()

	@staticmethod
	def resetBusToActive(bus_id):
		client = pymongo.MongoClient(MONGODB_URI)
		db = client[DEFAULT_DB]

		col = db['bus_reservations']
		res = col.find({'bus_id': bus_id})
		res = res.next()
		res["status"] = "active"

		col.update({'_id':res['_id']}, res )

		client.close()

		

#QueryDAO.addNextTripBusLoad(1)
#QueryDAO.BusHBLog(1,33)

#QueryDAO.GetBusesStatus()
#QueryDAO.GetBusByID(1)