import time
import _thread

from meshlibrary.MeshFacade import MeshFacade


from view.CompositeView import CompositeView
from view.RGBView import RGBView
from view.SerialConsoleView import SerialConsoleView


        

class MeshTestConsole:
    def __init__(self):

        self.view = CompositeView()
        #self.view.add(RGBView())
        self.view.add(SerialConsoleView())
        
        self.mf = MeshFacade(self.view, MeshTestConsole.callback)

    def callback():
        return

    def run(self):
        #Want to run the loop in a separate thread to make sure we can interract with the app on this one
        _thread.start_new_thread(MeshTestConsole.mainLoopInThread, (self, self))

    def mainLoopInThread(this, that):
        while True:
            this.view.update(this.mf.pma) #not superhappy about this instead the facade should offer an interface for this
            time.sleep(1)
    
    def n(self):
        print(self.mf.getKnownNodes)

    def p(self):
        self.mf.sendMessage(52, b"Ping")

    def rp(self):
        m = Message(54, Route(bytes((54,102, 101))), Message.TYPE_MESSAGE, b"Routethis")
        self.mf.meshController.addToQue(m)
