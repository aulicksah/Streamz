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
render1 = web.template.render('templates', base='topnav')

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
		""" Show page """
		
		login = self.login()
		return render.index(login)



	def POST(self):
		login = self.login()
		if not login.validates():            
			return "Unsuccessful"

		un=login.d.email
		pwd=login.d.password
		s = model.check_user(un,pwd)
		return s

		



class Homepage:



	def GET(self):
		""" Show page """		
		return render.homepage()

class Video:


	def GET(self):
		""" Show page """
		return render.video()

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
		pwd=register.d.password
		s = model.new_user(fn,ln,ph,eml,pwd)
		return s


app = web.application(urls, globals())

if __name__ == '__main__':
    app.run()
