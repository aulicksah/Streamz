#import libraries
import web
import json
import requests

# Import Elasticsearch package 
from elasticsearch import Elasticsearch 


# function to upload details to server
#details consists of id,channel,uploader,category,title,description and tags

def send_details(details):
  ids=json.loads(details)['id']
  # Connect to the elastic cluster
  es=Elasticsearch([{'host':'localhost','port':9200}])
  res = es.index(index='streams2',doc_type='video',body=details,id=ids)  #index_name=streams1, doc_type=videos
  return res


# function to search by keywords
#search based on category,channel,uploader,title,tags
def send_search(txt,age,keyword):
  txt=str(txt)
  print(txt)
  videos=[]
  es=Elasticsearch([{'host':'localhost','port':9200}])
  res= es.search(index='streams2',body={"query" : {
                "bool" : {
                    "should" : [
                    { "match" : {"channel" : txt}},
                    { "match" : {"category" : txt} },
                    {"match":{ "uploader" : txt }},
                    {"match": {"tags": txt}},
                    {"match": {"title":{"query":txt,"analyzer": "english"}}},
                    
                     ]
                    }
                    }
                    })
  for hit in res['hits']['hits']:
    videos.append(hit['_source']['id'])
  ids = {'id': videos}
  return json.dumps(ids)

  
 # function to delete from server 
def delete(index):
  #print index
  es=Elasticsearch([{'host':'localhost','port':9200}])
  res = es.delete(index='streams2', doc_type='video', id=index)
  return res	
    
def update_details(details):
  ids=json.loads(details)['id']
  #Connect to the elastic cluster
  es=Elasticsearch([{'host':'localhost','port':9200}])
  res=es.update(index='streams2',doc_type='video',id=ids,body={"doc":{details}})
  return details

def update_likes(ids,likes,dislikes,score):

  es=Elasticsearch([{'host':'localhost','port':9200}])
  res=es.update(index='streams2',doc_type='video',id=ids,body={"doc": {'likes':likes,'dislikes':dislikes,'score':score}})
  params={'status':"Updated"}
  return json.dumps(params)



def trending(age,country):
  video_id=[]
  channel_name=[]
  es=Elasticsearch([{'host':'localhost','port':9200}])

  res= es.search(index='streams2',body={
  
    "query": {
    
    "bool": {
                    "must":[

                    {"match": {"countries":country}},
                    
                    { "range": {
                        "age": {
                "lte": age
            }
        }
        }],
        }
        },
    
    
                    "sort" : [
      {"score" : {"order" : "desc", "mode" : "avg"}},]
                    
                    }
                    

    )

  for hit in res['hits']['hits']:
    video_id.append(hit['_source']['id'])
  
  res1= es.search(index='streams2',body={
  
    "query": {
    
    "bool": {
                    "must":[

                    {"match": {"countries":country}},
                    
                    { "range": {
                        "age": {
                "lte": age
            }
        }
        }],
        }
        },
    
    
                    "sort" : [
      {"subcount" : {"order" : "desc", "mode" : "avg"}},]
                    }
                    
                    

    )
  for hit1 in res1['hits']['hits']:
    channel_name.append(hit1['_source']['uploader'])

  video_ids={'trend_video': video_id,'trend_channel':channel_name}
  return video_ids  







def sort_category(category,age,country):
  category=str(category) 
  videos=[]
  es=Elasticsearch([{'host':'localhost','port':9200}])
  res= es.search(index='streams2',body={

   "query": {
    
    "bool": {
                    "must":[

                    {"match": {"countries":country}},
                    {"match":{"category":category}},
                    
                    { "range": {
                        "age": {
                "lte": age
            }
        }
        }],
        }
        }
   })
  for hit in res['hits']['hits']:
    videos.append(hit['_source']['id'])
  ids = {'id': videos}
  return json.dumps(ids)

def recommendation(ids,age,country):

  es=Elasticsearch([{'host':'localhost','port':9200}])
  res = es.get(index='streams2',doc_type='video',id=ids)
  category=res['_source']['category']
  uploader=res['_source']['uploader']
  recom=[]

  res1= es.search(index='streams2',body={

  "query": {
    
    "bool": {
                    "must":[

                    {"match": {"countries":country}},
                    
                    { "range": {
                        "age": {
                "lte": age
            }
        }
        },
    
                    {
                    "bool":

                    {
                    "should" : [
                    { "match" : {"category" : category} },
                    {"match":{ "uploader" : uploader }},
                    
                    ]

                    }
                    }
                    ]
                    }
                    }
                    }
                   
                  
                    )
  for hit in res1['hits']['hits']:
    recom.append(hit['_source']['id'])                    
  ids = {'recom_id':recom}
  return json.dumps(ids)