import csv
import json
import sys

csvfile = open(sys.argv[1], 'r')
jsonfile = open('output.json', 'w')

reader = csv.reader( csvfile)
temp = []
for row in reader:
    temp.append([row[0][4:], row[1]])

json.dump(temp,jsonfile)
