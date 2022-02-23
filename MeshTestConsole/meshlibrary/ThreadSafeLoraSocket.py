
import _thread
import socket
import ubinascii, network
from network import LoRa
from meshlibrary.ReceiveBuffer import ReceiveBuffer

class ThreadSafeLoraSocket:
    def __init__(self):
        self.socketLock = _thread.allocate_lock()
        self.lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868)
        self.lora_sock = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
        self.lora_sock.setblocking(True)


    def send(self, bytes):
        self.socketLock.acquire(1)
        self.lora_sock.setblocking(True)
        self.lora_sock.send(bytes)
        self.socketLock.release()

    def receive(self):
        self.socketLock.acquire(1)
        self.lora_sock.setblocking(False)
        data = self.lora_sock.recv(ReceiveBuffer.BUFFER_SIZE)
        loraStats = self.lora.stats()
        self.socketLock.release()

        return (data, loraStats)

    def getMac(self):
        return ubinascii.hexlify(self.lora.mac())[15]