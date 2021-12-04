from django.shortcuts import render
from django.http import HttpResponse
import json
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, A,Q, Index
from elasticsearch_dsl.query import MultiMatch, Match

def index(request):
    return render(request,'main/index.html')

def result(request):
    i = request.POST.get('platforms')
    j = request.POST.get('crimes')
    arr=[]

    if not i or not j:
        num=0
    else:
        try:
            if i=="twitter" and j=="sexcrime":
                index_name="train_twitter_sexual"
            elif i=="telegram" and j=="sexcrime":
                index_name="telegram_sexcrime"
            elif i=="discord" and j=="sexcrime":
                index_name="discord_sexual"
            elif i=="twitter" and j=="drug":
                index_name="train_twitter_drug"
            elif i=="telegram" and j=="drug":
                index_name="koelectra_tele_raw"
            elif i=="discord" and j=="drug":
                index_name="discord_drug"
            elif i=="twitter" and j=="gambling":
                index_name="twitter_drug"
            elif i=="telegram" and j=="gambling":
                index_name="train_telegram_gambling"            
            elif i=="discord" and j=="gambling":
                index_name="discord_gambling"
            arr,num,user_num=search(i,index_name)
        except:
            num=0
    context={"arr":arr,"platform":i,"crime":j,"num":num,"user_num":user_num}
    return HttpResponse(json.dumps(context), content_type="application/json")
    #return render(request,'main/index.html',{"arr":arr,"platform":i,"crime":j,"num":num})

def search(i,index_name):#channel 목록 보여주기
    tmp='http://elastic:deepolice@13.209.69.94:9200'
    es = Elasticsearch(tmp)
    #timestamp_range = { "@timestamp": { "gte": d1, "lte": d2 } }
    #res = Search(index = index_name, doc_type = "_doc", using=es).filter("range", **timestamp_range)

    res = Search(index = index_name, doc_type = "_doc", using=es)
    res=res.extra(track_total_hits=True,size=1000)
    results=res.execute()
    num=results.hits.total['value']

    if i=="twitter":
        outputs=[]
        for i in range(100):
            output={}
            r=results.hits[i]['msg']
            output['msg']=r
            outputs.append(output)
    elif i=="telegram":
        output1=set()
        output2=set()
        j=0
        user_num=0
        while j<num:
            r1=results.hits[j]['peer_id_channel_id']
            output1.add(r1)
            j+=1
        output1=list(output1)
        outputs=[]
        for i in range(len(output1)):
            res2 = Search(index = index_name, doc_type = "_doc", using=es)
            res2=res2.extra(track_total_hits=True,size=1000)
            res2=res2.filter('term',peer_id_channel_id=int(output1[i]))
            results2=res2.execute()
            num2=results2.hits.total['value']
            k=0
            while k<num2:
                r2=results2.hits[k]['from_id_user_id']
                output2.add(r2)
                k+=1
            output2=list(output2)
            user_num=len(output2)
            output={}
            output['channel_id']=int(output1[i])
            output['user_num']=user_num
            outputs.append(output)
            print(outputs)
    elif i=="discord":
        outputs=[]
        for i in range(100):
            output={}
            r1=results.hits[i]['channel_id']
            output['channel_id']=r1
            outputs.append(output)
    return outputs,num,user_num

def users_info(request):
    i=request.POST.get('platform')
    j=request.POST.get('crimes')
    id = request.POST.get('channel_id')
    
    if i=="twitter" and j=="sexcrime":
        index_name="train_twitter_sexual"
    elif i=="telegram" and j=="sexcrime":
        index_name="telegram_sexcrime"
    elif i=="discord" and j=="sexcrime":
        index_name="discord_sexual"
    elif i=="twitter" and j=="drug":
        index_name="train_twitter_drug"
    elif i=="telegram" and j=="drug":
        index_name="koelectra_tele_raw"
    elif i=="discord" and j=="drug":
        index_name="discord_drug"
    elif i=="twitter" and j=="gambling":
        index_name="twitter_drug"
    elif i=="telegram" and j=="gambling":
        index_name="train_telegram_gambling"            
    elif i=="discord" and j=="gambling":
        index_name="discord_gambling"
    arr,num=search2(i,index_name,id)

    context={"arr":arr,"num":num,"platform":i}
    return HttpResponse(json.dumps(context), content_type="application/json")

def search2(i,index_name,id):#해당하는 channel에 존재하는 user목록보여주기
    tmp='http://elastic:deepolice@13.209.69.94:9200'
    es = Elasticsearch(tmp)
 
    res = Search(index = index_name, doc_type = "_doc", using=es)
    res=res.extra(track_total_hits=True,size=1000)
    res=res.filter('term',peer_id_channel_id=id)
    results=res.execute()
    num=results.hits.total['value']
    if i=="twitter":
        outputs=[]
        for i in range(100):
            output={}
            r=results.hits[i]['msg']
            output['msg']=r
            outputs.append(output)
    elif i=="telegram":
        outputs=set()
        j=0
        while j<num:
            r1=results.hits[j]['from_id_user_id']
            outputs.add(r1)
            j+=1
        outputs=list(outputs)
    elif i=="discord":
        outputs=[]
        for i in range(100):
            output={}
            r1=results.hits[i]['channel_id']
            r2=results.hits[i]['content']
            r3=results.hits[i]['username']
            r4=results.hits[i]['timestamp']
            output['channel_id']=r1
            output['content']=r2
            output['username']=r3
            output['timestamp']=r4
            outputs.append(output)
    return outputs,num


def messages_info(request):
    i=request.POST.get('platform')
    j=request.POST.get('crimes')
    id = request.POST.get('user_id')
    
    if i=="twitter" and j=="sexcrime":
        index_name="train_twitter_sexual"
    elif i=="telegram" and j=="sexcrime":
        index_name="telegram_sexcrime"
    elif i=="discord" and j=="sexcrime":
        index_name="discord_sexual"
    elif i=="twitter" and j=="drug":
        index_name="train_twitter_drug"
    elif i=="telegram" and j=="drug":
        index_name="koelectra_tele_raw"
    elif i=="discord" and j=="drug":
        index_name="discord_drug"
    elif i=="twitter" and j=="gambling":
        index_name="twitter_drug"
    elif i=="telegram" and j=="gambling":
        index_name="train_telegram_gambling"            
    elif i=="discord" and j=="gambling":
        index_name="discord_gambling"
    arr,num,text=search3(i,index_name,id)
    context={"arr":arr,"num":num,"platform":i,"text":text}
    return HttpResponse(json.dumps(context), content_type="application/json")

def search3(i,index_name,id):#해당 user의 messages 보여주기
    print(id)
    tmp='http://elastic:deepolice@13.209.69.94:9200'
    es = Elasticsearch(tmp)
 
    res = Search(index = index_name, doc_type = "_doc", using=es)
    res=res.extra(track_total_hits=True,size=1000)
    res=res.filter('term',from_id_user_id=id)
    res=res.sort({"date":{"order":"asc"}})
    results=res.execute()
    num=results.hits.total['value']
    if i=="twitter":
        outputs=[]
        for i in range(100):
            output={}
            r=results.hits[i]['msg']
            output['msg']=r
            outputs.append(output)
    elif i=="telegram":
        outputs=[]
        text=""
        j=0
        while j<num:
            output={}
            r0=results.hits[j]['from_id_user_id']
            r1=results.hits[j]['date']
            r2=results.hits[j]['message']
            r3=results.hits[j]['true']
            r4=results.hits[j]['false']
            output['from_id_user_id']=r0
            output['date']=r1
            output['message']=r2
            output['true']=r3
            output['false']=r4
            outputs.append(output)
            text+=r2
            j+=1
    elif i=="discord":
        outputs=[]
        for i in range(100):
            output={}
            r1=results.hits[i]['channel_id']
            r2=results.hits[i]['content']
            r3=results.hits[i]['username']
            r4=results.hits[i]['timestamp']
            output['channel_id']=r1
            output['content']=r2
            output['username']=r3
            output['timestamp']=r4
            outputs.append(output)
    return outputs,num,text