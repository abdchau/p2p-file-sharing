# import socket
import flask
import sqlite3
# Import the python libraries
from pymongo import MongoClient
from pprint import pprint
import uuid
# import requests
import json
from flask import request
# from requests.api import request
from bson.json_util import dumps, loads
# import requests
# from requests.api import request

# Choose the appropriate client
client = MongoClient()

# Connect to db
db=client.bittorrent
torrent = db.torrent
peer = db.peer

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
	body = request.get_json(force=True)
	print(body)
	ans = list(torrent.find(body))
	# print(dumps(ans))
	return dumps(ans)

@app.route('/',methods=['POST'])
def upload_torrents():
	try:
		# print(request)
		body = request.get_json(force=True)
		torrent.insert_one(body)
		
		return "Successfully inserted"
	except Exception as e:
		return e.__str__()

@app.route('/id',methods=['GET'])
def get_id():
	uu = str(uuid.uuid4())
	# print(uu)
	return dumps({'id': uu})

@app.route('/id',methods=['POST'])
def update_port():
	body = request.get_json(force=True)
	print(body)
	peer.update_one({'id': body['id']}, {'$set': {'sock': body['sock']}}, upsert=True)
	return 'Socket info updated'

@app.route('/peer',methods=['GET'])
def get_peer():
	body = request.get_json(force=True)
	print(body)
	p = peer.find_one({'id':body['id']})
	print(p)
	return dumps(p['sock'])

@app.route('/piece',methods=['POST'])
def update_piece_peer():
	body = request.get_json(force=True)
	print(body)
	file = torrent.find_one({'file_id': body['file_id']})
	file['pieces_info'][body['piece_seq_no']]['peers'].append(body['new_peer'])
	torrent.update_one({'file_id': body['file_id']}, {'$set': {'pieces_info': file['pieces_info']}})
	return 'Peer added'

if __name__=='__main__':
	app.run(debug=True)