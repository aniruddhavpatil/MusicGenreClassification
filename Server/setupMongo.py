import os
import pymongo
import json
import sys
import datetime
from pymongo import MongoClient
import cv2

N = 1
def init():
    global N
    # lines = [line.rstrip('\n') for line in open('config.js')]
    f = open('config.js')
    config = json.load(f)
    N = config['no_of_annotators']

def setup(client):
    global N
    reset = False
    db = client.visualise
    videos = []
    colls = db.collection_names()
    if 'User' not in colls:
        user = db.create_collection('User')
        for i in range(1,6):
            user.insert_one({
            'username': 'user' + str(i),
            'password': 'iiit123'
            })
    else:
        choice = raw_input('Use existing user database? [y/n]: ')
        if choice == 'n':
            db['User'].drop()
            user = db.create_collection('User')
            for i in range(0,5):
                user.insert_one({
                'username': 'user' + str(i),
                'password': 'iiit123'
                })

    for i in range(1,N + 1):
        name = 'videos' + str(i)
        if name in colls:
            if not reset:
                choice = raw_input('One or more of the tables already exists, if you choose to continue they will be deleted and made fresh [y/n]: ')
                if choice == 'y':
                    reset = True
                else:
                    exit()
            db[name].drop()
            coll = db.create_collection(name)
            videos.append(db[name])
        else:
            coll = db.create_collection(name)
            videos.append(db[name])

    for f in os.walk(sys.argv[1]):
        fileLoc = f[0]
        for fil in f[2]:
		for i in videos:
	            if i.find({"vid_path": fileLoc + '/' + fil}).limit(1).count() == 0:
        	        vs = cv2.VideoCapture(fileLoc + '/' + fil)
	                doc = {}
	                date = str(datetime.date.today())
	                time = str(datetime.datetime.now().time()).split('.')[0]
	                doc['vid_path'] = fileLoc + '/' + fil
	                doc['upload_date'] = date
	                doc['upload_time'] = time
                	doc['annotated'] = False
	                doc['fps'] = vs.get(5)
	                doc['data'] = []
		        i.insert_one(doc)

client = MongoClient()
init()
setup(client)
