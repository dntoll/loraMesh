import time
import _thread

       

class MeshTestConsole:
    def __init__(self, view, hardwareInterface, meshFacade):
        self.view = view
        self.hardwareInterface = hardwareInterface
        self.meshFacade = meshFacade

    def callback(originIP, contentBytes):
        print("Received: " + contentBytes.decode("utf-8") + " from " + str(originIP))
        return

    def run(self):

        
        #Want to run the loop in a separate thread to make sure we can interract with the app on this one
        self.hardwareInterface.start_new_thread(MeshTestConsole.mainLoopInThread, (self, self))

    def mainLoopInThread(this, that):
        while True:
            this.view.update(this.meshFacade) #not superhappy about this instead the facade should offer an interface for this
            this.hardwareInterface.sleep_ms(1000)
            
    
    def n(self):
        print(self.meshFacade.getKnownNodes())

    def p(self):
        self.meshFacade.sendMessage(52, b"Ping")

    def rp(self):
        m = Message(54, Route(bytes((54,102, 101))), Message.TYPE_MESSAGE, b"Routethis")
        self.meshFacade.meshController.addToQue(m)
