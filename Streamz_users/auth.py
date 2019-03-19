import web
import model
import json
import requests
import hashlib

urls = ('/login', 'Login',
        '/logout', 'Logout',
        '/register', 'Register',
	'/profile', 'Profile',
	'/updateprofile', 'UpdateProfile',)


                

class Register:
   
        def POST(self):
                data = web.data()
                fn=json.loads(data)['firstname']
                ln=json.loads(data)['lastname']
                ph=json.loads(data)['phone']
                eml=json.loads(data)['email']
                un=json.loads(data)['username']
                pwd=json.loads(data)['password']
                pwd1= hashlib.md5(pwd).hexdigest()
                p=model.new_user(fn,ln,ph,eml,un,pwd1,0,0,0)
                return p

	"""Set subscribers and likes to 0"""
        

class Login:
    
        def POST(self):
                data=web.data()
                un=json.loads(data)['username']
                pwd=json.loads(data)['password']
                passhash = hashlib.md5(pwd).hexdigest()
                id=model.check_user(un,passhash)
                return id
	

class Profile:
    
        def POST(self):
                data=web.data()
                user=json.loads(data)['username']
                s=model.get_user(user)
                return s

class UpdateProfile:
    
        def POST(self):
                data=web.data()
                fn=json.loads(data)['firstname']
                ln=json.loads(data)['lastname']
                un=json.loads(data)['username']
                ph=json.loads(data)['phone']
                eml=json.loads(data)['email']
		cat=json.loads(data)['category']
		dob=json.loads(data)['dob']
		cntr=json.loads(data)['country']
                p=model.update_user_details(fn,ln,un,ph,eml,cat,dob,cntr)
                return p

app = web.application(urls, globals())

if __name__ == '__main__':
        app.run()
