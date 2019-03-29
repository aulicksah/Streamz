""" Basic todo list using webpy 0.3 """
import web
import requests
import model
from web import form
import json
### Url mappings

urls = (
	'/', 'Index',
	'/play/(\d+)','Play',
	'/home', 'Homepage',
	'/register', 'Register',
	'/about', 'About',
	'/uploads', 'Uploads',
	'/statistics', 'Statistics',
	'/uploadvideo','Uploadvideo',
	'/uploaded','Uploaded',
	'/comment','Comment',
	'/uploadvideoinfo/(\d+)','UploadVideoInfo',
	'/uploadvideoinfo','UploadVideoInfo',
	'/logout','Logout',
	'/search','Search',
	'/upload','MyUpload',
	'/profile','Profile',
	'/updateprofile','UpdateProfile',
	'/videos/(\d+)','Videos',
	'/thumbnails/(\d+)','Thumbnails', 
	'/videoname/(\d+)','VideoName',
	'/uploader/(\d+)','Uploader',
)


### Templates
render = web.template.render('templates', base='base')

app = web.application(urls, globals())

if web.config.get('_session') is None:
    session = web.session.Session(app, web.session.DiskStore('sessions'), {'user':'username'})
    web.config._session = session
else:
    session = web.config._session

class Search:
	def POST(self):
		i = web.input()
		s = model.send_search(i.searchtext)
		t=s['id']
 		videonames=[]
		for i in range(len(t)):
			videonames.append(model.get_videoname(t[i])['name'])
		uploaders=[]
		for i in range(len(t)):
			uploaders.append(model.get_uploader(t[i])['uploader'])
		return render.search(session.user,t,videonames,uploaders)
		
		#return s['id'][0]"""	

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
		raise web.seeother('/about')

class UploadVideoInfo:

	def GET(self,video_id):
		id=int(video_id)
		s=model.get_videodesc(id)
		#if s['id']==session.user:
		id1=s['id']
		name=s['name']
		uploader=s['uploader']
		description=s['description']
		category=s['category']
		countries=s['countries']
		age=s['age']
	
		#return type(countries)
		return render.uploadvideoinfo(session.user,id1,name,description,category,countries,age)

	def POST(self):

		i = web.input()
		#s = search_upload_video(i.searchtext)	
		th = web.input(mythumbnail={})
			
		countries=[]
		if hasattr(i, 'India'):
			countries.append({'country':i.India})
		if hasattr(i, 'UnitedStates'):
			countries.append({'country':i.UnitedStates})
		if hasattr(i, 'Australia'):
			countries.append({'country':i.Australia})
		if hasattr(i, 'UnitedKingdom'):
			countries.append({'country':i.UnitedKingdom})
		if hasattr(i, 'Germany'):
			countries.append({'country':i.Germany})
		if countries==[]:
			countries= "None"
		p=model.upload_video_info(i.id,i.name,i.description,i.tags.split(","),countries,i.category,session.user,i.age,th)
		raise web.seeother('/about')


class Play:
	def GET(self,video_id):
		""" Show page """
		if session.user=='username':
			raise web.seeother('/')
		else: 	
			return render.play(session.user,video_id)

class Videos:
    def GET(self,video_id):
        # GET THE ID OF THE VIDEO
		id=int(video_id)
		s=model.get_video(id)		
		return s

class Thumbnails:
    def GET(self,video_id):
        # GET THE ID OF THE VIDEO
		id=int(video_id)
		s=model.get_thumbnail(id)		
		return s

class VideoName:
    def GET(self,video_id):
        # GET THE ID OF THE VIDEO
		id=int(video_id)
		s=model.get_videoname(id)		
		return s

class Uploader:
    def GET(self,video_id):
        # GET THE ID OF THE VIDEO
		id=int(video_id)
		s=model.get_uploader(id)		
		return s



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



class Uploadvideo:
	def GET(self):
		""" Show page """		
		return render.uploadvideo()

	def POST(self):
		
		x = web.input(myfile={})
		r = model.upload_video(x,session.user)
		id=str(r['id'])
		raise web.seeother('/uploadvideodesc/'+id)
					
	

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
