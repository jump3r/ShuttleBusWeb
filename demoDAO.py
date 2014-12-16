import time
import datetime
import pymongo
import twilio_utils
from imageDAO import ImageDAO


class DemoDAO:	
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
	
