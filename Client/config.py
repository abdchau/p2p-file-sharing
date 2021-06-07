from helper.idHandler import IDHandler

# in bytes
PIECE_SIZE = 256
idH = IDHandler()

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