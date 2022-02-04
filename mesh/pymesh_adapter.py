
from machine import Timer
import time
import sys
import socket
import struct
import machine
import _thread
from network import LoRa

from mesh.Message import Message

class PymeshAdapter:
    ping = 1

    def __init__(self, view, messageCallback):
        global globalView
        global this
        globalView = view
        self.view = view
        this = self

        self.messageCallback = messageCallback
        
        lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868)
        lora_sock = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
        lora_sock.setblocking(True)

        print("Starting threads")
        self.socketLock = _thread.allocate_lock()
        self.listenThread = _thread.start_new_thread(PymeshAdapter._listen, (self, lora_sock))
        self.socketThread = _thread.start_new_thread(PymeshAdapter._sendThread, (self, lora_sock))


    def _listen(this, lora_sock):
        print("Start listening")
        while (True):

            # get any data received...
            this.socketLock.acquire(1)
            lora_sock.setblocking(False)
            data = lora_sock.recv(64)
            this.socketLock.release()
            this.process(data)

            # wait a random amount of time
            time.sleep(1)

    def _sendThread(this, lora_sock):
        print("Start sending")

        m = Message(1, 2, 0, bytes("Ping", 'utf-8'))
        while (True):
            # send some data
            this.socketLock.acquire(1)
            lora_sock.setblocking(True)
            lora_sock.send(m.getBytes())
            this.socketLock.release()

            time.sleep(machine.rng() & 0x0F)


    def process(self, receivedBytes):
        try:
            bytesEaten, m = Message.fromBytes(receivedBytes)
            if bytesEaten > 0:
                print(m.contentBytes)
        except:
            print("not a message")

        
    def getMyAddress(self):
        #https://github.com/pycom/pycom-libraries/blob/master/pymesh/pymesh_frozen/lib/loramesh.py#L153
        
        #Note we go beyond the mesh_interface we should use to get this one
        return 1
    
    def isPartOfANetwork(self):
        return False


    def stateToString(self, state):
        return {
            0: "STATE_DISABLED",
            1: "STATE_DETACHED",
            2: "STATE_CHILD",
            3: "STATE_ROUTER",
            4: "STATE_LEADER",
            5: "STATE_LEADER_SINGLE" }[state]
        return "STATE_UNKNOWN"

    def printDebug(self):
        return
    
    def update(self):
        return


    def sendMessage(self, target_ip, message):
        self.view.sendMessage(target_ip, message)
        

    def getAllIPs(self):
       
        return []
        

    def new_message_cb(rcv_ip, rcv_port, rcv_data):
        global globalView
        global this

        this.numMessages += 1

        globalView.receiveMessage(rcv_ip, rcv_data)

        this.messageCallback(rcv_ip, rcv_data)

