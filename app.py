import pyrebase
import firebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import firebase_admin
from firebase_admin import credentials

from flask import Flask, render_template, request, jsonify
import json

cred = credentials.Certificate("C:/Users/Hazel Tan/Documents/BT4103 Capstone/capstone-dsta-firebase-adminsdk-2kf8q-bc7d2cae62.json")
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

from flask import *

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
        html_string_selected += '<option value="{}">{}</option>'.format(entry, entry)

    return jsonify(html_string_selected=html_string_selected)


@app.route('/_process_data')
def process_data():
    selected_class = request.args.get('selected_class', type=str)
    selected_entry = request.args.get('selected_entry', type=str)

    # process the two selected values here and return the response; here we just create a dummy string

    return jsonify(random_text="you selected {} and {}".format(selected_class, selected_entry))


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
                           all_entries=default_values)

@app.route('/', methods=['GET', 'POST'])
def basic():
    if request.method == 'POST':
        if request.form['submit'] == 'add':
            name = request.form['name']
            db.child("todo").push(name)
            todo = db.child("todo").get()
            to = todo.val()
            return render_template('index.html', t=to.values())
        elif request.form['submit'] == 'delete':
            db.child("todo").remove()
        return render_template('index.html')
    return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True)