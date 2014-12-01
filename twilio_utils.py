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
		self._sid = twilio['sid'] #"AC54401f287c346b42136690f09b365661"#"AC362db56d14ff05dcb567fedb7d5967f3"
		self._token = twilio['token'] #"a23ab47138f9bd26808b43e4d12bde69"#"e611d70513cd12ffaf92c28cc9fa1e8f"
		self._from = twilio['from'] #"+15878003353"#"+16475593044"
		self.client = TwilioRestClient(self._sid, self._token)		
		print self._sid, self._token, self._from

	def notifyUsers(self, numbers, bus_id, message = "The bus #{} has arrived on campus."):
		print numbers, bus_id, message
		message = message.format(str(bus_id))
		for number in numbers:
			if "+1" not in number:
				number = "+1" + number
			try:
				print number
				self.client.messages.create(body=message, to=number, from_=self._from)
			except twilio.TwilioRestException as e:
				print e


