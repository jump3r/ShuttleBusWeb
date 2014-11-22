import requests

def UserBusIntetion():
	payload = {'busid': 1}
	r = requests.post('http://localhost:5000/UserCount',data=payload)
	print r.text



def BusHB(lonlat, busid=1):
	#payload = {'busid': busid, 'lon': lonlat[0], 'lat':lonlat[1]} 
	payload = 'busid:{},lon:{},lat:{}'.format(busid,*lonlat)
	headers = {'content-type': 'application/x-www-form-urlencoded'}
	#r = requests.post('http://localhost:5000/BusHB',data=payload)
	r = requests.post('http://shuttlebus.herokuapp.com/BusImageHB', headers=headers, data=payload)
	#r = requests.post('http://localhost:5000/BusHB', headers=headers, data=payload)
	print r.text

def BusRouteChangeHB():
    payload = {'busid': 1, 'route': 'UTM UFT'}
    r = requests.post('http://localhost:5000/BusRouteChangeHB',data=payload)

def BusesGeo():
    r = requests.get('http://localhost:5000/BusesGeo',data={})
       

def ArduinoSerialListener():
	import serial
	ser = serial.Serial('/dev/tty.usbserial', 9600)
	while True:
		print ser.readline()
		
def BusImageHB():
	fr = open("icon.png", "rb")
	f = fr.read()

	#l = len(f)
	#chunk = base64.b64encode(f)
	#chunk1 = f[:27231]
	#chunk2 = f[27231:]

	#chunk1 = base64.b64encode(chunk1)
	#chunk2 = base64.b64encode(chunk2)
	headers = {'content-type': 'application/x-www-form-urlencoded'}
	#website = "http://shuttlebus.herokuapp.com/BusImageHB"
	website = "http://localhost:5000/BusImageHB"
	r = requests.post(website, headers=headers, data=f)
	print r.text
	#r = requests.post(website, headers=headers, data=chunk1)
	#print r.text
	#r = requests.post(website, headers=headers, data=chunk2)
	#print r.text

#BusHB([43.662892,-79.395656], busid=1) #43.548043,-79.66095
BusImageHB()


'''
import datetime
s = datetime.datetime.utcnow()
e = datetime.datetime.utcnow()
mins = str(e - s).split(':')[1]
'''
	
