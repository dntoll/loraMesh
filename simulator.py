from mesh.PymeshAdapter import PymeshAdapter

from view.CompositeView import CompositeView

from simulator.SimulatorSocket import SimulatorSocket
from simulator.FakePycomInterface import FakePycomInterface
from simulator.Radio import Radio
from simulator.SimView import SimView
from time import sleep


view = CompositeView()
radio = Radio()
fpi = FakePycomInterface()

y = 0
clients = []
for i in range(25):
    sv = SimView(i)
    x = i/5
    y = i/5
    socket = SimulatorSocket(i, x, y)
    radio.add(socket)

    clients.append(PymeshAdapter(sv, socket, fpi))

clients[0].sendMessage(24, b"first")
#clients[2].sendMessage(0, b"hello")

timePerStep = 0.01
oneTime = True

for i in range(int(10.0/timePerStep)):
    radio.process()
    sleep(timePerStep)
    if oneTime and i > int(5/timePerStep):
        print("Send")
        oneTime = False
        clients[0].sendMessage(14, b"second")
print("ended tests")

fpi.die()
print("tried to release threads")

print(radio.sends)


import matplotlib as mpl
import matplotlib.pyplot as plt
import networkx as nx

seed = 13648  # Seed random number generators for reproducibility
G = nx.grid_2d_graph(5, 5)
pos = nx.spring_layout(G, seed=seed)

node_sizes = [3 + 10 * i for i in range(len(G))]
M = G.number_of_edges()
edge_colors = range(2, M + 2)
edge_alphas = [(5 + i) / (M + 4) for i in range(M)]
cmap = plt.cm.plasma

nodes = nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color="indigo")
edges = nx.draw_networkx_edges(
    G,
    pos,
    node_size=node_sizes,
    arrowstyle="->",
    arrowsize=10,
    edge_color=edge_colors,
    edge_cmap=cmap,
    width=2,
)
# set alpha value for each edge

ax = plt.gca()
ax.set_axis_off()
plt.show()