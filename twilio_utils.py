import twilio
from twilio.rest import TwilioRestClient

import pymongo
import requests
import os


def getTwilioParams():
	MONGODB_URI = 'mongodb://uftshuttlebus:uftshuttle@ds048537.mongolab.com:48537/mongo_db1' 
	if 'RUN_LOCAL' in os.environ and os.environ['RUN_LOCAL'] == 'yes':
		MONGODB_URI = 'mongodb://localhost:27017'
	DEFAULT_DB = 'mongo_db1'

	client = pymongo.MongoClient(MONGODB_URI)
	db = client[DEFAULT_DB]

	col = db['twilio_params']
	twilio_params = col.find().next()

	client.close()

	return twilio_params


class Twilio:

	def __init__(self):		
		twilio = getTwilioParams()
		self._sid = twilio['sid'] 
		self._token = twilio['token'] 
		self._from = twilio['from']
		self.client = TwilioRestClient(self._sid, self._token)		
		
	def notifyUsers(self, numbers, bus_id, message = "The bus #{} has arrived on campus."):
		
		message = message.format(str(bus_id))
		
		for number in numbers:
			if "+1" not in number:
				number = "+1" + number
			try:		
				self.client.messages.create(body=message, to=number, from_=self._from)
			except twilio.TwilioRestException as e:
				print e


