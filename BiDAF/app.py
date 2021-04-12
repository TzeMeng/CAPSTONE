import sys
import plotly
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import json
from datetime import date
from flask import jsonify
import requests
import os
import re
import time
import firebase
import firebase_admin
from firebase_admin import credentials, firestore,initialize_app
from bs4 import BeautifulSoup
from datetime import datetime
from flask import Flask, render_template, request, send_file
import matplotlib.pyplot as plt
import numpy as np
from eval import eval


from flask import Flask, render_template, request, jsonify
import json

cred = credentials.Certificate("key.json")
firebase_admin.initialize_app(cred)

db = firestore.client()




app = Flask(__name__)
docs = db.collection('Final_squad2').get()


context_para = []
titles = []

for doc in docs:
    titles.append(doc.get('title'))


title_context = {}

for title in titles:
    for doc in docs:
        topic = doc.get('title')
        if title!=topic:
            continue
        else:
            context_1 = []
            contexts = doc.get('paragraphs')
            for context in contexts:
                context_1.append(context.get('context'))
            title_context[title] = context_1


@app.route('/_update_dropdown')
def update_dropdown():

    # the value of the first dropdown (selected by the user)
    selected_class = request.args.get('selected_class', type=str)

    # get values for the second dropdown
    updated_values = title_context[selected_class]

    # create the value sin the dropdown as a html string
    html_string_selected = ''
    for entry in updated_values:
        html_string_selected += '<option value="{}">{}</option>'.format(entry, ' '.join(entry.split()[:20]))

    return jsonify(html_string_selected=html_string_selected)



@app.route('/_process_data')
def process_data():
    selected_entry = request.args.get('selected_entry', type=str)

    # process the two selected values here and return the response; here we just create a dummy string

    return jsonify(random_text="Context: {}".format(selected_entry))


@app.route('/')
def index():

    """
    Initialize the dropdown menues
    """

    class_entry_relations = title_context


    default_classes = sorted(class_entry_relations.keys())
    default_values = class_entry_relations[default_classes[0]]
    return render_template('index.html',
                           all_classes=default_classes,
                           all_entries=default_values,
                           len = len(default_values)

                           )




@app.route("/test", methods = ['GET','POST'])
def test():
    select = request.form.get('val')
    return (str(select))

#push the feedback answers to firebase
def push_feedback(data):
    if len(data['feedback'])!=0:
    

        user_ref=db.collection('Future_data')
        fb=user_ref.document("future").get().to_dict()
        cont=data['cont']
        q=data['query']
        ans=data['feedback']
        
        if  cont in fb:
            idx=int(len(fb[cont]))+1
            for i,j in zip(q,ans):
                fb[cont][str(idx)]={'answers':j, "question":i}
            
                idx+=1
            
        else:
            idx=0
            for i,j in zip(q,ans):
                fb[cont]={str(idx):{'answers':j, "question":i}}
                idx+=1
    
        user_ref.document(u'future').set({u"{}".format(cont) :fb[cont]}, merge= True)
            





#get the number of correct or wrong answers from feedback system
@app.route('/get_post', methods = ['POST'])
def get_accuracy():
    if request.method=='POST':
        jsdata = request.get_json()
        
        push_feedback(jsdata[1])
        
        today =date.today().isoformat()
        
        new_correct=jsdata[0]['corr']
        new_total=jsdata[0]['corr']+jsdata[0]['wr']
        topic=jsdata[0]['topic']
        squad_update=db.collection('Final_squad2')
        squad=db.collection('Final_squad2').get()
        

        for docs in squad:
           
            if docs.get('title')==topic:
                current_correct=docs.get('Query_accuracy')['correct']+new_correct
                current_total=docs.get('Query_accuracy')['total']+new_total
                update={
                        "correct":current_correct,
                        "total":current_total,}
                
        
                squad_update.document(u'{}'.format(docs.id)).set({u'Query_accuracy':update}, merge= True)
        
        user_ref=db.collection('visualisation_data')
        accuracy=user_ref.document("data").get().to_dict()['accuracy']
        if today in accuracy:
            current_correct=accuracy[today]['correct']+new_correct
            current_total=accuracy[today]['total']+new_total
            update={
                today:{
                    "correct":current_correct,
                    "total":current_total,
                }
            }

            
            
            user_ref.document(u'data').set({u'accuracy':update}, merge= True)

        else:
            update={
                today:{
                    "correct":new_correct,
                    "total":new_total,
                }
            }

            user_ref.document(u'data').set({u'accuracy':update}, merge= True)

            
        
    
    return jsonify(status="success",data=jsdata)


@app.route('/dashboard')
def dashboard():

    #For first 2 plots regarding the context and query length
    user_ref=db.collection('visualisation_data').get()
    cont=user_ref[0].get('context_len')
    q=user_ref[0].get('query_len')
    post=[]
    query=[]
    time_q=[]
    time_c=[]
    for k,j in cont.items():
        post.append(int(k))
        time_c.append(np.mean(j))
    for k,i in q.items():
        query.append(int(k))
        time_q.append(np.mean(i))

  
    
    data1=pd.DataFrame({"q":query, "time":time_q})
    data2=pd.DataFrame({"cont":post,"time":time_c})
    time_c = data2.sort_values(by=["cont"])['time'].values.tolist()
    post=data2.sort_values(by=["cont"])['cont'].values.tolist()
    values1 = data1.sort_values(by=["q"])['q'].values.tolist()
    time_q = data1.sort_values(by=["q"])['time'].values.tolist()
    
    #For the 2 plots regarding the accuracy of the answers 
    acc=user_ref[0].get('accuracy')
    
    accuracy=[]
   
    days=[]
    total=[]
    right=[]
    for i in acc.keys():
        total.append(acc[i]['total'])
        right.append(acc[i]['correct'])
        pct=acc[i]['correct']/acc[i]['total']
        accuracy.append(pct)
        days.append(i[5:])
    a=pd.DataFrame({'days':days, 'accuracy':accuracy})
    days=a.sort_values(by=['days'])['days'].tolist()
    accuracy=a.sort_values(by=['days'])['accuracy'].tolist()
    
   

    
    total_pct=round(sum(right)/sum(total),4)
    wrong=round(1-total_pct,4)

    pie=[total_pct,wrong]
     
    #For the stacked barchart at the bottom
    topics=[]
    query_correct=[]
    query_wrong=[]
    total=[]

    
    squad=db.collection('Final_squad2').get()
        
    
    for docs in squad:
        topics.append(docs.get('title'))
        corr=docs.get('Query_accuracy')['correct']
        query_correct.append(corr)
        query_wrong.append(docs.get('Query_accuracy')['total']-corr)
        t=docs.get('Query_accuracy')['total']
        total.append(t)
    
    data=pd.DataFrame({"topics": topics , 'q_corr':query_correct, 'q_wrong':query_wrong, 'total':total})
   
    query_correct=data.sort_values(by=["q_corr"],ascending=False)['q_corr'].values.tolist()
    query_wrong=data.sort_values(by=["q_corr"],ascending=False)['q_wrong'].values.tolist()
    topics=data.sort_values(by=["q_corr"],ascending=False)['topics'].values.tolist()
            
            


    return render_template('dashboard.html',values_c=post, label_c=time_c,label_q=time_q,values_q=values1,accuracy=accuracy, pie=pie,days=days, topics=topics, q_corr=query_correct, q_wr=query_wrong)
  


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

#update number of times the topic is being chosen
def update_chosen(title):
    user_ref=db.collection('Final_squad2')
    
    documents=db.collection('Final_squad2').get()
   
    for docs in documents:
  
        if docs.get('title')==title:
            
         
            chosen=docs.get('Chosen')+1
        
            user_ref.document(u'{}'.format(docs.id)).set({u'Chosen':chosen}, merge= True)



#update visualisation data in firebase
def update_length_data(entry,ques,t):
    length_ques=str(sum([len(i.split()) for i in ques.split(',') ]))
    length_entry=str(len(entry.split()))
    user_ref=db.collection('visualisation_data')
    cont=db.collection('visualisation_data').get()[0].get('context_len')
    time=sum(t)
 
    if length_entry in cont.keys():
        cont[length_entry].append(time)
        user_ref.document(u'data').set({u'context_len':cont}, merge= True)
    else:
        x=[]
        x.append(time)
        cont[length_entry]=x
        user_ref.document(u'data').set({u'context_len':cont}, merge= True)
   

    query=db.collection('visualisation_data').get()[0].get('query_len')
    if length_ques in query.keys():
        query[length_ques].append(time)
        user_ref.document(u'data').set({u'query_len':query}, merge= True)
    else:
        x=[]
        x.append(time)
        query[length_ques]=x
        user_ref.document(u'data').set({u'query_len':query}, merge= True)
   
def update_sample():
    user_ref=db.collection('Final_squad2')
    documents=db.collection('Final_squad2').get()
    x=[2,6,4,10]
    for docs in range(len(documents)):
        idx=documents[docs].id
        if int(idx) in x:
            user_ref.document(u'{}'.format(documents[docs].id)).set({u'Query_accuracy':{"correct":12, "total": 14}}, merge= True)
    


#data for about page bar-chart
@app.route('/user_dashboard')
def user_dashboard():
    cloud=[]
    count=[]
    
    documents=db.collection('Final_squad2').get()
    for docs in documents:
        cloud.append(docs.get('title'))
        count.append(docs.get('Chosen'))
    data=pd.DataFrame({"cloud":cloud, "count":count})
    title=data.sort_values(by=["count"],ascending=False)[:10]

    return render_template('user_dashboard.html',cloud=title['cloud'].values.tolist(), num=title['count'].values.tolist())

@app.route("/_evaluate")
def evaluate():
    answer = {"results": []}
    selected_entry = request.args.get('selected_entry', type=str)
    question = request.args.get('question', type=str)
    title=request.args.get('selected_class', type=str)

    update_chosen(title)

    time=[]
    questions = question.split(",")
    for q in questions:
        ans = eval(selected_entry, q)
        time.append(ans[1])
        answer["results"].append({"ques":q, "ans":ans[0]})

    update_length_data(selected_entry,question,time)
    return answer




#runs the application in debug mode
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 4000))
   
    app.run(debug=True)