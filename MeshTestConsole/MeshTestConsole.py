import time
import _thread

       

class MeshTestConsole:
    def __init__(self, meshFacade, view, pycomInterface):

        self.view = view
        self.meshFacade = meshFacade
        self.pycomInterface = pycomInterface

    def callback():
        return

    def run(self):

        
        #Want to run the loop in a separate thread to make sure we can interract with the app on this one
        self.pycomInterface.start_new_thread(MeshTestConsole.mainLoopInThread, (self, self))

    def mainLoopInThread(this, that):
        while True:
            this.view.update(this.meshFacade.pma) #not superhappy about this instead the facade should offer an interface for this
            this.pycomInterface.sleep_ms(1000)
    
    def n(self):
        print(self.meshFacade.getKnownNodes())

    def p(self):
        self.meshFacade.sendMessage(52, b"Ping")

    def rp(self):
        m = Message(54, Route(bytes((54,102, 101))), Message.TYPE_MESSAGE, b"Routethis")
        self.meshFacade.meshController.addToQue(m)
