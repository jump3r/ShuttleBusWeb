import time
import datetime
import pymongo
import requests
import os
import base64
import twilio_utils

MONGODB_URI = 'mongodb://uftshuttlebus:uftshuttle@ds048537.mongolab.com:48537/mongo_db1' 
if 'RUN_LOCAL' in os.environ and os.environ['RUN_LOCAL'] == 'yes':
	MONGODB_URI = 'mongodb://localhost:27017'
DEFAULT_DB = 'mongo_db1'

class QueryDAO:

	#DEMO METHODS
	@staticmethod
	def updateDBrefreshRate(refresh_val):
		client = pymongo.MongoClient(MONGODB_URI)
		db = client[DEFAULT_DB]

		col = db['bus_update_params']
		bus_obj = col.find().next()

		bus_obj["db_update"] = refresh_val
		bus_obj["js_update"] = 2000
		col.update({'_id':bus_obj['_id']},bus_obj)

		client.close()
	
	@staticmethod
	def getYoutubeVideo():
		client = pymongo.MongoClient(MONGODB_URI)
		db = client[DEFAULT_DB]

		col = db['video_link']
		video = col.find().next()

		return video['youtube_embedded_link']

	@staticmethod
	def getJSBusUpdateRate_ForDemo():
		client = pymongo.MongoClient(MONGODB_URI)
		db = client[DEFAULT_DB]

		col = db['bus_update_params']
		bus_obj = col.find().next()

		client.close()

		return int(bus_obj['js_update'])

	@staticmethod
	def getDBBusUpdateRate_ForDemo():
		client = pymongo.MongoClient(MONGODB_URI)
		db = client[DEFAULT_DB]

		col = db['bus_update_params']
		bus_obj = col.find().next()

		client.close()

		return float(bus_obj['db_update'])

	#END DEMO METHODS

	#IMAGE DAO
	@staticmethod
	def testGridFS(form_keys):
		from gridfs import GridFS

		client = pymongo.MongoClient(MONGODB_URI)
		db = client[DEFAULT_DB]
		
		fs = GridFS(db)
		gridin = fs.new_file(_id=2, chunk_num=2)
		with client.start_request():
			for i in range(len(form_keys)):
				gridin.write(form_keys[i].encode('UTF-8'))
		client.close()

	@staticmethod
	def storeImagePiece(imgp):
		client = pymongo.MongoClient(MONGODB_URI)
		db = client[DEFAULT_DB]
		
		collection = db['bus_images']
		#img_chunk = base64.b64encode(imgp)
		image = [			
			{'time': datetime.datetime.utcnow(), 'image': img_chunk}
		]		
		
		collection.insert(image)

		client.close()
	#END IMAGE DAO

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
	def UpdateBusSMSListeners(bus_res):
		client = pymongo.MongoClient(MONGODB_URI)
		db = client[DEFAULT_DB]
		
		col = db['bus_reservations']

		for res in bus_res:
			col.update({'bus_id':res['bus_id']}, {'$set': { "sms_listeners": res["sms_listeners"] }})
			
		client.close()

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



