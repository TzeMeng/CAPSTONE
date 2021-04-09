import pyrebase
import firebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import firebase_admin
from firebase_admin import credentials
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
    selected_class = request.args.get('selected_class', type=str)
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
                           len = len(default_values))

@app.route("/test", methods = ['GET','POST'])
def test():
    select = request.form.get('val')
    return (str(select))


@app.route("/_evaluate")
def evaluate():
    selected_entry = request.args.get('selected_entry', type=str)
    question = request.args.get('question', type=str)
    print(selected_entry)
    print(type(selected_entry))
    print(question)
    print(type(question))
    answer = eval(selected_entry, question)
    # return (selected_entry)
    return jsonify(answer="Answer: {}".format(answer))


if __name__ == '__main__':
    app.run(debug=True)