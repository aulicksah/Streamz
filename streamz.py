""" Basic todo list using webpy 0.3 """
import web
import model
from web import form

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
	'/searchresults','SearchResults',
	'/uploadvideodesc','UploadVideoDesc'

 
)


### Templates
render = web.template.render('templates', base='base')

app = web.application(urls, globals())

if web.config.get('_session') is None:
    session = web.session.Session(app, web.session.DiskStore('sessions'), {'user':'username'})
    web.config._session = session
else:
    session = web.config._session

class UploadVideoDesc:

	def GET(self):
		return render.uploadvideodesc()

	def POST(self):
		x = web.input()
		

		

class Uploaded:

	def POST(self):
		x = web.input(myfile={})
		filedir = 'static/video' # change this to the directory you want to store the file in.
		if 'myfile' in x: # to check if the file-object is created
			filepath=x.myfile.filename.replace('\\','/') # replaces the windows-style slashes with linux ones.
			filename=filepath.split('/')[-1] # splits the and chooses the last part (the filename with extension)
			fout = open(filedir +'/'+ filename,'w') # creates the file where the uploaded file should be stored
			fout.write(x.myfile.file.read()) # writes the uploaded file to the newly created file.
			fout.close() # closes the file, upload complete.
			s = model.upload_video(filename)
			return s

class SearchResults:


	def POST(self):
		i = web.input()
		s = model.send_search(i.searchtext)
		return s

class Comment:


	def POST(self):
		i = web.input()
		s = model.send_comment(i.commenttext)
		return s		

class Index:

	login = form.Form(
	form.Textbox('email'),
	form.Password('password'),
	form.Button('Login'),
	)

	def GET(self):

		login = self.login()
		return render.index(login)
		

		""" Show page """
		"""print 'session', session
		session.user='arnenupharsah'
		if session.user=='username':
		   return render.index(login)
		else:
			return 'Hello, %s!' % session.user"""
		

				

	def POST(self):
		login = self.login()
		if not login.validates():            
			return render.index(login)
		else:
			un=login.d.email
			pwd=login.d.password
			s= model.check_user(un,pwd)
			return s
			"""if s:
				session.loggedin = True
        		session.username = i.username
        		raise web.seeother('/home')  
		"""


class Homepage:
	def GET(self):
		""" Show page """		
		return render.homepage()

class Video:


	def GET(self):
		""" Show page """
		return render.homepage()

class About:

	def GET(self):
		""" Show page """
		
		return render.about()

class Uploads:

	def GET(self):
		""" Show page """
		
		return render.uploads()

class Statistics:

	def GET(self):
		""" Show page """
		
		return render.statistics()

class Uploadvideo:

	def GET(self):
		""" Show page """		
		return render.uploadvideo()

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
		model.new_user(fn,ln,ph,eml,un,pwd)
		



if __name__ == "__main__":
   app.run()
