from flask import Flask
from flask import g
from flask import Markup 
from flask import session, redirect, url_for, escape, request, render_template

import sys
import pymongo
from bson.json_util import dumps
from queryDAO import QueryDAO

from bus_utils import check_next_bus_stop, check_if_on_campus
from bus_utils import check_last_hb_within_min_time
from bus_utils import TOOLTIP_FOR_QUESTION_MARK, TOOLTIP_FOR_BUTTON
from bus_utils import parse_bushb_gsm, parse_bushb_gps

import map_styles 
from schedule import UFT_WEEKDAY_TIME, UTM_WEEKDAY_TIME
import time
#username = request.cookies.get('username')
#resp = make_response(render_template(...))
#resp.set_cookie('username', 'the username')
#return redirect(url_for('login'))
#app.logger.debug('A value for debugging')

app = Flask(__name__, static_url_path = "", static_folder = "static")


@app.route('/forgetme', methods=['GET'])
def ForgetMe():
	
	keys_to_del = []

	for k in session:
		keys_to_del.append(k)

	for k in keys_to_del:
		session.pop(k)
	print session
	return redirect(url_for('Index'))

@app.route('/presentation', methods=['GET'])
def DemoPresentation():	
	youtube_link = QueryDAO.getYoutubeVideo()

	return render_template('presentation.html', youtube_link = youtube_link )

@app.route('/controlpanel', methods=['GET'])
def DemoControlPanel():		

	return render_template('controlpanel.html')

@app.route('/DemoAction', methods=['POST'])
def DemoAction():		
	action = request.form['action'].strip()
	if action == "START":
		QueryDAO.updateDBrefreshRate(0.5)
		#from test_utils import simulated_demo
		#simulated_demo()				
		
	elif action == "STOP":
		QueryDAO.updateDBrefreshRate(-1.0)		
		
	return "<div>True</div>"


@app.route('/night', methods=['GET'])
def IndexNight():	
	#Nav bar background-color: #727581;
	return Index(night = True, navcolor = {"background-color":"background-color: #727581;"})


@app.route('/', methods=['GET'])
def Index(night = False, navcolor = {"background-color": ""}):	
	print session
	userip = request.remote_addr
	buses_geo = QueryDAO.GetBusesGeo()	
	
	#check if no hb for last 20 min
	buses_geo = check_last_hb_within_min_time(buses_geo)
	buses_geo_len = len(buses_geo)
	
	#STOPS
	stops_geo = QueryDAO.GetStopsGeo()
	
	#SEATS FOR EACH BUS
	seats_by_bus = QueryDAO.GetSeatsByBusID()
	
	#MAP STYLE
	'''
	local_time = time.localtime().tm_hour	
	if local_time > 18 or local_time < 5 or night:
		map_style_array = map_styles.greyStyleArray
		navcolor = {"background-color":"background-color: #727581;"}		
	elif local_time >= 5 or local_time <= 18:
		map_style_array = map_styles.dayStyleArray

	#Server is not on east coast
	if time.tzname != ('EST', 'EDT'):
		map_style_array = map_styles.dayStyleArray
	'''
	map_style_array = map_styles.dayStyleArray
	if night:		
		map_style_array = map_styles.greyStyleArray
		navcolor = {"background-color":"background-color: #727581;"}

	#INFO FOR INFO BOXES
	tooltips = {}
	tooltips['?'] = TOOLTIP_FOR_QUESTION_MARK
	tooltips['btn'] = TOOLTIP_FOR_BUTTON

	#BUS REFRESH RATE
	bus_update_rate = QueryDAO.getJSBusUpdateRate_ForDemo();

	#SCHEDULE FROM
	schedule = {}
	schedule['UTM'] = {'AM': UTM_WEEKDAY_TIME.split('*')[0].replace(" am",","), 'PM': UTM_WEEKDAY_TIME.split('*')[1].replace(" pm",",")}
	schedule['UFT'] = {'AM': UFT_WEEKDAY_TIME.split('*')[0].replace(" am",","), 'PM': UFT_WEEKDAY_TIME.split('*')[1].replace(" pm",",")}
	return render_template('shuttlebus.html', buses_geo = buses_geo, buses_geo_len = buses_geo_len, stops_geo = stops_geo, 
							map_style_array = map_style_array, seats_by_bus=seats_by_bus, tooltips = tooltips, 
							schedule = schedule, navcolor = navcolor, bus_update_rate = bus_update_rate)


@app.route('/SavePhoneNumber', methods=['POST'])
def SavePhoneNumber():
	result = {}
	new_number = request.form['phone_number'].strip()
	
	if len(new_number) == 0:
		result['snackbar_notification'] = "Your cannot have an empty phone number."
		return dumps(result)
	#Change all sms listeners to the new nubmer
	#all_subscribed_buses = []
	bus_res_to_update = []
	print session
	if "phone_number" in session:

		old_number = session["phone_number"]
		bus_res = QueryDAO.GetAllBusReservations()
		
		for bus in bus_res:
			if old_number in bus["sms_listeners"]:
				bus['sms_listeners'].remove(old_number)
				bus['sms_listeners'].append(new_number)
				bus_res_to_update.append({'bus_id':bus['bus_id'], 'sms_listeners':bus['sms_listeners']})
			#all_subscribed_buses.append(bus['bus_id'])

		if len(bus_res_to_update) != 0:
			QueryDAO.UpdateBusSMSListeners(bus_res_to_update)
	else:				
		session["phone_number"] = new_number
		#bus_res_to_update = getBusesSubscribedTo(session) #buses user is subscribed to and they have not arrived
		#subscribedto_not_arrived = GetSubscribedToBusesNotArrivedYet()
			
	#Get all phone numbers
	#Find current
	result["snackbar_notification"] = "Your phone number has been updated. Currently you are not subscribed to any bus SMS notifications"	
	if len(bus_res_to_update) != 0:
		result["snackbar_notification"] = "Your phone number has been updated. Currently you are subscribed to SMS notification for bus"
		result["snackbar_notification"] += " #{}"*len(bus_res_to_update) + "."
		result["snackbar_notification"] = result["snackbar_notification"].format(*[bus['bus_id'] for bus in bus_res_to_update])	

	return dumps(result)

	
@app.route('/SeatsCounter', methods=['GET'])
def GetSeatsCounter():
	bus_reservations = QueryDAO.GetSeatsByBusID()

	return dumps(bus_reservations)


@app.route('/UserCount', methods=['POST'])
def UserCount():	
	#app.logger.debug(request.remote_addr)		
	app.logger.debug(session)		
	
	result = {}
	busid = int(request.form['busid'])
	to_sms_subscribe = bool(str(request.form['subscribe']) == "1")
	
	bus = QueryDAO.GetBusByID(busid)
	if bus['status'] == 'inactive':		
		result['status'] = "Inactive"
		return dumps(result)
	
	bus_res = QueryDAO.getBusReservationIDsByBus(busid)
	busid = str(busid) 

	if busid not in session: # busid needs to be a str
		print "NOT IN SESSION"
		session[busid] = str(bus_res['trips_counter'])
		print session
		bus_res['seats_counter'] +=1
		QueryDAO.addNextTripBusLoad(bus_res) #Update bus counter	
		#result = "<div id='seats_num'>"+str(bus_res['seats_counter'])+"</div>"
		result['seats_num'] = str(bus_res['seats_counter'])
		if to_sms_subscribe and "phone_number" in session:
			bus_res['sms_listeners'].append(session["phone_number"])
			result['snackbar_notification'] = "You were successfully subscribed to SMS notification for bus #"+busid
			QueryDAO.addNextTripBusLoad(bus_res) #Update bus counter	
		else:
			result['snackbar_notification'] = "You were added to the shuttle bus. Thank you for sharing your intention."
		
		return dumps(result)
	
	user_trip_counter = str( session[busid] )
	bus_trip_counter = str(bus_res['trips_counter'])
	
	if user_trip_counter != bus_trip_counter:
		
		session[busid] = bus_trip_counter #Update to what trip user is registering to
		bus_res['seats_counter'] +=1		
		if to_sms_subscribe and "phone_number" in session:
			print "PHONE IN SESSION"
			bus_res['sms_listeners'].append(session["phone_number"])
			QueryDAO.addNextTripBusLoad(bus_res) #Update bus counter	
		else:
			print "PHONE NOT IN SESSION"

	elif user_trip_counter == bus_trip_counter and to_sms_subscribe:
		
		if "phone_number" in session and  session["phone_number"] not in bus_res['sms_listeners']:
			
			bus_res['sms_listeners'].append(session["phone_number"])
			QueryDAO.addNextTripBusLoad(bus_res) #Add number to sms	listeners
			result['snackbar_notification'] = "You were successfully subscribed to SMS notification for bus #"+busid
		else:
			result['snackbar_notification'] = "You are already added to the shuttle bus."
		
	else:
		result['snackbar_notification'] = "You are already added to the shuttle bus."
	
	result['seats_num'] = str(bus_res['seats_counter'])
	
	return dumps(result)


@app.route('/BusHB', methods=['POST'])
def BusHB():
	
	exception_message = "EXCEPTION OCCURED"
	print request.form.keys()
	try:
		if len(request.form) == 1:
			
			key_val_list = request.form.keys()[0].split(',')

			busid,lon,lat = None, None, None
			print key_val_list[0]
			if key_val_list[0] == "mode:gsm":
				busid,lon,lat = parse_bushb_gsm(key_val_list[1:])				
			else:
				busid,lon,lat = parse_bushb_gps(key_val_list[1:])									
			
			if None in [busid, lon, lat]:
				raise Exception("One of POST keys is not found")
			print busid, lon, lat

			if lon == 0.0 or lat == 0.0:
				raise Exception("Lon or Lat is zero. Keeping previous location")
			else:
				QueryDAO.BusHBLog(busid, [lon, lat])

			bus = QueryDAO.GetBusByID(busid)

			stop_is_changed = check_next_bus_stop(bus)
			is_within_campus = check_if_on_campus(bus)
			if stop_is_changed:
				QueryDAO.resetBusSeatsCounterAndStatus(busid)  
				bus['status'] = 'On campus'
				QueryDAO.updateBusById(bus)

			elif bus['status'] == 'Inactive' and is_within_campus:
				bus['status'] = 'On campus'
				QueryDAO.updateBusById(bus)

			elif bus['status'] == 'Inactive' and not is_within_campus:
				bus['status'] = 'On Route'
				QueryDAO.updateBusById(bus)

			elif bus['status'] == 'On campus' and not is_within_campus:
				bus['status'] = 'On Route'
				QueryDAO.updateBusById(bus)

		else:
			exception_message = "Number of arguments in POST list is not matching"
			raise Exception(exception_message)
		
	except Exception as e:
		print exception_message
		print e
		return "<div>{}.</div>".format(e)
	
	return "<div>True</div>"


@app.route('/BusesGeo', methods=['GET'])
def BusesGeo():
	
	buses_geo = QueryDAO.GetBusesGeo()

	return dumps(buses_geo)


@app.route('/BusRouteChangeHB', methods=['POST'])
def BusRouteChangeHB():	

	stop1,stop2 = request.form['route'].split()
	busid = int(request.form['busid'])
	QueryDAO.BusRegisterRoute(busid, [stop1, stop2])

	return "<div>True</div>"


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
	app.run(threaded=True)

