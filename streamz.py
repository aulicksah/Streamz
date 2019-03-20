""" Basic todo list using webpy 0.3 """
import web
import requests
import model
from web import form
import json
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
	'/uploadvideoinfo','UploadVideoInfo',
	'/logout','Logout',
	'/search','Search',
	'/upload','MyUpload',
	'/profile','Profile',
	'/updateprofile','UpdateProfile',

 
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
			if s['status']== "LoggedIn":
				session.loggedin = True
        		session.user = s['username']
			#return s
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
		s=model.new_user(fn,ln,ph,eml,un,pwd)
		if s['status']== "Registered":
			session.loggedin = True
			session.user = s['username']
			#return s
        	raise web.seeother('/updateprofile') 

class UpdateProfile:
	profile = form.Form(
	form.Textbox('firstname'),
	form.Textbox('lastname'),
	form.Textbox('phone'),
	form.Textbox('email'),
	form.Password('username'),
	form.Textbox('dob'),
	form.Textbox('country'),
	form.Button('Submit'),
	)

	def GET(self):
		profile=self.profile
		s=model.get_profile(session.user)
		fn=s['firstname']
		ln=s['lastname']
		cat=s['category']
		db=s['dob']
		eml=s['email']
		ph=s['phone']
		return render.updateprofile(profile,session.user,fn,ln,cat,db,eml,ph)

	def POST(self):
		i = web.input()
		s = model.update_profile(i.firstname,i.lastname,i.username,i.phone,i.email,i.category,i.country,i.dob)
		return s

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
		"""filedir = '/path/where/you/want/to/save' # change this to the directory you want to store the file in.
		if 'myfile' in x: # to check if the file-object is created
			filepath=x.myfile.filename.replace('\\','/') # replaces the windows-style slashes with linux ones.
			filename=filepath.split('/')[-1] # splits the and chooses the last part (the filename with extension)
			fout = open(filedir +'/'+ filename,'w') # creates the file where the uploaded file should be stored
			fout.write(x.myfile.file.read()) # writes the uploaded file to the newly created file.
			fout.close() # closes the file, upload complete."""
		filepath=x.myfile.filename.replace('\\','/')
		multipart_form_data = {'image': (x.myfile.filename, open(x.myfile.file, 'rb'))}
		response = requests.post('http://0.0.0.0:5050/upload', files=multipart_form_data)
		return response
					

class UploadVideoDesc:

	def GET(self,video_name):		
		return render.uploadvideodesc(video_name)

class UploadVideoInfo:

	def POST(self):

		i = web.input()
		#s = search_upload_video(i.searchtext)	
		x = web.input(mythumbnail={})
		filedir = 'http://0.0.0.0:5050/static/image' # change this to the directory you want to store the file in.
		if 'myfile' in x: # to check if the file-object is created
			filepath=x.myfile.filename.replace('\\','/') # replaces the windows-style slashes with linux ones.
			filename=filepath.split('/')[-1] # splits the and chooses the last part (the filename with extension)
			fout = open(filedir +'/'+ filename,'w') # creates the file where the uploaded file should be stored
			fout.write(x.myfile.file.read()) # writes the uploaded file to the newly created file.
			fout.close() # closes the file, upload complete.
			
		countries=[]
		if hasattr(i, 'India'):
			countries.append(i.India)
		if hasattr(i, 'UnitedStates'):
			countries.append(i.UnitedStates)
		if hasattr(i, 'Australia'):
			countries.append(i.Australia)
		if hasattr(i, 'UnitedKingdom'):
			countries.append(i.UnitedKingdom)
		if hasattr(i, 'Germany'):
			countries.append(i.Germany)
		if countries==[]:
			countries= "None"
		#p=model.upload_video_info(i.name,i.description,i.tags,i.location,countries,"category",session.user,i.age)
		return i.mythumbnail
		
		"""if i.Germany:
			return i.Australia
		else:
			return i.Australia"""


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

class MyUpload:

	def GET(self):
		""" Show page """
		
		return render.upload()


if __name__ == "__main__":
   app.run()
