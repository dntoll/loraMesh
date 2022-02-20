import time
import _thread

from mesh.PymeshAdapter import PymeshAdapter
from mesh.ThreadSafeLoraSocket import ThreadSafeLoraSocket
from mesh.PycomInterface import PycomInterface

from view.CompositeView import CompositeView
from view.RGBView import RGBView
from view.SerialConsoleView import SerialConsoleView


        

class AppController:
    def __init__(self):

        self.view = CompositeView()
        self.view.add(RGBView())
        self.view.add(SerialConsoleView())
        
        self.pm = PymeshAdapter(self.view, ThreadSafeLoraSocket(), PycomInterface())

    def run(self):
        #Want to run the loop in a separate thread to make sure we can interract with the app on this one
        _thread.start_new_thread(AppController.mainLoopInThread, (self, self))

    def mainLoopInThread(this, that):
        while True:
            this.view.update(this.pm)
            time.sleep(1)
