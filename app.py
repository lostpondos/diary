from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from datetime import datetime

client = MongoClient("mongodb://zilong:1l0v3you@ac-yjbaqbi-shard-00-00.k6ulip1.mongodb.net:27017,ac-yjbaqbi-shard-00-01.k6ulip1.mongodb.net:27017,ac-yjbaqbi-shard-00-02.k6ulip1.mongodb.net:27017/?ssl=true&replicaSet=atlas-n62kvh-shard-0&authSource=admin&retryWrites=true&w=majority")
db = client.dbperdiary

app = Flask(__name__)
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/diary', methods=['GET'])
def show_diary():
    articles = list(db.diary.find({},{'_id':False}))
    return jsonify({'articles': articles})

@app.route('/diary', methods=['POST'])
def save_diary():
    title_receive = request.form["title_give"]
    content_receive = request.form["content_give"]

    today = datetime.now()
    mytime = today.strftime('%y-%m-%d-%H-%M-%S')

    file = request.files["file_give"]
    extension = file.filename.split(".")[-1]
    filename = f'static/file-{mytime}.{extension}'
    file.save(filename)

    profile = request.files["profile_give"]
    extension = profile.filename.split(".")[-1]
    profilename = f'static/profile-{mytime}.{extension}'
    profile.save(profilename)

    doc = {
        'profile':profilename,
        'file':filename,
        'title':title_receive,
        'content':content_receive

    }
    db.diary.insert_one(doc)

    return jsonify({'msg':'Upload complete!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)