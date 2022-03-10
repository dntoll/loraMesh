import time
import sys
import struct
from meshlibrary.Message import Message

from meshlibrary.MeshController import MeshController
from meshlibrary.ReceiveBuffer import ReceiveBuffer
from meshlibrary.Route import Route
from meshlibrary.timers import *

class PymeshAdapter:
    

    def __init__(self, view, socket, pycomInterface, callback):
        self.view = view
        self.socket = socket

        self.receiveBuffer = ReceiveBuffer()
        self.meshController = MeshController(view, self.getMyAddress(), pycomInterface, callback)
        self.meshControllerLock = pycomInterface.allocate_lock()
        self.listenThread = pycomInterface.start_new_thread(PymeshAdapter._listen, (self, socket, pycomInterface))
        self.socketThread = pycomInterface.start_new_thread(PymeshAdapter._sendThread, (self, socket, pycomInterface))

    
    def getMessagesInSendQue(self):
        self.meshControllerLock.acquire(1)
        m = self.meshController.getSendQue().getSendQue()
        self.meshControllerLock.release()
        return m

    def getKnownNodes(self):
        self.meshControllerLock.acquire(1)
        m = self.meshController.router.getKnownNodes()
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
            queItem = this.meshController.getSendQue().getQueItemToSend()
            this.meshController.getSendQue().removeOld()
            this.meshControllerLock.release()

            #transform mes to fin if sendcount is high


            if queItem is not None:
                lora_sock.send(queItem.message.getBytes())
                this.view.sendMessage(queItem.message)

            pycomInterface.sleep_ms(pycomInterface.rng() % MAX_SLEEP_AFTER_SEND)

    def _listen(this, lora_sock, pycomInterface):
        while (True):

            # get any data received...
            data, loraStats = lora_sock.receive()
            this.processReceivedBytes(data, loraStats)
            
            #Maybe we can make this blocking instead...
            pycomInterface.sleep_ms(SLEEP_AFTER_RECEIVE)


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
