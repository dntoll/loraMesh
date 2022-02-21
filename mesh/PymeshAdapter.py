import time
import sys
import struct
from mesh.Message import Message

from mesh.MeshController import MeshController
from mesh.ReceiveBuffer import ReceiveBuffer
from mesh.Route import Route

class PymeshAdapter:
    

    def __init__(self, view, socket, pycomInterface):
        self.view = view
        self.socket = socket

        self.receiveBuffer = ReceiveBuffer()
        self.meshController = MeshController(view, self.getMyAddress(), pycomInterface)
        self.meshControllerLock = pycomInterface.allocate_lock()
        self.listenThread = pycomInterface.start_new_thread(PymeshAdapter._listen, (self, socket, pycomInterface))
        self.socketThread = pycomInterface.start_new_thread(PymeshAdapter._sendThread, (self, socket, pycomInterface))

    
    def getMessagesInSendQue(self):
        self.meshControllerLock.acquire(1)
        m = self.meshController.getSendQue().getSendQue()
        self.meshControllerLock.release()
        return m

    def getNeighbors(self):
        self.meshControllerLock.acquire(1)
        m = self.meshController.router.getNeighbors()
        self.meshControllerLock.release()
        return m
    
    def getRoutes(self):
        self.meshControllerLock.acquire(1)
        m = self.meshController.router.getRoutes()
        self.meshControllerLock.release()
        return m


    def _sendThread(this, lora_sock, pycomInterface):
        while (True):
            this.meshControllerLock.acquire(1)
            m = this.meshController.getSendQue().getMessageToSend()
            this.meshControllerLock.release()

            if m is not None:
                lora_sock.send(m.getBytes())
                this.view.sendMessage(m)

            pycomInterface.sleep_ms(pycomInterface.rng() % 10)

    def _listen(this, lora_sock, pycomInterface):
        while (True):

            # get any data received...
            data, loraStats = lora_sock.receive()
            this.processReceivedBytes(data, loraStats)
            # wait one second
            pycomInterface.sleep_ms(5)


    #This is run by the receiver thread...
    def processReceivedBytes(self, receivedBytes, loraStats):
        messages = self.receiveBuffer.getMessages(receivedBytes)

        if len(messages) > 0:
            self.meshControllerLock.acquire(1)
            for m in messages:
                self.meshController.onReceive(m, loraStats)
            self.meshControllerLock.release()

        self.view.receiveMessages(messages)                

    def getMyAddress(self):
        return self.socket.getMac()

    def sendMessage(self, target_ip, message):
        self.meshControllerLock.acquire(1)

        if self.meshController.router.hasRoute(self.getMyAddress(), target_ip):
            route = self.meshController.router.getRoute(self.getMyAddress(), target_ip)
            m = Message(self.getMyAddress(), route, Message.TYPE_MESSAGE, message)
        else:
            route = Route(bytes([self.getMyAddress(), target_ip]))
            m = Message(self.getMyAddress(), route, Message.TYPE_FIND, message)
        self.meshController.addToQue(m)

        self.meshControllerLock.release()

        


    def getAllIPs(self):
        self.meshControllerLock.acquire(1)
        neighbors = self.meshController.getKnownNeighbors()
        self.meshControllerLock.release()
        return neighbors
