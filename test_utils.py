import requests

def UserBusIntetion():
	payload = {'busid': 1}
	r = requests.post('http://localhost:5000/UserCount',data=payload)
	print r.text



def BusHB(lonlat, busid=1):
	payload = {'busid': busid, 'lon': lonlat[0], 'lat':lonlat[1]}    
	r = requests.post('http://localhost:5000/BusHB',data=payload)
    
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
		

#UserBusIntetion()
#BusesGeo()
#BusHB([43.662892,-79.395656], busid= 1) #43.548043,-79.66095
#BusRouteChangeHB()
#print haversine([43.548043,-79.66095], [43.662892,-79.395656])
'''
import datetime
s = datetime.datetime.utcnow()
e = datetime.datetime.utcnow()
mins = str(e - s).split(':')[1]
'''
	