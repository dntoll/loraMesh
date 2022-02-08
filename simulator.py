from mesh.PymeshAdapter import PymeshAdapter

from view.CompositeView import CompositeView

from simulator.SimulatorSocket import SimulatorSocket
from simulator.FakePycomInterface import FakePycomInterface


view = CompositeView()

pm = PymeshAdapter(view, SimulatorSocket(1), FakePycomInterface())

pm.sendMessage(1, b"hello")