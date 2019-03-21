import web
import json 

db = web.database(dbn='sqlite', db='videos.db')

def get_videodesc(id):
	"""authdb = sqlite3.connect('videos.db')
	c= authdb.execute('select * from video where id=?',[id])
	row = c.fetchone()
	nm=row[1]
	url=row[2]
	params={'id':id, 'name':nm,'url':url}"""
	params = {'id': id} 
	return json.dumps(params)

def upload_video(name,videopath):
	id=db.insert('video', name=name, urlpath=videopath)
	params={'id':id}
	return json.dumps(params)
		

def del_video(id):
    db.delete('videos', where="id=$id", vars=locals())
