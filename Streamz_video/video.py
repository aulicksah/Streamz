import web
import model
import json
import requests

urls = ('/getvideodesc', 'GetVideoDesc',
        '/upload', 'Upload',
)

	

class GetVideoDesc:
    
        def POST(self):
                data=web.data()
                id=json.loads(data)['vid']
                s=model.get_videodesc(id)
                return s

class Upload:
    def POST(self):
        web.header('Access-Control-Allow-Origin','*')
        web.header('Access-Control-Allow-Credentials', 'true')
        data = web.input()
        filename=data['name']
        fout = open('static/videos' +'/'+ filename,'w')
        fout.write(data['file']) 
        fout.close() 
        res = model.upload_video(filename,'http://0.0.0.0:5050/upload' +'/'+ filename)
        return res


app = web.application(urls, globals())

if __name__ == '__main__':
        app.run()
