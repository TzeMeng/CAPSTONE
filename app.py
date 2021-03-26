import pyrebase
import firebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import firebase_admin
from firebase_admin import credentials

import flask

cred = credentials.Certificate("ENTER YOUR CREDENTIALS HERE")
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
print(title_context['Normans'])

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