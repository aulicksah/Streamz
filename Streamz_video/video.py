import web
import model
import json

### Url mappings

urls = (
    '/', 'Index',
    '/del/(\d+)', 'Delete'
)


class Index:

    def GET(self):
        videos = model.get_video()
        video_list = []
        for video in videos:
          video_list.append(video) 
        return json.dumps(video_list)

    def POST(self):
        video = web.data()
        _id = model.new_video(json.loads(video)['name']['url']['desc']['channel']['uploaded']['uploader']['category']['tags'])
        return json.dumps({'id': _id})


class Delete:
    
    def POST(self, id):
        id = int(id)
        model.del_video(id)
        web.seeother('/')


app = web.application(urls, globals())

if __name__ == '__main__':
    app.run()
