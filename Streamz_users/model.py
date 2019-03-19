import requests
import json
import web
import sqlite3
import hashlib

db = web.database(dbn='sqlite', db='streamz.db')



def new_user(firstname,lastname,phone,email,username,pwd,subscribers,likes,dislikes):
	id=db.insert('user', firstname=firstname, lastname=lastname,email=email,username=username,pwd=pwd,phone=phone,
subscribers=subscribers,likes=likes,dislikes=dislikes)
	params={'status':'Registered','username':username,'firstname':firstname,'lastname':lastname,'email':email,'phone':phone}
	return json.dumps(params)
	
def check_user(username,password):
    authdb = sqlite3.connect('streamz.db')
    #passhash = hashlib.md5(password).hexdigest()
    c= authdb.execute('select * from user where username=? and pwd=?',(username,password))
    row = c.fetchone()
    if row == None:
	logged={"loggedin":"false"}
	return logged  
     
		#params={'status':'NotLoggedIn'}
		#return json.dumps(params)
	#if pass2==password:
 	#raise web.seeother('/results')
	#return json.dumps({"loggedin":"false"})   
    else: 
			params={'status':'LoggedIn','username':username}
			return json.dumps(params)
	#error={"loggedin":"true","username":username} 

def get_user(username):
	authdb = sqlite3.connect('streamz.db')
	c= authdb.execute('select * from user where username=?',[username])
	row = c.fetchone()
	fn=row[1]
	ln=row[2]
	eml=row[3]
	un=row[4]
	ph=row[6]
	dob=row[7]
	coun=row[8]
	cat=row[9]
	subs=row[10]
	lik=row[11]
	dlik=row[12]
	param={'firstname':fn, 'lastname':ln,'email':eml,'username':un,'phone':ph,'dob':dob,'country':coun,
'category':cat,'subscribers':subs,'likes':lik,'dislikes':dlik}	
	return json.dumps(param)

def update_user_details(firstname,lastname,username,phone,email,category,dob,country):
	#id=db.update('user', firstname=firstname, lastname=lastname,username=username,phone=phone,email=email,dob=dob,country=country,category=category)
	
	#authdb = sqlite3.connect('streamz.db')
	#c= authdb.execute('update * from user where username=?',(username))
	#row = c.fetchone()
	return "success"

	


