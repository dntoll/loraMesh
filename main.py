import time

from mesh.pymesh_adapter import PymeshAdapter
from view.CompositeView import CompositeView
from view.RGBView import RGBView
from view.SerialConsoleView import SerialConsoleView
from view.pybytesView import pybytesView



class App:
    def __init__(self, pybytes):
        
        self.view = CompositeView()
        self.view.add(RGBView())
        self.view.add(SerialConsoleView())
        self.view.add(pybytesView(pybytes))

        self.pm = PymeshAdapter(pybytes, self.view)

    def run(self):
        while True:
            self.pm.update()

            if self.pm.isPartOfANetwork():
                self.sendToAll()
                time.sleep(10)
            time.sleep(3)
            #break

    def sendToAll(self):
        ips = self.pm.getAllIPs()
        for ip in ips:
            self.pm.sendMessage(ip, "Hello from me " + str(self.pm.getMyAddress()))

a = App(pybytes)
a.run()