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
        x = web.input()
        """filedir = './videos' # change this to the directory you want to store the file in.
       	if 'myfile' in x: # to check if the file-object is created
       	    filepath=x.myfile.filename.replace('\\','/') # replaces the windows-style slashes with linux ones.
       	    filename=filepath.split('/')[-1] # splits the and chooses the last part (the filename with extension)
       	    fout = open(filedir +'/'+ filename,'w') # creates the file where the uploaded file should be stored
       	    fout.write(x.myfile.file.read()) # writes the uploaded file to the newly created file.
       	    fout.close() # closes the file, upload complete."""
        return x



app = web.application(urls, globals())

if __name__ == '__main__':
    app.run()
