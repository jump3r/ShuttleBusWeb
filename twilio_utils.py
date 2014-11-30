import twilio
from twilio.rest import TwilioRestClient
 
# Your Account Sid and Auth Token from twilio.com/user/account

class Twilio:

	def __init__(self):
		self.sid = "AC362db56d14ff05dcb567fedb7d5967f3"
		self.token = "e611d70513cd12ffaf92c28cc9fa1e8f"
		self.client = TwilioRestClient(self.sid, self.token)		

	def notifyUsers(self, numbers, bus_id, message = "The bus #{} has arrived on campus."):
		print numbers, bus_id, message
		message = message.format(str(bus_id))
		for number in numbers:
			if "+1" not in number:
				number = "+1" + number
			try:
				print number
				self.client.messages.create(body=message, to=number, from_="+16475593044")
			except twilio.TwilioRestException as e:
				print e
