""" Basic todo list using webpy 0.3 """
import web
import requests
import model
from web import form
import json
import datetime
from datetime import date
import ast
### Url mappings

urls = (
	'/', 'Index',
	'/register', 'Register',
	'/home', 'Homepage',
	'/play/(\d+)','Play',
	'/uploadvideo','Uploadvideo',
	'/uploadvideoinfo/(\d+)','UploadVideoInfo',
	'/uploadvideoinfo','UploadVideoInfo',
	'/editvideo/(\d+)','EditVideo',
	'/deletevideo/(\d+)','DeleteVideo',
	'/comment','Comment',
	'/logout','Logout',
	'/search','Search',
	'/profile','Profile',
	'/updateprofile','UpdateProfile',
	'/about', 'About',
	'/uploads', 'Uploads',
	'/statistics', 'Statistics',
	'/videos/(\d+)','Videos',
	'/thumbnails/(\d+)','Thumbnails', 
	'/profilepic/(\d+)','ProfilePic',
	'/coverpic/(\d+)','CoverPic',
	'/like','Like',
	'/dislike','Dislike',
	'/nonelike','Nonelike',
	'/subscribe','Subscribe',
	'/unsubscribe','Unsubscribe',
	'/demo','Demo',
	'/updatevideo','UpdateVideo',

)


### Templates
render = web.template.render('templates', base='base')

app = web.application(urls, globals())

if web.config.get('_session') is None:
    session = web.session.Session(app, web.session.DiskStore('sessions'), {'user':'username'})
    web.config._session = session
else:
    session = web.config._session

class DeleteVideo:

	def POST(self,video_id):
		id=int(video_id)
		s=model.delete_video(id)
		if s['status']=="Deleted":
			raise web.seeother('/uploads')

class Uploads:

	def GET(self):
		s=model.get_uploads(session.user)
		t=s['videouploads']
 		videonames=[]
		for i in range(len(t)):
			videonames.append(model.get_videoname(t[i])['name'])
		uploaders=[]
		for i in range(len(t)):
			uploaders.append(model.get_uploader(t[i])['uploader'])
		return render.uploads(session.user,t,videonames,uploaders)

class Subscribe:
	def POST(self):
		i = web.input()
		s=model.subscribe(i.username,i.uploader)
		if s['subscribestatus']=="Subscribed":
			raise web.seeother('/play/'+i.videoid)


class Unsubscribe:
	def POST(self):
		i = web.input()
		s=model.unsubscribe(i.username,i.uploader)
		if s['subscribestatus']=="Unsubscribed":
			raise web.seeother('/play/'+i.videoid)


class Like:
	def POST(self):
		i = web.input()
		s=model.update_like(i.username,i.videoid)
		if s['likestatus']=="Liked":
			raise web.seeother('/play/'+i.videoid)

class Dislike:
	def POST(self):
		i = web.input()
		s=model.update_dislike(i.username,i.videoid)
		if s['likestatus']=="Disliked":
			raise web.seeother('/play/'+i.videoid)

class Nonelike:
	def POST(self):
		i = web.input()
		s=model.update_nonelike(i.username,i.videoid)
		if s['likestatus']=="Noneliked":
			raise web.seeother('/play/'+i.videoid)

class UpdateVideo:
	def POST(self):

		i = web.input()
		th = web.input(mythumbnail={})
			
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
			countries= None
		if i.age=="None":
			age=0
		elif i.age=="10+":
			age=10
		else:
			age=18
		t=str(i.tags)
		tg=json.dumps(t.split(","))
		p=model.update_video(i.id,i.name,i.description,tg,countries,i.category,session.user,age,th)
		raise web.seeother('/play/'+i.id)
		#return p

class EditVideo:

	def POST(self,video_id):
		id=int(video_id)
		s=model.get_videodesc(id)
		#if s['id']==session.user:
		id1=s['id']
		name=s['name']
		uploader=s['uploader']
		description=s['description']
		category=s['category']
		if s['countries']!=None:
			countries=ast.literal_eval(s['countries'])
		else:
			countries=None
		age=s['age']		
		tags=ast.literal_eval(s['tags'])
		return render.editvideo(session.user,int(id1),name,description,category,countries,int(age),','.join(tags))
		

	

class UpdateProfile:
	
	def GET(self):
		
		s=model.get_profile(session.user)
		fn=s['firstname']
		ln=s['lastname']
		cat=s['category']
		db=s['dob']
		abt=s['about']
		eml=s['email']
		ph=s['phone']
		return render.updateprofile(session.user,fn,ln,abt,cat,db,eml,ph)
		return s

	def POST(self):
		i = web.input()
		x = web.input(myprofilepic={})
		y = web.input(mycoverpic={})
		s = model.update_profile(i.firstname,i.lastname,i.username,i.about,i.phone,i.email,i.category,i.country,i.dob,x,y)
		return s

class Index:

	login = form.Form(
	form.Textbox('username'),
	form.Password('password'),
	form.Button('Login'),
	)

	def GET(self):

		if session.user!='username':
				raise web.seeother('/home')
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
		s=model.new_user(fn,ln,ph,eml,un,pwd,str(date.today()))
		if s['status']== "Registered":
			session.loggedin = True
			session.user = s['username']
			#return s
        	raise web.seeother('/updateprofile')
		#return s

class Search:


	def POST(self):
		i = web.input()
		s = model.send_search(i.searchtext,model.calculate_Age(model.get_dob(session.user)['dob']),model.get_country(session.user)['country'])
		t=s['id']
 		videonames=[]
		for i in range(len(t)):
			videonames.append(model.get_videoname(t[i])['name'])
		uploaders=[]
		for i in range(len(t)):
			uploaders.append(model.get_uploader(t[i])['uploader'])
		return render.search(session.user,t,videonames,uploaders)


class Homepage:
	def GET(self):
		if session.user=='username':
				raise web.seeother('/')
		else: 	
			return render.homepage(session.user)

class Play:
	def GET(self,video_id):
		if session.user=='username':
			raise web.seeother('/')
		else:
			ls=model.get_likestatus(session.user,video_id)
			ss=model.get_subscribestatus(session.user,model.get_uploader(video_id)['uploader'])
			return render.play(session.user,video_id,model.get_videoname(video_id)['name'],model.get_uploader(video_id)['uploader'],model.get_description(video_id)['description'],ls['likestatus'],ss['subscribestatus'])

class Uploadvideo:
	def GET(self):	
		return render.uploadvideo()

	def POST(self):
		
		x = web.input(myfile={})
		r = model.upload_video(x,session.user)
		id=str(r['id'])
		raise web.seeother('/uploadvideoinfo/'+id)

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
		
		return render.uploadvideoinfo(session.user,id1,name,description,category,countries,age)

	def POST(self):

		i = web.input()
		th = web.input(mythumbnail={})
			
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
			countries= None
		if i.age=="None":
			age=0
		elif i.age=="10+":
			age=10
		else:
			age=18
		t=str(i.tags)
		tg=json.dumps(t.split(","))
		p=model.upload_video_info(i.id,i.name,i.description,tg,countries,i.category,session.user,age,th)
		raise web.seeother('/about')


class Comment:

	def POST(self):
		i = web.input()
		s = model.send_comment(i.commenttext)
		return i	
"""-----------------------------------------------------------------------------"""
class Videos:
    def GET(self,video_id):
		id=int(video_id)
		s=model.get_video(id)		
		return s

class Thumbnails:
    def GET(self,video_id):
		id=int(video_id)
		s=model.get_thumbnail(id)		
		return s

class ProfilePic:
    def GET(self,username):
		s=model.get_profilepic(username)		
		return s

class CoverPic:
    def GET(self,username):
		s=model.get_coverpic(username)		
		return s

class Logout:
    def GET(self):
        session.kill()
        raise web.seeother('/')
"""------------------------------------------------------------------"""		


class About:
	def GET(self):
		if session.user=='username':
			raise web.seeother('/')
		else: 	
			return render.about(session.user)



class Demo:
	def GET(self):
		return render.demo()

class Statistics:

	def GET(self):
		s=model.get_uploads(session.user)
		t=s['videouploads']
 		videonames=[]
		for i in range(len(t)):
			videonames.append(model.get_videoname(t[i])['name'])
		uploaders=[]
		for i in range(len(t)):
			uploaders.append(model.get_uploader(t[i])['uploader'])
		return render.statistics(session.user,t,videonames,uploaders)



if __name__ == "__main__":
   app.run()
