from network import Listener, Handler, poll
import sys

handlers = {}  # map client handler to user name
 
class MyHandler(Handler):
     
    def on_open(self):
        pass
         
    def on_close(self):
        pass
     
    def on_msg(self, msg):
        if 'join' in msg:
            print msg['join'] + " has joined."
            handlers[msg['join']] = self
            
            #need to figure out the type of what self is and need to delete the correct one
##            print handlers.keys()
        if 'txt' in msg:
            print msg['speak'] +": " + msg['txt']
        if 'txt' in msg:
            if msg['txt'] == 'quit':
                print msg['speak'] + " has left..."
                del handlers[msg['speak']]
##                print self.__class__.__name__
                Handler.do_close(self)
                
 
 
port = 8888
server = Listener(port, MyHandler)
while 1:
    try:
        poll(timeout=0.05) # in seconds
    except KeyboardInterrupt:
        print "Closing server, Bye: "
        for client in handlers:
            print client
            Handler.do_close(handlers[client])
        print handlers.keys()

        print "Server Shutdown Complete..."
        sys.exit()


