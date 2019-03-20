import requests
import json


def new_user(firstname,lastname,phone,email,username,password):
    params = {'firstname': firstname,'lastname':lastname,'phone':phone,'email':email,'username':username,'password':password} 
    p=requests.post('http://0.0.0.0:9090/register', data=json.dumps(params))
    return p.json()

def check_user(username,password):
    params = {'username': username,'password':password} 
    p=requests.post('http://0.0.0.0:9090/login', data=json.dumps(params))
    return p.json()

def get_profile(username):
    params = {'username':username} 
    p=requests.post('http://0.0.0.0:9090/profile', data=json.dumps(params))
    return p.json()
     
def update_profile(firstname,lastname,username,phone,email,category,country,dob):
    params = {'firstname':firstname,'lastname':lastname,'username':username,'phone':phone,'email':email,'category':category,'country':country,'dob':dob} 
    p=requests.post('http://0.0.0.0:9090/updateprofile', data=json.dumps(params))
    return p
    #return json.dumps(params)

"""--------------------------------------Search---------------------------------"""

def send_search(search_text):
    params = {'keyword': search_text} 
    p=requests.post('http://0.0.0.0:7070/search', data=json.dumps(params))
    return p.json()
    #return json.dumps(params)

def search_upload_video(path):
    params = {'name':name,'description':description,'tags':tags} 
    #requests.post(url1, data=json.dumps(params))
    return json.dumps(params)
"""--------------------------------------Comments---------------------------------"""

def send_comment(search_text):
    params = {'comment_text':search_text} 
    #requests.post(url1, data=json.dumps(params))
    return json.dumps(params)

"""--------------------------------------Video Upload---------------------------------"""
def upload_video(name,file):
    params = {'name': name,'file':file} 
    p=requests.post('http://0.0.0.0:5050/upload', files=file)
    #p=requests.post('http://0.0.0.0:5050/upload', data=json.dumps(params))
    return p.json()

def upload_video_info(name,description,tags,video_location,countries,category,uploader,age):
    params = {'video_name':name,'description':description,'tags':tags,'video_location':'http://0.0.0.0:5050/static/video/'+location,'category':category,'countries':countries,'uploader':uploader,'age':age} 
    #p=requests.post('http://0.0.0.0:7070/search', data=json.dumps(params))
    return p.json()    
    #return json.dumps(params)   