
from machine import Timer
import time
import sys
import socket
import struct
import machine
import _thread
from network import LoRa
import ubinascii, network
from mesh.Message import Message
from mesh.Message import ToShortMessageException
from mesh.MeshController import MeshController

class PymeshAdapter:
    BUFFER_SIZE = 256

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


        self.macOneByte = ubinascii.hexlify(lora.mac())[0]

        self.savedBuffer = bytearray()
        self.meshController = MeshController(messageCallback, self.getMyAddress())

        print("Starting threads")
        self.socketLock = _thread.allocate_lock()
        self.meshControllerLock = _thread.allocate_lock()
        self.listenThread = _thread.start_new_thread(PymeshAdapter._listen, (self, lora_sock))
        self.socketThread = _thread.start_new_thread(PymeshAdapter._sendThread, (self, lora_sock))



    def _sendThread(this, lora_sock):
        print("Start sending")

        #m =
        while (True):
            this.meshControllerLock.acquire(1)
            m = this.meshController.getMessage()
            this.meshControllerLock.release()

            if m is not None:
                print("Sending...")
                # send some data
                this.socketLock.acquire(1)
                lora_sock.setblocking(True)
                lora_sock.send(m.getBytes())
                this.socketLock.release()

            time.sleep(machine.rng() & 0x0F)

    def _listen(this, lora_sock):
        print("Start listening")
        while (True):

            # get any data received...
            this.socketLock.acquire(1)
            lora_sock.setblocking(False)
            data = lora_sock.recv(PymeshAdapter.BUFFER_SIZE)
            this.socketLock.release()

            this.processReceivedBytes(data)

            # wait a random amount of time
            time.sleep(1)


    #This is run by the receiver thread...
    def processReceivedBytes(self, receivedBytes):
        newBuffer = bytearray(len(self.savedBuffer) + len(receivedBytes))
        newBuffer[0:len(self.savedBuffer)] = self.savedBuffer
        newBuffer[len(self.savedBuffer):] = receivedBytes

        while(len(newBuffer) > 0):
            try:
                bytesEaten, m = Message.fromBytes(newBuffer)
                if bytesEaten > 0:
                    print(m.contentBytes.decode("utf-8"))
                    newBuffer = newBuffer[bytesEaten:]

                    self.meshControllerLock.acquire(1)
                    self.meshController.onReceive(m)
                    self.meshControllerLock.release()
            except ToShortMessageException:
                print("not full message received")
                break
            except Exception as err:
                print("Exception {0}".format(err) + str(newBuffer))
                newBuffer = newBuffer[1:]

        self.savedBuffer = bytearray(len(newBuffer))
        self.savedBuffer[0:] = newBuffer

    def getMyAddress(self):
        #https://github.com/pycom/pycom-libraries/blob/master/pymesh/pymesh_frozen/lib/loramesh.py#L153

        #Note we go beyond the mesh_interface we should use to get this one
        return self.macOneByte

    def update(self):
        return

    def sendMessage(self, target_ip, message):
        m = Message(this.getMyAddress(), target_ip, Message.TYPE_MESSAGE, message)
        self.meshControllerLock.acquire(1)
        self.meshController.append(m)
        self.meshControllerLock.release()

        self.view.sendMessage(target_ip, message)


    def getAllIPs(self):
        self.meshControllerLock.acquire(1)
        neighbors = self.meshController.getKnownNeighbors()
        self.meshControllerLock.release()
        return neighbors

    def new_message_cb(rcv_ip, rcv_port, rcv_data):
        global globalView
        global this

        this.numMessages += 1
        globalView.receiveMessage(rcv_ip, rcv_data)
        this.messageCallback(rcv_ip, rcv_data)
