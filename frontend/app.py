import sys
import plotly
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import json

from flask import jsonify
import requests
import os
import re
import time
import firebase
import firebase_admin
from firebase_admin import credentials, firestore,initialize_app
from bs4 import BeautifulSoup
from gensim.summarization import summarize
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import datetime
from flask import Flask, render_template, request, send_file
from flask_mail import Mail, Message
import matplotlib.pyplot as plt

cred=credentials.Certificate("key.json")
default_app=initialize_app(cred)
db=firestore.client()

app = Flask(__name__)
docs = db.collection('squad2.0').get()

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
                context_1.append([context.get('context')])
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
        html_string_selected += '<option value="{}">{}</option>'.format(entry, ' '.join(entry[0].split()[:20]))

    return jsonify(html_string_selected=html_string_selected)

@app.route('/index.html')


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
    d1={1:{"ques":'what is my name?', "ans": 'i am xingying'},
       2:{"ques":'what is my name?', "ans": ' i am hazel'},
       3:{"ques":'what is my name?', "ans": ' i am zhihan'},
       4:{"ques":'what is my name?', "ans": ' i am tze meng'}
    }
    #D=['APPLE','PEAR']

    return render_template('index.html',
                           all_classes=default_classes,
                           all_entries=default_values,
                           len = len(default_values),answers=d1)

@app.route("/test", methods = ['GET','POST'])
def test():
    select = request.form.get('val')
    return (str(select))

#get the number of correct or wrong answers from feedback system
@app.route('/get_post', methods = ['POST'])
def get_accuracy():
    jsdata = request.get_json()
    print(jsdata[0]['corr'],"888")
    
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
    values = post
    values1 = query

    acc=user_ref[0].get('accuracy')
    
    accuracy=[]
   
    days=[]
    total=[]
    right=[]
    for i in range(len(acc)):
        total.append(acc[str(i+1)]['total'])
        right.append(acc[str(i+1)]['correct'])
        pct=acc[str(i+1)]['correct']/acc[str(i+1)]['total']
        accuracy.append(pct)

        days.append(i+1)
    total_pct=round(sum(right)/sum(total),2)
    wrong=round(1-total_pct,2)
    pie=[total_pct,wrong]
    

    return render_template('dashboard.html',values=values, label=labels,values1=values1,accuracy=accuracy, pie=pie,days=days)
  

def update_sample():
    user_ref=db.collection('squad2.0')
    documents=db.collection('squad2.0').get()
    
    for docs in documents:
       
        user_ref.document(u'{}'.format(docs.id)).set({u'Chosen':1}, merge= True)
    
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

#runs the application in debug mode
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 4000))
    #update_sample()
    #app.run(host='0.0.0.0', port=port)
    app.run(debug=True)