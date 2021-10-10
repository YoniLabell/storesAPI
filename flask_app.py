from flask import Flask, redirect, render_template, request, url_for,jsonify
from flask_sqlalchemy import SQLAlchemy
import requests
import json
import xmltodict
import os
import time
from datetime import datetime, timedelta

app = Flask(__name__)

app.config["DEBUG"] = True


SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="yonilabell",
    password="mydatabase",
    hostname="yonilabell.mysql.pythonanywhere-services.com",
    databasename="yonilabell$comments",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Comment(db.Model):

    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(4096))

class User(db.Model):

    __tablename__ = "Users"

    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(4096))

comments = []

@app.route("/")
def home():
    return render_template("portfolio.html")

@app.route("/portfolio")
def portfolio():
    return render_template("portfolio.html")

@app.route("/MyCV")
def mycv():
    return render_template("mycv.html")

@app.route("/adduser/<uid>/<name>")
def adduser(uid,name):
    #users=[]
    newuser = User(id=uid,user=name)
    db.session.add(newuser)
    db.session.commit()
    #users=User.query.all()
    return str(name)+" added"

@app.route("/admin/getusers")
def getUsers():


        users=User.query.all()
        myusers=''
        for user in users:
            myusers+=str(user.user)+':'+str(user.id)+'\n'
        return myusers+'\n'+str(len(users))



@app.route("/getp/<stor>/<id>/<item>")
def getp(stor,id,item):
    try:
        path="/home/yonilabell/stores_dir/"+stor+"/"+id+"p.json"
        with open(path) as f:
            data = json.load(f)

        return jsonify(data[item])
    except:
        return "item not found"

@app.route("/getstores")
def getstores():
    path='/home/yonilabell/stores_dir/'
    file='/stores.xml'
    stores={}
    for dir in os.listdir(path):
        with open(path+dir+file) as pf:
            doc = xmltodict.parse(pf.read())
            stores[dir]={s['StoreId']:s['City']+','+s['Address'] for s in doc['Root']['SubChains']['SubChain']['Stores']['Store'] if s['City'] != 'unknown' }

    return jsonify(stores)

@app.route("/getsubstores/<store>")
def gets(store):
    path='/home/yonilabell/stores_dir/'
    file='/stores.xml'
    stores={}

    with open(path+store+file) as pf:
        doc = xmltodict.parse(pf.read())
        stores={s['StoreId']:s['City']+', '+s['Address'] for s in doc['Root']['SubChains']['SubChain']['Stores']['Store'] if s['City'] != 'unknown' }

    return jsonify(stores)

@app.route("/getstore/<store>/<id>")
def getstore(store,id):
    path='/home/yonilabell/stores_dir/'
    file='/stores.xml'
    astore={}

    with open(path+store+file) as pf:
        doc = xmltodict.parse(pf.read())
        astore={'0':''+s['StoreName']+'\n עיר: '+s['City']+', כתובת: '+s['Address'] for s in doc['Root']['SubChains']['SubChain']['Stores']['Store'] if int(s['StoreId']) == int(id)  }
    return jsonify(astore)



@app.route("/getitembymame/<name>")
def get_item_by_mame(name):

    try:

        path="/home/yonilabell/all_names/all_names.json"
        with open(path) as f:
            names = json.load(f)

        data={}
        for k, v in names.items():
            if len(data)>9:
                break

            if name in k :
                if v in data.values():
                    pass
                else:
                    data[k]=v

        return jsonify(data)

    except:
        return jsonify({})

@app.route("/getitembyid/<id>")
def get_item_by_id(id):
    try:
        path="/home/yonilabell/all_names/all_ids.json"
        with open (path) as f:
            items=json.load(f)
        return jsonify(items[id])

    except:
        return jsonify({False})


@app.route('/timenow')
def timenow():
    t=datetime.now() + timedelta(hours=3)# IL time
    lastUpdated=str('{:%d/%m/%Y, %H:%M}'.format(t))
    t = open("lastUpdated.txt", "w")
    t.write(str(lastUpdated))
    t.close()
    return  str(lastUpdated)



@app.route("/lastUpdated")
def lastUpdated():
    t = open("lastUpdated.txt", "r")
    lastUpdated=t.read()
    t.close()
    return str(lastUpdated)

@app.route("/cheapest/<item>")
def cheapest(item):
    cheapestitem=float('inf')
    for i in stores:
        for j in sub:
            return




    return  cheapestitem

@app.route("/test")
def test():

    return "ok"

@app.route("/test1")
def test1():

    return jsonify({'0':'test1'})

@app.route("/ERROR")
def error():

    return "ERROR", 500



