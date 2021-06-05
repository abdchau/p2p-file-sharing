# import socket
import flask
import sqlite3
# Import the python libraries
from pymongo import MongoClient
from pprint import pprint
import uuid
# import requests
from flask import request
# from requests.api import request

# import requests
# from requests.api import request

# Choose the appropriate client
client = MongoClient()

# Connect to db
db=client.bittorrent
torrent = db.torrent

# Use the condition to choose the record
# and use the update method
# db.torrent.update_one(
#         {"Age":'42'},
#         {
#         "$set": {
#             "Name":"Srinidhi",
#             "Age":'35',
#             "Address":"New Omsk, WC"
#         }
#         }
# )
	

# Queryresult = torrent.find_one({'Age':'35'})

# pprint(Queryresult)


app = flask.Flask(__name__)

@app.route('/',methods=['GET'])
def get_torrents():
	# get torrents

	return "Server homepage"

@app.route('/',methods=['POST'])
def upload_torrents():
	try:
		print(request)
		body = request.get_json(force=True)
		torrent.insert_one(body)
		
		return "Successfully inserted"
	except Exception as e:
		return e.__str__()

if __name__=='__main__':
	app.run(debug=True)