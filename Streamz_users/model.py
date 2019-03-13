import requests
import json
import web
import sqlite3
import hashlib
import responses
db = web.database(dbn='sqlite', db='streamz.db')

url = 'http://0.0.0.0:8080/registerResponse'

def new_user(firstname,lastname,phone,email,username,pwd):
	id=db.insert('user', firstname=firstname, lastname=lastname,email=email,username=username,pwd=pwd,phone=phone)
	params={'status':'Registered','firstname':firstname,'id':id}
	#return resp.json(params)
	return json.dumps(params)
	
def check_user(username,password):
    authdb = sqlite3.connect('streamz.db')
    #passhash = hashlib.md5(password).hexdigest()
    c= authdb.execute('select * from user where username=? and pwd=?',(username,password))
    row = c.fetchone()
    if row == None:
     
		params={'status':'NotLoggedIn'}
		return json.dumps(params)
	#if pass2==password:
 	#raise web.seeother('/results')
	#return json.dumps({"loggedin":"false"})   
    else: 
			params={'status':'LoggedIn','username':username}
			return json.dumps(params)
	#error={"loggedin":"true","username":username} 
	


