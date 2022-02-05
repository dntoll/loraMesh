

    

class Router:

    def __init__(self):
        self.neighbors = set()

    def deriveRouterData(self, message, receivedLoraStats):

        #receivedLoraStats from lora.stats() https://docs.pycom.io/firmwareapi/pycom/network/lora/
        self.neighbors.add(message.senderMac)


    def getRoute(self, senderMac):
        route = bytearray(1)
        route[0] = senderMac
        return route