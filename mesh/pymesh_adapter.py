
import time
import sys
import socket
import struct
import _thread
from network import LoRa
from mesh import Message

class PymeshAdapter:
    ping = 1

    def __init__(self, pybytes, view, pyMeshDebugLevel, messageCallback):
        global globalView
        global this
        globalView = view
        this = self

        
        self.view = view
        self.messageCallback = messageCallback
        self.lora = LoRa(mode=LoRa.LORA, tx_iq=True, region=LoRa.EU868)

        self.rawMac = self.lora.mac()[7]

        lora_sock = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
        lora_sock.setblocking(True)

        print("Starting threads")
        self.listenThread = _thread.start_new_thread(PymeshAdapter.listen, (self, lora_sock))
        self.sendThread = _thread.start_new_thread(PymeshAdapter.connect, (self, lora_sock))


    def connect(this, lora_sock):
        i = 0
        while True:
            m = Message(this.rawMac, this.ping, "Ping")
            lora_sock.send(m.getBytes())
            print('Sent {}'.format(m.getBytes()))
            i= i+1
            time.sleep(5)

    def listen(this, lora_sock):
        i = 0
        while (True):
            if lora_sock.recv(64) == b'Ping':
                lora_sock.send('Pong')
                print('Pong {}'.format(i))
                i = i+1
            time.sleep(5)

        
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

