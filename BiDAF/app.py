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

# config = {
#     "apiKey": "AIzaSyACjmO00NqYUJU_bdiddjgXT-y7ltLAiFE",
#     "authDomain": "capstone-dsta.firebaseapp.com",
#     "databaseURL": "https://capstone-dsta-default-rtdb.firebaseio.com",
#     "projectId": "capstone-dsta",
#     "storageBucket": "capstone-dsta.appspot.com",
#     "messagingSenderId": "70356572000",
#     "appId": "1:70356572000:web:e2874f6c7c9b9ed7817005",
#     "measurementId": "G-3T27VJP341"
# }
#
# firebase = pyrebase.initialize_app(config)
# db = firebase.database()


# db.child("names").push({"name":"tuna"})
# db.child("names").child("name").update({"name":"swordfish"})
# users = db.child("names").child("name").get()
# print(users.val())
# users = db.child("names").child("name").get()
# print(users.key())
# db.child("names").child("name").remove()
# db.child("names").remove()



app = Flask(__name__)
docs = db.collection('Final_squad2').get()

# for doc in docs:
#     print(doc)

context_para = []
titles = []

for doc in docs:
    titles.append(doc.get('title'))
# print(title)

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
# print(title_context['Normans'])

# @app.route('/', methods=['GET'])
# def dropdown():
#     a = title_context
#     return render_template('index.html', a = title_context)

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
    #selected_class = request.args.get('selected_class', type=str)
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
    ##for testing the outputs in index.html after getting answers
    # d1={1:{"ques":'what is my name?', "ans": 'i am xingying'},
    #    2:{"ques":'what is my name?', "ans": ' i am hazel'},
    #    3:{"ques":'what is my name?', "ans": ' i am zhihan'},
    #    4:{"ques":'what is my name?', "ans": ' i am tze meng'}
    # }
    #D=['APPLE','PEAR']

    # print(answer,"888888")

    return render_template('index.html',
                           all_classes=default_classes,
                           all_entries=default_values,
                           len = len(default_values)

                           )


# @app.route('/index.html')
# def transfer(x):
#     # df = x
#
#     """
#     Initialize the dropdown menues
#     """
#     ##for testing the outputs in index.html after getting answers
#     d1={1:{"ques":'what is my name?', "ans": 'i am xingying'},
#        2:{"ques":'what is my name?', "ans": ' i am hazel'},
#        3:{"ques":'what is my name?', "ans": ' i am zhihan'},
#        4:{"ques":'what is my name?', "ans": ' i am tze meng'}
#     }
#     print(x,"99999#####")
#     #D=['APPLE','PEAR']
#
#     return render_template('index.html', answers=d1)

@app.route("/test", methods = ['GET','POST'])
def test():
    select = request.form.get('val')
    return (str(select))

#get the number of correct or wrong answers from feedback system
@app.route('/get_post', methods = ['POST'])
def get_accuracy():
    if request.method=='POST':
        jsdata = request.get_json()
        user_ref=db.collection('visualisation_data')
        accuracy=user_ref.document("data").get().to_dict()['accuracy']
        #date=datetime.date(datetime.now())
        
        today =date.today().isoformat()
        
        new_correct=jsdata[0]['corr']
        new_total=jsdata[0]['corr']+jsdata[0]['wr']
        
        if today in accuracy:
            current_correct=accuracy[today]['correct']+new_correct
            current_total=accuracy[today]['total']+new_total
            update={
                today:{
                    "correct":current_correct,
                    "total":current_total,
                }
            }

            
            #documents=db.collection('data_visualisation').get()
            user_ref.document(u'data').set({u'accuracy':update}, merge= True)

        else:
            update={
                today:{
                    "correct":new_correct,
                    "total":new_total,
                }
            }

            user_ref.document(u'data').set({u'accuracy':update}, merge= True)

            
            # print(jsdata[0],"888")
            # print(datetime.date(datetime.now()))
    
    return jsonify(status="success",data=jsdata)

@app.route('/dashboard')
def dashboard():
    user_ref=db.collection('visualisation_data').get()
    post=[]
    cont=user_ref[0].get('Context_length')
    q=user_ref[0].get('query_length')
    t=user_ref[0].get('time')
    query=[]
    time=[]
    for doc in range(len(cont)):
        post.append(cont[doc])
        query.append(q[doc])
        time.append(t[doc])
    labels = time
  
    values1 = query
    #print(values,"55555555%%%%")

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


        days.append(i)
    days.sort()

  
    total_pct=round(sum(right)/sum(total),2)
    wrong=round(1-total_pct,2)
    pie=[total_pct,wrong]
    

    return render_template('dashboard.html',values=post, label=labels,values1=values1,accuracy=accuracy, pie=pie,days=days)
  

# def update_sample():
#     user_ref=db.collection('Final_squad2')
#     documents=db.collection('Final_squad2').get()
#     for docs in documents:
       
#         user_ref.document(u'{}'.format(docs.id)).set({u'Chosen':1}, merge= True)

#     user_ref=db.collection('visualisation_data')

#     today='2021-04-03'
#     today2='2021-04-04'
#     today3='2021-04-05'
#     today4='2021-04-06'
#     update={
#                 today:{
#                     "correct":9,
#                     "total":10,
#                 },
#                 today2:{
#                     "correct":7,
#                     "total":10,
#                 },
#                 today3:{
#                     "correct":10,
#                     "total":10,
#                 },
#                 today4:{
#                     "correct":8,
#                     "total":10,
#                 }

#             }

#     user_ref.document(u'data').set({u'accuracy':update}, merge= True)
    # user_ref=db.collection('squad2.0')
    # documents=db.collection('squad2.0').get()
    # for docs in documents:
       
    #     user_ref.document(u'{}'.format(docs.id)).set({u'Chosen':1}, merge= True)
    
    
def delete():
    user_ref=db.collection('visualisation_data')
    documents=db.collection('visualisation_data').get()
    for docs in documents:
        if(docs.id!='data'):
            print(docs.id)
            user_ref.document(u'{}'.format(docs.id)).delete()


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

def update_chosen(title):
    user_ref=db.collection('Final_squad2')
    
    documents=db.collection('Final_squad2').get()
    for docs in documents:
  
        if docs.get('title')==title:
         
            chosen=docs.get('Chosen')+1
            user_ref.document(u'{}'.format(docs.id)).set({u'Chosen':chosen}, merge= True)

# def update_future_data(selected_entry,question, )

def update_length_data(entry,ques,time):
    length_ques=str(sum([len(i.split()) for i in ques.split(',') ]))
    length_entry=str(len(entry.split()))
    user_ref=db.collection('visualisation_data')
    cont=db.collection('visualisation_data').get()[0].get('context_len')
    if length_entry in cont.keys():
        print(cont,length_entry,"999******")
        cont[length_entry].append(time)
        #cont[length_entry]=values
        print(cont,"7777777")
        
        user_ref.document(u'data').set({u'context_len':cont}, merge= True)
    else:
        x=[]
        x.append(time)
        cont[length_entry]=x
        user_ref.document(u'data').set({u'context_len':cont}, merge= True)
   

    query=db.collection('visualisation_data').get()[0].get('query_len')
    if length_ques in query.keys():
        query[length_ques].append(time)
        #query[length_ques]=values
        
        user_ref.document(u'data').set({u'query_len':query}, merge= True)
    else:
        x=[]
        x.append(time)
        
        query[length_ques]=x
        print(x,"9999999999999999")
        user_ref.document(u'data').set({u'query_len':query}, merge= True)
   


@app.route("/_evaluate")
def evaluate():
    answer = {"results": []}
    selected_entry = request.args.get('selected_entry', type=str)
    question = request.args.get('question', type=str)
    title=request.args.get('selected_class', type=str)
    update_chosen(title)

    #time=18
    #update_length_data(selected_entry,question,time)
    questions = question.split(",")
    # count = 1
    for q in questions:
        ans = eval(selected_entry, q)
        answer["results"].append({"ques":q, "ans":ans})
    print(answer)
    #     count = count+1
        # print(ans)
    # print(answer)
    # transfer(answer)
        # print(ans)

    # return (selected_entry)
    return jsonify(answer=answer)
    # return render_template('index.html', answer=answer)
    # return jsonify(answer=answer)
    # return answering(selected_entry, question)

@app.route("/answer/", methods=['GET','POST'])
def answering(selected_entry, question):
    answer ={}
    questions = question.split(",")
    count = 1
    for q in questions:
        ans = eval(selected_entry, q)
        answer[count] = {"ques": q, "ans": ans}
        count = count + 1
    print(answer)
    # return answer
    return render_template('index.html', answer=answer)



#runs the application in debug mode
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 4000))

    #update_sample()
    #app.run(host='0.0.0.0', port=port)
    app.run(debug=True)