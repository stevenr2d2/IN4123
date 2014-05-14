from random import randint
from time import sleep

from network import Handler, poll
from pygame import Rect, init as init_pygame
from pygame.display import set_mode, update as update_pygame_display
from pygame.draw import rect as draw_rect
from pygame.event import get as get_pygame_events
from pygame.time import Clock

################### MODEL #############################
def collide_boxes(box1, box2):
    x1, y1, w1, h1 = box1
    x2, y2, w2, h2 = box2
    return x1 < x2 + w2 and y1 < y2 + h2 and x2 < x1 + w1 and y2 < y1 + h1

class Model():
    
    cmd_directions = {'up': (0, -1),
                      'down': (0, 1),
                      'left': (-1, 0),
                      'right': (1, 0)}
    
    def __init__(self):
        global borders, pellets, players, myname
        
##        self.borders = borders
##        self.pellets = pellets
        self.game_over = False
##        self.mydir = self.cmd_directions['down']  # start direction: down
##        self.mybox = [200, 150, 10, 10]  # start in middle of the screen
        
    def do_cmd(self, cmd):
        if cmd == 'quit':
            self.game_over = True
##        else:
##            self.mydir = self.cmd_directions[cmd]
            
##    def update(self):
##        
##        # move me
##        self.mybox[0] += self.mydir[0]
##        self.mybox[1] += self.mydir[1]
##        # potential collision with a border
##        for b in self.borders:
##            if collide_boxes(self.mybox, b):
##                self.mybox = [200, 150, 10, 10]
##        # potential collision with a pellet
##        for index, pellet in enumerate(self.pellets):
##            if collide_boxes(self.mybox, pellet):
##                self.mybox[2] *= 1.2
##                self.mybox[3] *= 1.2
##                self.pellets[index] = [randint(10, 380), randint(10, 280), 5, 5]
##            



################### CONTROLLER #############################

import pygame
from pygame.locals import KEYDOWN, QUIT, K_ESCAPE, K_UP, K_DOWN, K_LEFT, K_RIGHT

class Controller():
    def __init__(self, m):
        self.m = m
        pygame.init()
   
    def poll(self):
        global client, borders, pellets, players, myname
        randomDirection = randint(0, 3)
        cmd = None
        for event in pygame.event.get():  # inputs
            if event.type == QUIT:
                exit()
            if event.type == KEYDOWN:
                key = event.key
                if key == K_ESCAPE:
                    exit()
##        if randomDirection == 0:
##            msg = {'input': 'up'}
##            client.do_send(msg)
##        if randomDirection == 1:
##            msg = {'input': 'down'}
##            client.do_send(msg)
##        if randomDirection == 2:
##            msg = {'input': 'left'}
##            client.do_send(msg)
##        if randomDirection == 3:
##            msg = {'input': 'right'}
##            client.do_send(msg)

        p = pellets[0]
        b = players[myname]
        if p[0] > b[0]:
            msg = {'input': 'right'}
            client.do_send(msg)
        elif p[0] + p[2] < b[0]:
            msg = {'input': 'left'}
            client.do_send(msg)
        elif p[1] > b[1]:
            msg = {'input': 'down'}
            client.do_send(msg)
        else:
            msg = {'input': 'up'}
            client.do_send(msg)
##        def poll(self):
##        randomDirection = randint(0, 3)
##        cmd = None
##        for event in pygame.event.get():  # inputs
##            
##            if event.type == QUIT:
##                exit()
##            if event.type == KEYDOWN:
##                if key == K_ESCAPE:
##                    key = event.key
##                    exit()
##                elif key in valid_inputs:
##                    msg = {'input': valid_inputs[key]}
##                    client.do_send(msg)
##        if cmd:
##            self.m.do_cmd(cmd)

##################### CONTROLLER #############################
class NetworkController (Handler):
    def on_msg(self, data):
        global borders, pellets, players, myname
        borders = [make_rect(b) for b in data['borders']]
        pellets = [make_rect(p) for p in data['pellets']]
        players = {name: make_rect(p) for name, p in data['players'].items()}
        myname = data['myname']
        

################### VIEW #############################

class View():
    def __init__(self, m):
        self.m = m
        pygame.init()
        self.screen = pygame.display.set_mode((400, 300))
        self.frameCounter = 0;
        
    def display(self):
        global borders, pellets, players, myname, clock
        screen = self.screen
        screen.fill((0, 0, 64))  # dark blue
        [draw_rect(screen, (0, 191, 255), b) for b in borders]  # deep sky blue 
        [draw_rect(screen, (255, 192, 203), p) for p in pellets]  # shrimp
        for name, p in players.items():
            if name != myname:
                draw_rect(screen, (255, 0, 0), p)  # red
            if myname:
                draw_rect(screen, (0, 191, 255), players[myname])  # deep sky blue

            print "Position: " + str(players[myname][0]) +","+ str(players[myname][1])
        
        update_pygame_display()
        clock.tick(50)
        
##        borders = [pygame.Rect(b[0], b[1], b[2], b[3]) for b in self.m.borders]
##        pellets = [pygame.Rect(p[0], p[1], p[2], p[3]) for p in self.m.pellets]
##        b = self.m.mybox
##        myrect = pygame.Rect(b[0], b[1], b[2], b[3])
##        for name, p in players.items():
##            if myname:
##                myrect = draw_rect(screen, (0, 191, 255), players[myname])  # deep sky blue
##
##        screen.fill((0, 0, 64))  # dark blue
##        pygame.draw.rect(screen, (0, 191, 255), myrect)  # Deep Sky Blue
##        [pygame.draw.rect(screen, (255, 192, 203), p) for p in pellets]  # pink
##        [pygame.draw.rect(screen, (0, 191, 255), b) for b in borders]  # red
##        self.frameCounter += 1
##        if self.frameCounter == 50:
##            print "Position: " + str(self.m.mybox[0]) +","+ str(self.m.mybox[1])
##            self.frameCounter = 0
##
##            
##        pygame.display.update()


    
################### LOOP #############################

def make_rect(quad):  # make a pygame.Rect from a list of 4 integers
    x, y, w, h = quad
    return Rect(x, y, w, h)
#Connect to server if, to get server side data needs to input into the game (borders, pellets, player, ... ect)      
client = NetworkController('localhost', 8888)  # connect asynchronously


borders = []
pellets = []
players = {}  # map player name to rectangle
myname = None
clock = Clock()
## wait until we are connected to the server
while(borders == []):
    poll()  # push and pull network messages
    print "Please wait..."
    
##test to see if we get databack from server
##print str(borders[0][3])
print "Connected to server"

model = Model()
c = Controller(model)
v = View(model)

while not model.game_over :

    beforePullValuex = players[myname][0]
    beforePullValuey = players[myname][1]

    beforePellet1x = pellets[0][0]
    beforePellet1y = pellets[0][1]
    
    poll()
    sleep(0.1)
    c.poll()
##    model.update()
    v.display()

    afterPullValuex = players[myname][0]
    afterPullValuey = players[myname][1]

    AfterPellet1x = pellets[0][0]
    AfterPellet1y = pellets[0][1]
    

    if ((beforePullValuex == afterPullValuex) and beforePullValuey == afterPullValuey):
            model.game_over = True
            print "Server Has Been Disconnected! Bye Bye"

    if( (beforePellet1x != AfterPellet1x) and (beforePellet1y != AfterPellet1y)):
        print "Pellet was eaten"


    



