from django.shortcuts import render
from django.http import HttpResponse
import json
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, A,Q, Index

def index(request):
    return render(request,'main/index.html')

def result(request):
    i = request.POST.get('platforms')
    j = request.POST.get('crimes')
    global num
    global user_num

    try:
        if i=="twitter" and j=="sexcrime":
            index_name="kcelectra_twitter_sexual"
        elif i=="telegram" and j=="sexcrime":
            index_name="kcelectra_telegram_sexual"
        elif i=="discord" and j=="sexcrime":
            index_name="kcelectra_discord_sexual"
        elif i=="twitter" and j=="drug":
            index_name="kcelectra_twitter_drug"
        elif i=="telegram" and j=="drug":
            index_name="kcelectra_telegram_drug"
        elif i=="discord" and j=="drug":
            index_name="kcelectra_discord_drug"
        elif i=="twitter" and j=="gambling":
            index_name="kcelectra_twitter_gambling"
        elif i=="telegram" and j=="gambling":
            index_name="kcelectra_telegram_gambling"            
        elif i=="discord" and j=="gambling":
            index_name="kcelectra_discord_gambling"
        if i=="twitter":
            arr,num,new2_dict,user_num,high_user_num=search(i,index_name)
        elif i=="telegram" or i=="discord":
            arr,num,channel,user_num=search(i,index_name)
    except:
        arr=[]
        new2_dict={}
        channel={}
        num=0
        user_num=0
        high_user_num=0
    if i=="twitter":
        context={"arr":arr,"platform":i,"crime":j,"num":num,"new2_dict":new2_dict,"user_num":user_num,"high_user_num":high_user_num}
    elif i=="telegram" or i=="discord":
        context={"arr":arr,"platform":i,"crime":j,"num":num,"channel_dict":channel,"user_num":user_num}
    return HttpResponse(json.dumps(context), content_type="application/json")

def search(i,index_name):#channel 목록 보여주기
    tmp='http://elastic:deepolice@13.209.69.94:9200'
    es = Elasticsearch(tmp)

    if i=="twitter" or i=="telegram":
        resp = es.search(index=index_name,body={"size": 10000, "query":{"match_all": {}},"sort":{'date':{'order':'asc'}},},scroll='5m')
    elif i=="discord":
        resp = es.search(index=index_name,body={"size": 10000, "query":{"match_all": {}},"sort":{'timestamp':{'order':'asc'}},},scroll='5m')
    old_scroll_id=resp['_scroll_id']

    global outputs
    outputs=[]#outputs에 전체 es내용 다 저장
    if i=="twitter":
        for doc in resp['hits']['hits']:
            output={}
            r0=doc['_source']['user_id']
            r1=doc['_source']['korea_date']
            r2=doc['_source']['text']
            r3=doc['_source']['true']
            r4=doc['_source']['false']
            output['from_id_user_id']=r0
            output['date']=r1
            output['message']=r2
            output['true']=r3
            output['false']=r4
            outputs.append(output)
        while len(resp['hits']['hits']):
            resp=es.scroll(scroll_id=old_scroll_id,scroll='1s')
            for doc in resp['hits']['hits']:
                output={}
                r0=doc['_source']['user_id']
                r1=doc['_source']['korea_date']
                r2=doc['_source']['text']
                r3=doc['_source']['true']
                r4=doc['_source']['false']
                output['from_id_user_id']=r0
                output['date']=r1
                output['message']=r2
                output['true']=r3
                output['false']=r4
                outputs.append(output) 
        new2_dict,user_num,high_user_num=avg_twi(outputs)
        num=len(outputs)
        return outputs,num,new2_dict,user_num,high_user_num
    elif i=="telegram":
        for doc in resp['hits']['hits']:
            output={}
            r0=doc['_source']['from_id_user_id']
            r1=doc['_source']['korea_date']
            r2=doc['_source']['message']
            r3=doc['_source']['true']
            r4=doc['_source']['false']
            r5=doc['_source']['peer_id_channel_id']
            output['from_id_user_id']=r0
            output['date']=r1
            output['message']=r2
            output['true']=r3
            output['false']=r4
            output['peer_id_channel_id']=r5
        while len(resp['hits']['hits']):
            resp=es.scroll(scroll_id=old_scroll_id,scroll='1s')
            for doc in resp['hits']['hits']:
                output={}
                r0=doc['_source']['from_id_user_id']
                r1=doc['_source']['korea_date']
                r2=doc['_source']['message']
                r3=doc['_source']['true']
                r4=doc['_source']['false']
                r5=doc['_source']['peer_id_channel_id']
                output['from_id_user_id']=r0
                output['date']=r1
                output['message']=r2
                output['true']=r3
                output['false']=r4
                output['peer_id_channel_id']=r5
                outputs.append(output)
        channel,user_num=avg(outputs)
        num=len(outputs)
        return outputs,num,channel,user_num
    elif i=="discord":
        for doc in resp['hits']['hits']:
            output={}
            r0=doc['_source']['user_id']
            r1=doc['_source']['korea_date']
            r2=doc['_source']['content']
            r3=doc['_source']['true']
            r4=doc['_source']['false']
            r5=doc['_source']['channel_id']
            output['from_id_user_id']=r0
            output['date']=r1
            output['message']=r2
            output['true']=r3
            output['false']=r4
            output['peer_id_channel_id']=r5
            outputs.append(output)
        while len(resp['hits']['hits']):
            resp=es.scroll(scroll_id=old_scroll_id,scroll='1s')
            for doc in resp['hits']['hits']:
                output={}
                r0=doc['_source']['user_id']
                r1=doc['_source']['korea_date']
                r2=doc['_source']['content']
                r3=doc['_source']['true']
                r4=doc['_source']['false']
                r5=doc['_source']['channel_id']
                output['from_id_user_id']=r0
                output['date']=r1
                output['message']=r2
                output['true']=r3
                output['false']=r4
                output['peer_id_channel_id']=r5
                outputs.append(output)
        channel,user_num=avg(outputs)
        num=len(outputs)
        return outputs,num,channel,user_num

def avg_twi(outputs):
    #한 레코드당 {(채널 id) : [평균, 총 count]}
    global new2_dict
    new2_dict={}
    for i in outputs:
        i['new_key']=i['from_id_user_id']
        if new2_dict.get(i['new_key']):
            cnt=int(new2_dict.get(i['new_key'])[1])
            new_avg=(avg*cnt+float(i['true']))/(cnt+1)
            cnt+=1
            new_record={i['new_key']:[new_avg,cnt]}
            new2_dict.update(new_record)
        else:
            new_record={i['new_key']:[i['true'],1]}
            new2_dict.update(new_record)

    user_num=0
    high_user_num=0
    for i,j in new2_dict.items():
        user_num+=1
        if float(j[0])>=0.7:
            high_user_num+=1
    return new2_dict,user_num,high_user_num

def avg(outputs):
    #user_id,channel_id를 키값으로 저장
    for i in outputs:
        new_value=i['from_id_user_id'],i['peer_id_channel_id']
        i['new_key']=new_value
    
    #한 레코드당 {(유저 id, 채널 id) : [평균, 총 count]}
    global new_dict
    new_dict={}
    for i in outputs:
        if new_dict.get(i['new_key']):
            avg=float(new_dict.get(i['new_key'])[0])
            cnt=int(new_dict.get(i['new_key'])[1])
            new_avg=(avg*cnt+float(i['true']))/(cnt+1)
            cnt+=1
            new_record={i['new_key']:[new_avg,cnt]}
            new_dict.update(new_record)
        else:
            new_record={i['new_key']:[i['true'],1]}
            new_dict.update(new_record)
    #print(new_dict)

    #채널id중복제거
    channel=set()
    for i in range(len(outputs)):
        channel.add(outputs[i]['peer_id_channel_id'])
    channel=list(channel)
    #print(channel)

    #channel별로 users,high_risk_users 저장
    channel_dict={}
    for i in range(len(channel)):
        channel_dict[channel[i]]=[0,0]

    #channel_dict={[channel_id:[users,high_risk_users]]}
    #print("초기",channel_dict)
    user_num=0
    for i,j in new_dict.items():
        #print(i[1],j[0])
        for x in range(len(channel)):
            if int(i[1])==int(channel[x]):
                user_num+=1
                channel_dict[channel[x]][0]+=1
                #print(channel_dict)
                if float(j[0])>=0.7:
                    channel_dict[channel[x]][1]+=1
    return channel_dict,user_num

def users_info(request):
    pl = request.POST.get('platforms')
    cr = request.POST.get('crimes')
    global ch
    ch=request.POST.get('channel_id')

    #user_num,high_user_num 계산
    user_num=0
    high_user_num=0
    channel_dict={}
    global outputs
    channel_dict,t=avg(outputs)
    for i,j in channel_dict.items():
        if int(i)==int(ch):
            user_num=j[0]
            high_user_num=j[1]

    #msg_num 계산
    #{user_id:[risk,message_count]}
    msg_num=0
    global new_dict
    global user_dict
    user_dict={}
    for i,j in new_dict.items():
        if int(i[1])==int(ch):
            msg_num+=j[1]
            user_dict[i[0]]=[j[0],j[1]]

    context={"channel_id":ch,"platform":pl,"crime":cr,"num":num,"user_dict":user_dict,"user_num":user_num,"high_user_num":high_user_num,"msg_num":msg_num}
    return HttpResponse(json.dumps(context), content_type="application/json")

def messages_info(request):
    i=request.POST.get('platforms')
    id = request.POST.get('user_id')
    ch_id = request.POST.get('channel_id')
    arr2=[]
    user_msg_num=0
    text=""
    if i=="twitter":
        for x,y in new2_dict.items():
            if int(x)==int(id):
                user_msg_num=y[1]
        arr2,text=search2(id)
    elif i=="telegram" or i=="discord":
        #user_id 가져와서 msg 수 반환
        for x,y in user_dict.items():
            if int(x)==int(id):
                user_msg_num=y[1]
        arr2,text=search3(id)
    context={"arr":arr2,"platform":i,"text":text,"msg_num":user_msg_num,"user_id":id,"channel_id":ch_id}
    return HttpResponse(json.dumps(context), content_type="application/json")

def search2(id):
    global outputs
    results=[]
    text=""
    for i in outputs:
        if int(i['from_id_user_id'])==int(id):
            result={}
            result['from_id_user_id']=i['from_id_user_id']
            result['date']=i['date']
            result['message']=i['message']
            results.append(result)
            text+=(" "+i['message'])
    return results,text

def search3(id):#해당 user의 messages 보여주기
    global outputs
    global ch
    results=[]
    text=""
    for i in outputs:
        if int(i['from_id_user_id'])==int(id) and int(i['peer_id_channel_id'])==int(ch):
            result={}
            result['from_id_user_id']=i['from_id_user_id']
            result['date']=i['date']
            result['message']=i['message']
            results.append(result)
            text+=(" "+i['message'])
    return results,text