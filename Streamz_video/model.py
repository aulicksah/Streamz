import web

db = web.database(dbn='sqlite', db='videos.db')

def get_video():
    return db.select('videos', order='id')

def new_video(text1,text2,text3,text4,time,text5,text6,text7):
    return db.insert('videos',name=text1, url=text2, desc=text3, channel=text4, uploaded=time, uploader=text5, category=text6, tags=text7)

def del_video(id):
    db.delete('videos', where="id=$id", vars=locals())
