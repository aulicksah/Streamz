""" Basic todo list using webpy 0.3 """
import web
import requests
import model
from web import form
import json
import responses
### Url mappings

urls = (
	'/', 'Index',
	'/video','Video',
	'/home', 'Homepage',
	'/register', 'Register',
	'/about', 'About',
	'/uploads', 'Uploads',
	'/statistics', 'Statistics',
	'/uploadvideo','Uploadvideo',
	'/uploaded','Uploaded',
	'/comment','Comment',
	'/uploadvideodesc/(.*)','UploadVideoDesc',
	'/logout','Logout',
	'/search','Search'

 
)


### Templates
render = web.template.render('templates', base='base')

app = web.application(urls, globals())

if web.config.get('_session') is None:
    session = web.session.Session(app, web.session.DiskStore('sessions'), {'user':'username'})
    web.config._session = session
else:
    session = web.config._session

class Index:

	login = form.Form(
	form.Textbox('username'),
	form.Password('password'),
	form.Button('Login'),
	)

	def GET(self):

		login = self.login()
		return render.index(login)
		
	def POST(self):
		login = self.login()
		if not login.validates():            
			return render.index(login)
		else:
			un=login.d.username
			pwd=login.d.password
			s= model.check_user(un,pwd)			
			if s!= "NotLoggedIn":
				session.loggedin = True
        		session.user = un
			#return session.user
        	raise web.seeother('/home') 

class Register:
	register = form.Form(
	form.Textbox('firstname'),
	form.Textbox('lastname'),
	form.Textbox('phone'),
	form.Textbox('email'),
	form.Password('username'),
	form.Password('password'),
	form.Button('Register'),
	)

	def GET(self):
		""" Show page """
		register = self.register()
		return render.register(register)

	def POST(self):
		register = self.register()
		if not register.validates():            
			return "Unsuccessful"

		fn=register.d.firstname
		ln=register.d.lastname
		ph=register.d.phone
		eml=register.d.email
		un=register.d.username
		pwd=register.d.password
		p=model.new_user(fn,ln,ph,eml,un,pwd)
		return p

class Logout:
    def GET(self):
        session.kill()
        raise web.seeother('/')

class Homepage:
	def GET(self):
		""" Show page """
		if session.user=='username':
				raise web.seeother('/')
		else: 	
			return render.homepage(session.user)

class Video:
	def GET(self):
		""" Show page """
		if session.user=='username':
				raise web.seeother('/')
		else: 	
			return render.video(session.user)

class Uploadvideo:
	def GET(self):
		""" Show page """		
		return render.uploadvideo()

	def POST(self):
		x = web.input(myfile={})
		filedir = 'static/video' # change this to the directory you want to store the file in.
		if 'myfile' in x: # to check if the file-object is created
			filepath=x.myfile.filename.replace('\\','/') # replaces the windows-style slashes with linux ones.
			filename=filepath.split('/')[-1] # splits the and chooses the last part (the filename with extension)
			fout = open(filedir +'/'+ filename,'w') # creates the file where the uploaded file should be stored
			fout.write(x.myfile.file.read()) # writes the uploaded file to the newly created file.
			fout.close() # closes the file, upload complete.
			raise web.seeother('/uploadvideodesc/'+filename)		

class UploadVideoDesc:

	def GET(self,video_name):		
		return render.uploadvideodesc(video_name)

	def POST(self):
		x = web.input()


class Search:

	def POST(self):
		i = web.input()
		s = model.send_search(i.searchtext)
		return s	

class Comment:

	def POST(self):
		i = web.input()
		s = model.send_comment(i.commenttext)
		return i	


"""------------------------------------------------------------------"""		


class About:
	def GET(self):
		""" Show page """
		if session.user=='username':
			raise web.seeother('/')
		else: 	
			return render.about(session.user)

class Uploads:

	def GET(self):
		""" Show page """
		
		return render.uploads()

class Statistics:

	def GET(self):
		""" Show page """
		
		return render.statistics()


if __name__ == "__main__":
   app.run()
