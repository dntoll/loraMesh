import sys
import os
import cairo
import math
cwd = os.getcwd()
sys.path.append(cwd + "\\MeshTestConsole")

from meshlibrary.PymeshAdapter import PymeshAdapter
from simulator.SimulatorSocket import SimulatorSocket
from simulator.FakePycomInterface import FakePycomInterface
from simulator.Radio import Radio
from simulator.PlotView import PlotView
from meshlibrary.Message import Message


def devNullCallback(origin, content):
    return

radio = Radio()
fpi = FakePycomInterface()

y = 0
clients = []
views = {}
numClients = 100
width = math.sqrt(numClients)
for i in range(numClients):
    x = i // width
    y = i % width
    views[i] = PlotView(x, y, i)
    socket = SimulatorSocket(i, x, y, 1)
    radio.add(i, socket)
    clients.append(PymeshAdapter(views[i], socket, fpi, devNullCallback))


#All nodes send message to the other side

def sendWaitDraw(context, fromNode, toNode, translateX, translateY, mess):
    for i in range(numClients):
        views[i].clear()
    clients[fromNode].sendMessage(toNode, mess)
    radio.processUntilSilent(secondsOfSilence = 1)

    context.translate(translateX, translateY)
    for i in range(numClients):
        views[i].draw(context, views)
    for i in range(numClients):
        views[i].drawNumbers(context, views)
    


with cairo.SVGSurface("plotView.svg", 800, 800) as surface:
    context = cairo.Context(surface)
    context.scale(400/width, 400/width)
    context.set_source_rgb(0,0,0)
    context.set_line_width(0.04)

    fromNode = 52
    toNode = 46

    sendWaitDraw(context, fromNode, toNode, 0, 0, b"message")
    sendWaitDraw(context, fromNode, toNode, 10, 0, b"message2")
    sendWaitDraw(context, fromNode, toNode, -10, 10, b"message3")
    sendWaitDraw(context, fromNode, toNode, 10, 0, b"message4")

    
    
        

fpi.die()