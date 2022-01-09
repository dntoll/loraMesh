import time
import _thread

from mesh.pymesh_adapter import PymeshAdapter
from view.CompositeView import CompositeView
from view.RGBView import RGBView
from view.SerialConsoleView import SerialConsoleView
from view.pybytesView import pybytesView

def mainLoopInThread(this, that):

    
    while True:
        this.pm.update()

        if this.pm.isPartOfANetwork():
            this.sendToAll()
            time.sleep(10)
        time.sleep(3)

class App:
    def __init__(self, pybytes):
        
        self.view = CompositeView()
        self.view.add(RGBView())
        self.view.add(SerialConsoleView())
        self.view.add(pybytesView(pybytes))

        self.pm = PymeshAdapter(pybytes, self.view, 0)

    def run(self):
        #Want to run the loop in a separate thread to make sure we can interract with the app on this one
        _thread.start_new_thread(mainLoopInThread, (self, self))
        
            #break
    
    

    def sendToAll(self):
        ips = self.pm.getAllIPs()
        for ip in ips:
            self.pm.sendMessage(ip, "Hello from me " + str(self.pm.getMyAddress()))

a = App(pybytes)
a.run()