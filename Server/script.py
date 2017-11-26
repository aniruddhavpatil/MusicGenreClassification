import sys
import MySQLdb
import json
import ast
import datetime
import imutils
import time
import os
import csv
import cv2
# f = open("test", "w+")
# f.write(sys.argv[1])
path = '/home/arn197/cvit/visualise/data/'
# f.close()
class Data:
    def __init__(self,db):
        self.cursor = db.cursor()
        self.id = 0

    def getID(self):
        command = "select * from data"
        try:
            # Execute the SQL command
            self.cursor.execute(command)
            # Fetch all the rows in a list of lists.
            self.id = self.cursor.rowcount
        except:
            print "Error: unable to fetch data"
            # disconnect from server

    def getAll(self):
        command = "select * from split_data where tagged=0"
        try:
            # Execute the SQL command
            self.cursor.execute(command)
            # Fetch all the rows in a list of lists.
            results = self.cursor.fetchall()
            for row in results:
                data = {}
                data['id'] = row[0]
                data['vid_path'] = row[1]
                data['score'] = row[2]
                data['upload_date'] = str(row[3])
                data['upload_time'] = str(row[4])
                data['tagged'] = row[5]
                json_data = json.dumps(data)
                print json_data
                # res.append(json_data)
            # print res
        except:
            print "Error: unable to fetch data"
            # disconnect from server
    def uploadStart(self,db,filename):
        global path
        file_path = path + filename
        # time = str(datetime.date.today()) + ' ' + str(datetime.datetime.now().time()).split('.')[0]
        time = '2017-09-17'
        command = "insert into vid_data (vid_path, tag, score, upload_date, status) values ('%s', '%s', %d, '%s', '%s')" % (file_path, 'none', 0, time, 'pending')
        # print command
        try:
            # Execute the SQL command
            self.cursor.execute(command)
            # Fetch all the rows in a list of lists.
            db.commit()
        except:
            print "Error: unable to enter data into database"
            # disconnect from server

    def uploadDone(self,db):
        command = "update vid_data set status='%s' where id=%d" % ('active',self.id)
        try:
            # Execute the SQL command
            self.cursor.execute(command)
            # Fetch all the rows in a list of lists.
            db.commit()
            # print 'Success'
        except:
            print "Error: unable to fetch data"
            # disconnect from server
    def feedbackAdd(self,db,vid_no,rating,feedback):
        # time = str(datetime.date.today()) + ' ' + str(datetime.datetime.now().time()).split('.')[0]
        # getVid = "select * from vid_data where id=%d" % (int(vid_no))
        rating = "update split_data set score=%f,tagged=%r where id=%d" % (float(rating),True,int(vid_no))
        # print insertNew
        try:
            # Execute the SQL command
            self.cursor.execute(rating)
            db.commit()
        except:
            print "Error: unable to enter data into database"
            # disconnect from server
        insertNew = "insert into tags (video_id, tag) values (%d, '%s')" % (int(vid_no), feedback)
        print rating,insertNew
        try:
            # Execute the SQL command
            self.cursor.execute(insertNew)
            db.commit()
        except:
            print "Error: unable to enter data into database"
            # disconnect from server

    def genData(self,db,output_path):
        command = "select vid_path,tag,score from split_data as s,tags as t where s.id = t.video_id order by video_id"
        try:
            self.cursor.execute(command)
            results = self.cursor.fetchall()
            vids = []
            data = []
            for row in results:
                index = -1
                if row[0] in vids:
                    index = vids.index(row[0])
                if index > -1:
                    data[index].append(row[1])
                else:
                    vids.append(row[0])
                    print row[0]
                    data.append([row[0],row[2],row[1]])
            with open(output_path, "wb") as csv_file:
                writer = csv.writer(csv_file, delimiter=',')
                for line in data:
                    writer.writerow(line)
        except:
            print "Error: unable to fetch data from database"

def init():
    db = MySQLdb.connect("localhost","root","pass","visualise")
    data = Data(db)
    global path
    # if sys.argv[1] == 'get-all':
    data.getID()
    # f = "/home/arn197/cvit/visualize-backend/data/Rick.and.Morty.S03E07.720p.HDTV.2CH.x265.HEVC-PSA.mkv"
    # d = f.split(".")[0] + 'split/'
    # data.split(f,d)
    c = 0
    args = []
    for i in sys.argv:
        args.append(i)
    if len(args) > 1:
        if args[1] == 'get-all':
            data.getAll()
        elif args[1] == 'upload-start':
            # print 'Hello'
            # print args[2]
            data.uploadStart(db,args[2])
        elif args[1] == 'upload-done':
            data.uploadDone(db)
        elif args[1] == 'feedback-add':
            for tag in args[4:]:
                data.feedbackAdd(db, args[2], args[3], tag)
        elif args[1] == 'annotated-data':
            output_path = "output.csv"
            data.genData(db,output_path)
    db.close()

init()
