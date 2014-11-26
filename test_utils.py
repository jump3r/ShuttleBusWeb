import requests

def UserBusIntetion():
	payload = {'busid': 1}
	r = requests.post('http://localhost:5000/UserCount',data=payload)
	print r.text



def BusHB(lonlat, busid=1, method = "GPS"):
	#payload = {'busid': busid, 'lon': lonlat[0], 'lat':lonlat[1]} 
	if method == "GSM":		
		payload = "mode:gsm,busid:{}, {},{},2014//11/23,20:04:50".format(busid,*lonlat)
	else:		
		payload = 'mode:gps,busid:{},lon:{},lat:{}'.format(busid,*lonlat)
	print payload
	headers = {'content-type': 'application/x-www-form-urlencoded'}
	website = "http://localhost:5000/BusHB"
	#website = "http://shuttlebus.herokuapp.com/BusHB"
	r = requests.post(website,headers=headers, data=payload)
	
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
	
def simulated_demo():
	from bus_coord_route_demo import UTM_STGEORGE
	import time
	num = 1
	while num != 0:
		for coord in UTM_STGEORGE:			
			coord = coord[:]
			coord.reverse()
			BusHB(coord , busid=1, method="GSM")
			time.sleep(0.5)
		UTM_STGEORGE.reverse()
		num -= 1

simulated_demo()
#coord = [43.548043,-79.66095] #UTM
#coord = [43.662892,-79.395656] #ST.
#coord.reverse()
#BusHB(coord , busid=1, method="GSM") #43.548043,-79.66095
#BusImageHB()


'''
import datetime
s = datetime.datetime.utcnow()
e = datetime.datetime.utcnow()
mins = str(e - s).split(':')[1]
'''
	
