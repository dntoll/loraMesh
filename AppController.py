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

        """if this.pm.isPartOfANetwork():
            this.sendToAll("Ping")
            time.sleep(10)"""
        time.sleep(20)

class AppController:
    def __init__(self):

        self.view = CompositeView()
        self.view.add(RGBView())
        self.view.add(SerialConsoleView())
        #self.view.add(pybytesView(pybytes))

        self.pm = PymeshAdapter(self.view, self.messageCallback)

    def run(self):
        #Want to run the loop in a separate thread to make sure we can interract with the app on this one
        _thread.start_new_thread(mainLoopInThread, (self, self))

    def messageCallback(self, rcv_ip, rcv_dat):
        message = rcv_dat.decode('utf-8')
        print("Callback from %s: %s" %
            (rcv_ip, message))

    def sendToAll(self, content):
        ips = self.pm.getAllIPs()
        for ip in ips:
            self.pm.sendMessage(ip, content)
