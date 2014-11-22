from flask import Flask
from flask import g
from flask import Markup 
from flask import session, redirect, url_for, escape, request, render_template

import sys
import pymongo
from bson.json_util import dumps
from queryDAO import QueryDAO
from bus_utils import check_next_bus_stop
from bus_utils import check_last_hb_within_min_time
from bus_utils import TOOLTIP_FOR_QUESTION_MARK, TOOLTIP_FOR_BUTTON
import map_styles 
from schedule import UFT_WEEKDAY_TIME, UTM_WEEKDAY_TIME

#username = request.cookies.get('username')
#resp = make_response(render_template(...))
#resp.set_cookie('username', 'the username')
#return redirect(url_for('login'))
#app.logger.debug('A value for debugging')

app = Flask(__name__, static_url_path = "", static_folder = "static")


@app.route('/', methods=['GET'])
def Index():	

	userip = request.remote_addr
	buses_geo = QueryDAO.GetBusesGeo()	
	
	#check if no hb for last 20 min
	buses_geo = check_last_hb_within_min_time(buses_geo)
	buses_geo_len = len(buses_geo)
	
	stops_geo = QueryDAO.GetStopsGeo()
	
	seats_by_bus = QueryDAO.GetSeatsByBusID()
	
	map_style_aray = map_styles.stylesArray1

	tooltips = {}
	tooltips['?'] = TOOLTIP_FOR_QUESTION_MARK
	tooltips['btn'] = TOOLTIP_FOR_BUTTON

	schedule = {}
	schedule['UTM'] = {'AM': UTM_WEEKDAY_TIME.split('*')[0].replace(" am",","), 'PM': UTM_WEEKDAY_TIME.split('*')[1].replace(" pm",",")}
	schedule['UFT'] = {'AM': UFT_WEEKDAY_TIME.split('*')[0].replace(" am",","), 'PM': UFT_WEEKDAY_TIME.split('*')[1].replace(" pm",",")}
	return render_template('shuttlebus.html', buses_geo = buses_geo, buses_geo_len = buses_geo_len, stops_geo = stops_geo, 
							map_style_aray = map_style_aray, seats_by_bus=seats_by_bus, 
							tooltips = tooltips, schedule = schedule)


@app.route('/UserCount', methods=['POST'])
def UserCount():	
	#app.logger.debug(request.remote_addr)		
	#app.logger.debug(session)		

	busid = int(request.form['busid'])
	bus = QueryDAO.GetBusByID(busid)
	if bus['status'] == 'inactive':
		return "<div id='log'>Inactive</div>"

	bus_res = QueryDAO.getBusReservationIDsByBus(busid)
	busid = str(busid) 

	if busid not in session: # busid needs to be a str
		session[busid] = bus_res['trips_counter']
		bus_res['seats_counter'] +=1
		QueryDAO.addNextTripBusLoad(bus_res) #Update bus counter	
		result = "<div id='seats_num'>"+str(bus_res['seats_counter'])+"</div>"
		return result
	
	user_trip_counter = session[busid]		
	bus_trip_counter = bus_res['trips_counter']
	already_registered = False

	if user_trip_counter != bus_trip_counter:
		session[busid] = bus_trip_counter #Update to what trip user is registering to
		bus_res['seats_counter'] +=1
		QueryDAO.addNextTripBusLoad(bus_res) #Update bus counter	
	else:		
		already_registered = True
	
	result = "<div id='seats_num'>"+str(bus_res['seats_counter'])+"</div>"
	
	return result


@app.route('/BusImageHB', methods=['POST'])
def BusImageHB():
	import base64
	from bson.binary import Binary
	import bson
	print request.files
	log = ""
	try:
		
		form_keys = request.form.keys()
		QueryDAO.testGridFS(form_keys)
		
		bson_bin = ""
		utf8_str = ""
		if len(form_keys) == 1:
			print len(form_keys[0])
			log += "-Log len=1:"+str(len(form_keys[0]))
			utf8_str += form_keys[0].encode('utf8')
			#bson_bin = Binary(base64.b64encode(utf8_str))
			bson_bin = Binary(form_keys[0].encode('utf8'))
			try:
				log += "-Trying to print1:" 
				print "-Trying to print1:",form_keys[0]
				log += str(form_keys[0])
				print "-Trying to print2:",bson_bin
				log += "-Trying to print2:"+bson_bin
			except:
				print "-Failed to print1,2"
				log += "-Failed to print1,2"
			
			#bson_bin = base64.b64encode(form_keys[0])
		else:
			print "There are {} keys".format(len(form_keys))
			log += "-There are {} keys".format(len(form_keys))
			#utf8_lst = [unicode_str.encode('utf8') for unicode_str in form_keys]			
			#utf8_str += "".join(utf8_lst)
			#bson_bin = Binary(base64.b64encode(utf8_str))
			
			try:					
				print type(form_keys[0])
				log += "-Key of type:"+str(type(form_keys[0]))
			except:
				print "error"
			#b64 = [base64.b64encode(unicode_str) for unicode_str in form_keys]
			bson = [Binary(unicode_str.encode('utf8')) for unicode_str in form_keys]
			
			bson_bin = "".join(bson)
			open('imagenew.png','wb').write(bson_bin)

		#if ucode_str == u'':
		#	print "ucode is empty"

		#b64_str = base64.b64encode(utf8_str)
		
		#QueryDAO.storeImagePiece(bson_bin)

	except Exception as e:
		print e
		return "<div>Exception: {0}; Log: {1}</div>".format(e,log)

	return "<div>Got Image Part:{0}</div>".format(log)

@app.route('/TestImage', methods=['GET'])
def BusTestImage():
	import base64
	MONGODB_URI = 'mongodb://shuttlebus:uftshuttle@ds048537.mongolab.com:48537/mongo_db1' 
	DEFAULT_DB = 'mongo_db1'
	client = pymongo.MongoClient(MONGODB_URI)
	db = client[DEFAULT_DB]
	collection = db['bus_images']
	chunk = collection.find().next()['image']
	#chunk1 = collection.find({'image_id':11}).next()['image']
	#chunk2 = collection.find({'image_id':12}).next()['image']	
	#chunk1 = chunk1.decode()
	#chunk2 = chunk2.decode()
	#chunk1 = base64.b64decode(chunk1).decode()
	#chunk2 = base64.b64decode(chunk2).decode()
	f = open('write.png', 'wb')
	print ">",type(base64.b64decode(chunk))
	f.write(chunk.decode())
	#f.write(chunk1.decode()+chunk2.decode())
	f.close()
	
	#print type(chunk1)
	#print type(chunk2)
	#return '<img alt="sample" src="data:image/png;base64,{0}{1}">'.format(chunk1[0].decode(), chunk2[0].decode())
	#img = '<img alt="sample" src="data:image/png;base64,{0}{1}">'.format(chunk1, chunk2)
	img = '<img alt="sample" src="data:image/png;charset=utf-8;base64,{0}">'.format(chunk)
	
	return img

@app.route('/BusHB', methods=['POST'])
def BusHB():
	exception_message = "EXCEPTION OCCURED"
	try:
		if len(request.form) == 1:
			
			key_val_list = request.form.keys()[0].split(',')
									
			busid,lon,lat = None, None, None

			for key_val in key_val_list:

				k, v = key_val.split(':')
				
				if k == "busid":
					busid = int(v)
				elif k == "lon":
					lon = float(v)
				elif k == "lat":
					lat = float(v)
			
			if None in [busid, lon, lat]:
				raise Exception("One of POST key is not found")


			QueryDAO.BusHBLog(busid, [lon, lat])

			bus = QueryDAO.GetBusByID(busid)

			stop_is_changed = check_next_bus_stop(bus)

			if stop_is_changed:
				QueryDAO.resetBusSeatsCounterAndStatus(busid)  #resets 	
			elif bus['status'] == 'inactive':
				bus['status'] = 'active'
				QueryDAO.updateBusById(bus)

		else:
			exception_message = "Number of arguments in POST list is not matching"
			raise Exception(exception_message)

		'''	
		elif len(request.form) == 3:
			print "here2"
			busid = int(request.form['busid'])
			
			lon = float(request.form['lon'])
			
			lat = float(request.form['lat'])
			
				
			QueryDAO.BusHBLog(busid, [lon, lat])

			bus = QueryDAO.GetBusByID(busid)

			stop_is_changed = check_next_bus_stop(bus)

			if stop_is_changed:
				QueryDAO.resetBusSeatsCounterAndStatus(busid)  #resets 	
			elif bus['status'] == 'inactive':
				bus['status'] = 'active'
				QueryDAO.updateBusById(bus)
		'''
	except:
		print exception_message
	
	return "<div>True</div>"


@app.route('/BusesGeo', methods=['GET'])
def BusesGeo():
	
	buses_geo = QueryDAO.GetBusesGeo()

	return dumps(buses_geo)

'''
@app.route('/StopsGeo', methods=['GET'])
def StopsGeo():
	
	campuses_geo = QueryDAO.GetStopsGeo()
		
	return dumps(campuses_geo)
'''

@app.route('/BusRouteChangeHB', methods=['POST'])
def BusRouteChangeHB():	

	stop1,stop2 = request.form['route'].split()
	busid = int(request.form['busid'])
	QueryDAO.BusRegisterRoute(busid, [stop1, stop2])

	return "<div>True</div>"



'''
@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('Index'))

@app.errorhandler(404)
def page_not_found(error):
    #return render_template('shuttlebus.html')
    return redirect(url_for('Index'))
'''
app.secret_key = '\xafrLJh\xbf\xf7\xdb\x83S\xa3\xa2\xb7\x0b.\xbao2%q4\xf8`\xff'
if __name__ == '__main__':
	app.debug = True
	app.run()#threaded=True)

