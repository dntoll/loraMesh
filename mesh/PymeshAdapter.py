
from machine import Timer
import time
import sys
import struct
import machine
import _thread
from mesh.Message import Message

from mesh.MeshController import MeshController
from mesh.ReceiveBuffer import ReceiveBuffer

class PymeshAdapter:
    

    def __init__(self, view, socket):
        self.view = view
        self.socket = socket

        self.receiveBuffer = ReceiveBuffer()
        self.meshController = MeshController(view, self.getMyAddress())
        self.meshControllerLock = _thread.allocate_lock()
        

        print("Starting threads on " + str(self.getMyAddress()))
        self.listenThread = _thread.start_new_thread(PymeshAdapter._listen, (self, socket))
        self.socketThread = _thread.start_new_thread(PymeshAdapter._sendThread, (self, socket))

    def getMessagesInSendQue(self):
        self.meshControllerLock.acquire(1)
        m = self.meshController.getMessagesInSendQue()
        self.meshControllerLock.release()

        return m


    def _sendThread(this, lora_sock):
        print("Start sending")

        #m =
        while (True):
            this.meshControllerLock.acquire(1)
            m = this.meshController.getMessage()
            this.meshControllerLock.release()

            if m is not None:
                lora_sock.send(m.getBytes())
                this.view.sendMessage(m)

            time.sleep(machine.rng() & 0x0F)

    def _listen(this, lora_sock):
        print("Start listening")
        while (True):

            # get any data received...
            data, loraStats = lora_sock.receive()

            this.processReceivedBytes(data, loraStats)

            # wait a random amount of time
            time.sleep(1)


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

        route = self.meshController.router.getRoute(self.getMyAddress(), target_ip)
        m = Message(self.getMyAddress(), route, Message.TYPE_MESSAGE, message)
        self.meshController.append(m)

        self.meshControllerLock.release()

        


    def getAllIPs(self):
        self.meshControllerLock.acquire(1)
        neighbors = self.meshController.getKnownNeighbors()
        self.meshControllerLock.release()
        return neighbors
