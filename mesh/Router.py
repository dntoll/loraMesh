

    

class Router:

    def __init__(self):
        self.neighbors = set()

    def deriveRouterData(self, message, receivedLoraStats):

        #receivedLoraStats from lora.stats() https://docs.pycom.io/firmwareapi/pycom/network/lora/
        self.neighbors.add(message.senderMac)


    def getRoute(self, fromMac, toMac):
        route = bytearray(2)
        route[0] = fromMac
        route[1] = toMac
        return route