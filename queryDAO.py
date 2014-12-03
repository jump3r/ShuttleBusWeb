import time
import datetime
import pymongo
import requests
import os
import base64
import twilio_utils
#Does not see these????
from imageDAO import ImageDAO
from busDAO import BusDAO
from demoDAO import DemoDAO

MONGODB_URI = 'mongodb://uftshuttlebus:uftshuttle@ds048537.mongolab.com:48537/mongo_db1' 
if 'RUN_LOCAL' in os.environ and os.environ['RUN_LOCAL'] == 'yes':
	MONGODB_URI = 'mongodb://localhost:27017'
DEFAULT_DB = 'mongo_db1'

class QueryDAO(BusDAO,ImageDAO,DemoDAO):
	
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