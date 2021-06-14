from helper.idHandler import IDHandler
from communication.serverconn import ServerConn
from _thread import start_new_thread

idh = IDHandler()
server = ServerConn()

from communication.seeder import Seeder

seeder = Seeder()

start_new_thread(seeder.loop, ())

print(seeder)