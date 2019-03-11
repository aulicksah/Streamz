import requests
import json


url = 'http://0.0.0.0:9090/register'
url1 = 'http://0.0.0.0:9090/login'

def new_user(firstname,lastname,phone,email,username,password):
    params = {'firstname': firstname,'lastname':lastname,'phone':phone,'email':email,'username':username,'password':password} 
    requests.post(url, data=json.dumps(params))
    #return json.dumps(params)

def check_user(username,password):
    params = {'username': username,'password':password} 
    requests.post(url1, data=json.dumps(params))
    #return json.dumps(params)

"""--------------------------------------Search---------------------------------"""

def send_search(search_text):
    params = {'search_text':search_text} 
    #requests.post(url1, data=json.dumps(params))
    return json.dumps(params)

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
def upload_video(name,description,tags,location):
    params = {'video_name':name,'description':description,'tags':tags,'location':'http://0.0.0.0:5050/static/video/'+location} 
    #requests.post(url1, data=json.dumps(params))
    return json.dumps(params)   