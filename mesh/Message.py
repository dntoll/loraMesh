

class Message:
    def __init__(self, senderMac, receiverMac, messageType, contentBytes):
        self.senderMac = senderMac
        self.receiverMac = receiverMac
        self.messageType = messageType
        self.contentBytes = contentBytes
        return

    def getBytes(self):
        ret = bytearray(3+len(self.contentBytes))
        ret[0:2] = bytes((self.senderMac, self.receiverMac, self.messageType))
        ret[3:] = self.contentBytes
        return bytes(ret)
    
    def fromBytes(bytes):
        senderMac = bytes[0]
        receiverMac = bytes[1]
        messageType = bytes[2]
        contentBytes = bytes[3:]

        return Message(senderMac, receiverMac, messageType, contentBytes)

    def test():
        contentBytes = bytes((4,5,6))
        m = Message(1,2,3,contentBytes)

        byteMessage = m.getBytes()

        r = Message.fromBytes(byteMessage)

        assert(r.senderMac == m.senderMac)
        assert(r.receiverMac == m.receiverMac)
        assert(r.messageType == m.messageType)
        assert(r.contentBytes[0] == m.contentBytes[0] and r.contentBytes[1] == m.contentBytes[1] and r.contentBytes[2] == m.contentBytes[2]) #<- ? comparison?