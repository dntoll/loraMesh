import sys
import os
cwd = os.getcwd()
sys.path.append(cwd + "\\MeshTestConsole")




from meshlibrary.PymeshAdapter import PymeshAdapter
from simulator.SimulatorSocket import SimulatorSocket
from simulator.FakePycomInterface import FakePycomInterface
from simulator.Radio import Radio
from simulator.SimTestView import SimTestView
from view.CompositeView import CompositeView
from meshlibrary.Message import Message
import time

radio = Radio()
fpi = FakePycomInterface()

y = 0
clients = []
views = {}


chainLength = 100
for i in range(chainLength):
    
    views[i] = CompositeView()
    if i == 0:
        views[0] = SimTestView(i)    
    x = i
    y = 0
    socket = SimulatorSocket(i, x, y)
    radio.add(i, socket)
    clients.append(PymeshAdapter(views[i], socket, fpi))


#All nodes send message to the other side
clients[0].sendMessage(chainLength-1, bytes(i))

print ("test starts")
pre = time.time()
radio.processUntilSilent(secondsOfSilence = 0.5)
post = time.time()
print ("test finished")

if views[0].hasMessageFrom(chainLength-1, Message.TYPE_ACC):
    print(str(0) + " got Acc from " + str(chainLength-1))

print("We got a response in " +str(post-pre-0.5) + " sends." )

fpi.die()        
print("ended tests")


