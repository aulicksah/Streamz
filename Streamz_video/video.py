import web
import model
import json
import requests
### Url mappings

urls = (
	'/upload','Upload',
)




urls = (
    '/', 'Index',
    '/videos/(.+)', 'Videos',
    '/upload', 'Upload',
    '/play/(.+)','Play',
)


### Templates
render = web.template.render('templates', base='base')

class Play:
    def GET(self,videoid):
        return render.play(videoid) 

class Videos:
    def GET(self,videoid):
        # GET THE ID OF THE VIDEO
	return open('videos/video.mp4',"rb").read()

class Upload:
    def POST(self):
        web.header('Access-Control-Allow-Origin','*')
        web.header('Access-Control-Allow-Credentials', 'true')
        x = web.input()
        print x
        """filedir = 'static/video'
        if 'myfile' in x: 
            filepath=x.myfile.filename 
            filename=filepath.split('/')[-1] 
            fout = open(filedir +'/'+ filename,'w')
            fout.write(x.myfile.file.read()) 
            fout.close() 
	_id = model.upload_video(json.loads(filedir +'/'+ filename)['url'])
	return json.dumps({'id': _id})"""
	



app = web.application(urls, globals())

if __name__ == '__main__':
    app.run()
