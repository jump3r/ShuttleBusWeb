import time
import datetime
import pymongo
import twilio_utils

class BusGetDAO:
	#BusDAO
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
	def GetAllBusReservations():
		client = pymongo.MongoClient(MONGODB_URI)
		db = client[DEFAULT_DB]
		
		collection = db['bus_reservations']
			
		records = collection.find()	

		reservations = []
		for rec in records:
			if rec['sms_listeners'] != []:
				reservations.append({'bus_id': rec['bus_id'],'sms_listeners': rec['sms_listeners']})

		client.close()
		return reservations


	@staticmethod
	def GetSubscribedToBusesNotArrivedYet(busid_counter_dict):
		''' Get buses user is subscribed to and not have arrived yet (current trip counter matches the one in user session.
		busid_counter = {bus_id: trip counter user is subscribed to}
		'''

		client = pymongo.MongoClient(MONGODB_URI)
		db = client[DEFAULT_DB]
		
		col = db['bus_reservations']

		records = collection.find()	

		subscribed_not_arrived = []
		for rec in records:
			bus_id = rec['bus_id']
			trips_counter = rec['trips_counter']
			if bus_id in busid_counter and busid_counter_dict[bus_id] == trips_counter:
				subscribed_not_arrived.append({'bus_id': bus_id})

		return subscribed_not_arrived

class BusUpdateDAO:

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

		
	# updateBusDAO
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
		
		print res['sms_listeners']
		t = twilio_utils.Twilio()
		t.notifyUsers(res['sms_listeners'], res['bus_id'])		
		
		res['sms_listeners'] = []
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


	@staticmethod
	def UpdateBusSMSListeners(bus_res):
		client = pymongo.MongoClient(MONGODB_URI)
		db = client[DEFAULT_DB]
		
		col = db['bus_reservations']

		for res in bus_res:
			col.update({'bus_id':res['bus_id']}, {'$set': { "sms_listeners": res["sms_listeners"] }})
			
		client.close()

class BusDAO(BusGetDAO,BusUpdateDAO):

	def default(self):
		print "BusDAO"
