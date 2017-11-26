#!/bin/bash

echo 'Checking for mongofiles/db folder'
if ! [ -d "mongofiles/db" ]; then
echo 'Found existing folder'
mkdir -p mongofiles/db
fi
echo 'Checking for running mongod instance'
m=`ps | grep 'mongod' | wc -l`
if [ $m -eq 0 ]; then
echo 'Instance not found, starting new instance'
mongod --dbpath mongofiles/db > output_mongo.log 2>&1 &
fi

echo 'Setting up database'

python setupMongo.py $1

echo 'Database setup complete, starting server..'

nodemon bin/www 3011

