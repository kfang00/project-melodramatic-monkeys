import os
from queue import Empty
from flask import Flask, render_template, request
from dotenv import load_dotenv
from peewee import *
import datetime
from playhouse.shortcuts import model_to_dict
import re

load_dotenv()
app = Flask(__name__)

if os.getenv("TESTING") == "true":
    print("Running in test mode")
    mydb = SqliteDatabase('file:memory?mode=memory&cache=shared',uri=True)
else:
    mydb = MySQLDatabase(os.getenv("MYSQL_DATABASE"),
        user = os.getenv("MYSQL_USER"),
        password = os.getenv("MYSQL_PASSWORD"),
        host = os.getenv("MYSQL_HOST"),
        port = 3306
    )

print(mydb)

class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = mydb

mydb.connect()
mydb.create_tables([TimelinePost])

isKayla = True

@app.route('/')
def mario_index():
    return render_template('mario_index.html', url=os.getenv("URL"), title="Mario")

@app.route('/mario_about')
def mario_about():
    return render_template('mario_about.html', url=os.getenv("URL"))

@app.route('/mario_experience')
def mario_experience():
    return render_template('mario_experience.html', url=os.getenv("URL"))

@app.route('/mario_education')
def mario_education():
    return render_template('mario_education.html', url=os.getenv("URL"))

@app.route('/mario_hobbies')
def mario_hobbies():
    return render_template('mario_hobbies.html', url=os.getenv("URL"))

@app.route('/mario_places')
def mario_places():
    return render_template('mario_places.html', url=os.getenv("URL"))



@app.route('/kayla')
def kayla_index():
    return render_template('kayla_index.html', url=os.getenv("URL"))

@app.route('/kayla_about')
def kayla_about():
    return render_template('kayla_about.html', url=os.getenv("URL"))

@app.route('/kayla_experience')
def kayla_experience():
    return render_template('kayla_experience.html', url=os.getenv("URL"))

@app.route('/kayla_education')
def kayla_education():
    return render_template('kayla_education.html', url=os.getenv("URL"))

@app.route('/kayla_hobbies')
def kayla_hobbies():
    return render_template('kayla_hobbies.html', url=os.getenv("URL"))

@app.route('/kayla_places')
def kayla_places():
    return render_template('kayla_places.html', url=os.getenv("URL"))


@app.route('/api/timeline_post', methods=['POST'])
def post_time_line_post():
    try:
        name = request.form['name']
        if name == "":
            return "Invalid name",400
    except:
        return "Invalid name", 400

    try:
        email = request.form['email']
        if not re.search('^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$',email):
            return "Invalid email",400
    except:
        return "Invalid email",400

    try:
        content = request.form['content']
        if content == "":
            return "Invalid content",400
    except:
        return "Invalid content",400
        
    timeline_post = TimelinePost.create(name=name, email=email, content=content)
    return model_to_dict(timeline_post)
        

@app.route('/api/timeline_post', methods=['GET'])
def get_time_line_post():
    return {
        'timeline_posts': [
            model_to_dict(p)
            for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
    }
    
@app.route('/timeline')
def timeline():
    return render_template('timeline.html', title = "Timeline", posts = get_time_line_post()['timeline_posts'], url=os.getenv("URL"))

@app.route('/timeline', methods=['POST'])
def timeline_post():
    post_time_line_post()
    return render_template('timeline.html', title = "Timeline", posts = get_time_line_post()['timeline_posts'], url=os.getenv("URL"))

@app.route('/api/timeline_post', methods=['DELETE'])
def delete_time_line_post():
    name = request.form['name']
    post = TimelinePost.get(TimelinePost.name == name)
    post.delete_instance()
    return "done"