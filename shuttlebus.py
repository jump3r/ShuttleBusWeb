from flask import Flask
from flask import Markup #Markup('<em>Marked up</em> &raquo; HTML').striptags()
from flask import Flask, session, redirect, url_for, escape, request, render_template

import sys
import pymongo

#username = request.cookies.get('username')
#resp = make_response(render_template(...))
#resp.set_cookie('username', 'the username')
#return redirect(url_for('login'))
#app.logger.debug('A value for debugging')

app = Flask(__name__)

@app.route('/', methods=['GET'])
def Index():
	print request.form

	return render_template('shuttlebus.html')

@app.route('/usercount', methods=['POST', 'GET'])
def RegisterForBus():
	print request.args.get('id')
	app.logger.debug('A value for debugging')	
	#resp = make_response(render_template('shuttlebus.html'))
	#resp.headers['X-Something'] = 'A value'
	
	return "<div id='log'>Hello</div>"



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
	app.run()

