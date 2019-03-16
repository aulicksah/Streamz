import web

db = web.database(dbn='sqlite', db='videos.db')

def get_video():
    return db.select('videos', order='id')

def upload_video(name,description,tags,video_location,countries,uploader,age):
	id=db.insert('user', firstname=firstname, lastname=lastname,email=email,username=username,pwd=pwd,phone=phone)
	params={'status':username,'username':username,'id':id}
	requests.post(url, data=json.dumps(params))
		

def del_video(id):
    db.delete('videos', where="id=$id", vars=locals())
