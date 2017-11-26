import sys
import pymongo
from pymongo import MongoClient
import json
from bson.json_util import dumps,loads
from bson.objectid import ObjectId
import ast
import datetime
import imutils
import time
import os
import csv
import cv2
sys.path.insert(0, '..')

from index import run


class Data:
    def __init__(self,db):
        self.db = db
        self.col = [db.videos1,db.videos2,db.videos3,db.videos4,db.videos5]
        self.users = db.User
        self.uploaded = db.uploaded
        self.usersList = ["user1","user2","user3","user4","user5"]

    def getAnnotations(self,user):
        ind = self.usersList.index(user)
        data = self.col[ind].find({"annotated":False})
        for i in data:
            print dumps(i)

    def uploadStart(self,filename):
        path = './uploads/'
        file_path = path + filename
        # vs = cv2.VideoCapture(file_path)
        doc = {}
        date = str(datetime.date.today())
        time = str(datetime.datetime.now().time()).split('.')[0]
        doc['vid_path'] = file_path
        doc['upload_date'] = date
        doc['upload_time'] = time
        doc['annotated'] = False
        doc['fps'] = 25
        doc['data'] = []
        self.uploaded.insert_one(doc)

    def uploadDone(self,db):
        print 'Hello'

    def feedbackAdd(self,db,vid_id,rating, endFrame, startFrame, done, user, feedback):
        print vid_id
        if done == "true":
            done = True
        else:
            done = False
        ind = self.usersList.index(user)
        self.col[ind].update_one(
            {"_id": ObjectId(vid_id)},
            {
                '$push': {"data": {"start-frame": startFrame, "end-frame": endFrame, "tags": feedback, "score": rating, "user": user} },
                '$set': {"annotated": done}
            }
        )

    def genData(self,db,output_path,user):
        ind = self.usersList.index(user)
        data = self.col[ind].find({"annotated": True})
        output = []
        for l in data:
            output.append([l['vid_path'],l['data'][0]['score']])
        with open(output_path, "wb") as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            for line in output:
                writer.writerow(line)

    def findUser(self,db,u,p):
        userExists = self.users.find({"username": u})
        if userExists.count() == 0:
            print 'wrong-username'
            return
        passUser = self.users.find({"password":p,"username":u}).count()
        if passUser == 1:
            print 'correct'
        else:
            print 'wrong-pass'

    def find(self, name, path):
        for root, dirs, files in os.walk(path):
            if name in files:
                return os.path.join(root, name)

    def getGenre(self,filename):
        filename = self.find(filename,'../../Dataset')
        # print filename
        out = run('nn',filename)
        if out[0][0] == 1:
            print 'classical'
        elif out[0][1] == 1:
            print 'pop'
        elif out[0][2] == 1:
            print 'jazz'
        elif out[0][3] == 1:
            print 'metal'

    def getReco(self,filename,genre):
        print run('reco',filename,genre)

def init():
    client = MongoClient()
    db = client.visualise
    data = Data(db)
    args = []
    for i in sys.argv:
        args.append(i)

    if len(args) > 1:
        if args[1] == 'get-all':
            data.getAnnotations(args[2])
        elif args[1] == 'get-genre':
            data.getGenre(args[2])
        elif args[1] == 'get-reco':
            data.getReco(args[2],args[3])
        elif args[1] == 'upload-start':
            data.uploadStart(args[2])
        elif args[1] == 'upload-done':
            data.uploadDone(db)
        elif args[1] == 'feedback-add':
            tags = []
            for tag in args[8:]:
                tags.append(tag)
            data.feedbackAdd(db, args[2], args[3], args[4], args[5], args[6], args[7], tags)
        elif args[1] == 'annotated-data':
            output_path = "output_" + args[2] + ".csv"
            data.genData(db,output_path,args[2])
        elif args[1] == 'find-user':
            data.findUser(db,args[2],args[3])
init()
