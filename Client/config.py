from helper.idHandler import IDHandler
from communication.serverconn import ServerConn
from _thread import start_new_thread
import time

# in bytes
PIECE_SIZE = 256
idh = IDHandler()
server = ServerConn()

from communication.seeder import Seeder

seeder = Seeder()

start_new_thread(seeder.loop, ())

print(seeder)
'''
- db_piece_info of file
	- array of pieces
		- seq num
		# - size
		- md5 hash
	- file name

- peers_info
	# - owner is the first peer
	- peer_ip:port
	- uuid
	- piece seq no. array
	- randomly select peer for piece

- file
	- no. of pieces
	piece_info
		# - which file it belongs to
		- sequence no. of piece
		- piece_bytes
'''