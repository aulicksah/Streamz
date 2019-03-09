import requests
import json


url1 = 'http://0.0.0.0:8080/getuser'


def new_user(firstname,lastname,phone,email,password):
    params = {'firstname': firstname,'lastname':lastname,'phone':phone,'email':email,'password':password} 
    #requests.post(url1, data=json.dumps(params))
    return json.dumps(params)

def check_user(username,password):
    params = {'username': username,'password':password} 
    #requests.post(url1, data=json.dumps(params))
    return json.dumps(params)

def send_search(search_text):
    params = {'search_text':search_text} 
    #requests.post(url1, data=json.dumps(params))
    return json.dumps(params)

def send_comment(search_text):
    params = {'comment_text':search_text} 
    #requests.post(url1, data=json.dumps(params))
    return json.dumps(params)

def upload_video(name):
    params = {'name':name} 
    #requests.post(url1, data=json.dumps(params))
    return json.dumps(params)

def search_upload_video(path):
    params = {'name':name,'description':description,'tags':tags} 
    #requests.post(url1, data=json.dumps(params))
    return json.dumps(params)
    
    