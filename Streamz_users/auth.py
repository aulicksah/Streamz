import web
import model
import json
import requests
import hashlib
import responses
urls = ('/login', 'Login',
        '/logout', 'Logout',
        '/register', 'Register',)


                

class Register:
   
        def POST(self):
                """ REST API TO ADD NEW ENTRY  """
                data = web.data()
                fn=json.loads(data)['firstname']
                ln=json.loads(data)['lastname']
                ph=json.loads(data)['phone']
                eml=json.loads(data)['email']
                un=json.loads(data)['username']
                pwd=json.loads(data)['password']
                pwd1= hashlib.md5(pwd).hexdigest()
                p=model.new_user(fn,ln,ph,eml,un,pwd1)
                return p

	
        

class Login:
    
        def POST(self):
                """resr api to authentication"""
                data=web.data()
                un=json.loads(data)['username']
                pwd=json.loads(data)['password']
                passhash = hashlib.md5(pwd).hexdigest()
                id=model.check_user(un,passhash)
                return id


app = web.application(urls, globals())

if __name__ == '__main__':
        app.run()
