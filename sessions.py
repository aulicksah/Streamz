import web
urls = ("/", "hello")

app = web.application(urls, globals())

if web.config.get('_session') is None:
    session = web.session.Session(app, web.session.DiskStore('sessions'), {'user':'Aulick'})
    web.config._session = session
else:
    session = web.config._session

class hello:
   def GET(self):
       print 'session', session
       session.user='arnenupharsah'
       return 'Hello, %s!' % session.user

if __name__ == "__main__":
   app.run()