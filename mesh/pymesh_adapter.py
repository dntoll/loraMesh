
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
        this = self

        
        self.view = view
        self.messageCallback = messageCallback
        self.lora = LoRa(mode=LoRa.LORA, tx_iq=True, region=LoRa.EU868)

        self.rawMac = self.lora.mac()[7]

        lora_sock = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
        lora_sock.setblocking(True)

        print("Starting threads")
        self.socketThread = _thread.start_new_thread(PymeshAdapter._sendAndListen, (self, lora_sock))


    def _sendAndListen(this, lora_sock):
        chrono = Timer.Chrono()
        chrono.start()
        
        print("Start listening")
        while (True):

            # send some data
            lora_sock.setblocking(True)
            lora_sock.send('Hello')

            # get any data received...
            lora_sock.setblocking(False)
            data = lora_sock.recv(64)
            print(data)

            # wait a random amount of time
            time.sleep(machine.rng() & 0x0F)
            #print(str(chrono.read()))

            """if chrono.read() > 5:
                chrono.stop()
                content = bytes("Ping",'UTF-8')
                m = Message(this.rawMac, 0, 1, content)
                lora_sock.setblocking(True)
                lora_sock.send(m.getBytes())
                this.view.sendMessage(0,m.getBytes())
                lora_sock.setblocking(False)
                chrono.reset()
                chrono.start()

            lora_sock.setblocking(False)
            buffer = lora_sock.recv(64)
            if len(buffer) > 0:
                print("recv")
                print('Received {}'.format(buffer))
                this.view.receiveMessage(0,bytes())"""

        
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

