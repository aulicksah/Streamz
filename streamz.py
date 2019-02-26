""" Basic todo list using webpy 0.3 """
import web
import json
from web import form

### Url mappings

urls = (
	'/', 'Index',
	'/home', 'Homepage',
 
)


### Templates
render = web.template.render('templates', base='base')


class Index:

	login = form.Form(
	form.Textbox('loginemail'),
	form.Password('loginpassword'),
	form.Button('loginbtn'),
	)

	register = form.Form(
	form.Textbox('firstname'),
	form.Textbox('lastname'),
	form.Textbox('phoneno'),
	form.Textbox('email'),
	form.Password('registerpassword'),
	form.Button('registerbtn'),
	)

	def GET(self):
		""" Show page """
		
		login = self.login()
		register = self.register()
		return render.index(login, register)

	def POST(self):
		""" Add new entry 
		form = self.form()
		if not form.validates():
		    todos = model.get_todos()
		    return render.index(todos, form)
		model.new_todo(form.d.title)
		raise web.seeother('/')

		"""

class Homepage:

	def GET(self):
		""" Show page """
		
		return render.homepage()

app = web.application(urls, globals())

if __name__ == '__main__':
    app.run()
