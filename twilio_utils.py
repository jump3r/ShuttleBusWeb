import twilio
from twilio.rest import TwilioRestClient
 
# Your Account Sid and Auth Token from twilio.com/user/account

class Twilio:

	def __init__(self):
		self._sid = "AC54401f287c346b42136690f09b365661"#"AC362db56d14ff05dcb567fedb7d5967f3"
		self._token = "a23ab47138f9bd26808b43e4d12bde69"#"e611d70513cd12ffaf92c28cc9fa1e8f"
		self._from = "+15878003353"#"+16475593044"
		self.client = TwilioRestClient(self._sid, self._token)		

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
