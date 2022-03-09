import sys
import os
import cairo
cwd = os.getcwd()
sys.path.append(cwd + "\\MeshTestConsole")




from meshlibrary.PymeshAdapter import PymeshAdapter
from simulator.SimulatorSocket import SimulatorSocket
from simulator.FakePycomInterface import FakePycomInterface
from simulator.Radio import Radio
from simulator.PlotView import PlotView
from meshlibrary.Message import Message


def devNullCallback(origin, content):
    #print("Content: " + content)
    return

radio = Radio()
fpi = FakePycomInterface()

y = 0
clients = []
views = {}
for i in range(25):
    
    x = i // 5
    y = i % 5

    views[i] = PlotView(x, y, i)
    socket = SimulatorSocket(i, x, y, 3)
    print(str(x) + " " + str(y))
    radio.add(i, socket)
    clients.append(PymeshAdapter(views[i], socket, fpi, devNullCallback))


#All nodes send message to the other side
clients[0].sendMessage(1, b"first")

radio.processUntilSilent(secondsOfSilence = 2)
fpi.die()



with cairo.SVGSurface("plotView.svg", 200, 200) as surface:
    context = cairo.Context(surface)
    context.scale(20, 20)

    for i in range(25):
        views[i].draw(context, views)
    