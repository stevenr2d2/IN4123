from network import Listener, Handler, poll
import re


handlers = {}  # map client handler to user name
names = {} # map name to handler
subs = {} # map tag to handlers

def broadcast(msg):
    for h in handlers.keys():
        h.do_send(msg)


class MyHandler(Handler):
    
    def on_open(self):
        handlers[self] = None
        
    def on_close(self):
        name = handlers[self]
        del handlers[self]
        broadcast({'leave': name, 'users': handlers.values()})
        
    def on_msg(self, msg):
        if 'join' in msg:
            name = msg['join']
            handlers[self] = name
            broadcast({'join': name, 'users': handlers.values()})
        elif 'speak' in msg:
            name, txt = msg['speak'], msg['txt']


	    m = re.findall(r"\+\S+", txt)
	    if (len(m) > 0):
		##add people to hashTage subscribed too
		for hashtag in m:
		    if subs.has_key(hashtag):
			if self not in subs[hashtag]:
		            subs[hashtag].append(self)
			name = str(len(subs[hashtag]))
		    else:
			hashtag = hashtag[1:] 
		        subs[hashtag] = [self] 

	    x = re.findall(r"\#\S+", txt)
	    if (len(x) > 0):
                for hashtagSend in x:
		    hashtagSend = hashtagSend[1:]
	 	    if subs.has_key(hashtagSend):
		        for handler in subs[hashtagSend]:
        		    handler.do_send({'speak': name, 'txt': txt})

	    y = re.findall(r"\-\S+", txt)
	    if (len(y) > 0):
                for hashtagRemove in y:
		    hashtagRemove = hashtagRemove[1:]
	 	    if subs.has_key(hashtagRemove):
		        if self in subs[hashtagRemove]:
			    subs[hashtagRemove].remove(self)

	    z = re.findall(r"\@\S+", txt)
	    if (len(z) > 0):
                for userName in z:
		    userName = userName[1:]
		    for key in handlers:
		        if handlers[key] == userName:
        		    key.do_send({'speak': name, 'txt': txt})

#            broadcast({'speak': name, 'txt': txt})



Listener(8888, MyHandler)
while 1:
    poll(0.05)
