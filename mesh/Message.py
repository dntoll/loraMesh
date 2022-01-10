

class Message:
    def __init__(self, senderMac, receiverMac, messageType, contentBytes):
        self.senderMac = senderMac;
        self.receiverMac = receiverMac;
        self.messageType = messageType;
        self.contentBytes = contentBytes;
        return

    def getBytes(self):
        ret = bytearray(3+len(self.contentBytes))
        ret[0:2] = [self.senderMac, self.receiverMac, self.messageType]
        ret[3:] = self.contentBytes
        return bytes(ret)