from network import Handler, poll
import sys
from threading import Thread
from time import sleep


myname = raw_input('What is your name? ')

class Client(Handler):
    
    def on_close(self):
        pass
    
    def on_msg(self, msg):
        if 'txt' in msg:
            print msg['txt'] + "client"
        
host, port = 'localhost', 8888
client = Client(host, port)
client.do_send({'join': myname})

def periodic_poll():
    while 1:
        poll()
        sleep(0.05)  # seconds
                            
thread = Thread(target=periodic_poll)
thread.daemon = True  # die when the main thread dies 
thread.start()

while 1:
    try:
        mytxt = sys.stdin.readline().rstrip()
        client.do_send({'speak': myname, 'txt': mytxt})
    except KeyboardInterrupt:
        client.do_send({'speak': myname, 'txt': 'close'})
        print "Client Shutdown Complete..."
        sys.exit()

