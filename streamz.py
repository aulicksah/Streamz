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
	'/getuser','Getuser'
 
)


### Templates
render = web.template.render('templates', base='base')


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

	searchform = form.Form(
	form.Textbox('searchtext'),
	form.Button('Search'),
	)

	def GET(self):
		""" Show page """
		searchform = self.searchform()
		return render.video(searchform)

	def POST(self):
		searchform = self.searchform()
		if not searchform.validates():            
			return "Unsuccessful"
		txt=searchform.d.searchtext
		s = model.send_search(txt)
		return s
	


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

class Getuser:

	def POST(self):
		""" Show page """
		user = web.data()
		return user


app = web.application(urls, globals())

if __name__ == '__main__':
    app.run()
