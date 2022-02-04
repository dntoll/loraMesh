

class Message:
    def __init__(self, senderMac, receiverMac, messageType, contentBytes):
        self.senderMac = senderMac
        self.receiverMac = receiverMac
        self.messageType = messageType
        self.contentBytes = contentBytes
        return

    def getBytes(self):
        ret = bytearray(3+len(self.contentBytes))
        ret[0:3] = bytes((self.senderMac, self.receiverMac, self.messageType, len(self.contentBytes)))
        ret[4:] = self.contentBytes
        return bytes(ret)
    
    def fromBytes(bytes):
        if len(bytes) < 4:
            return (0, None)

        senderMac = bytes[0]
        receiverMac = bytes[1]
        messageType = bytes[2]
        contentLength = bytes[3]

        if len(bytes) < 4 + contentLength:
            return (0, None) #not enough data in buffer


        contentBytes = bytes[4:4+contentLength]

        return (4+contentLength, Message(senderMac, receiverMac, messageType, contentBytes))

    def test():
        contentBytes = bytes((4,5,6))
        m = Message(1,2,3,contentBytes)

        byteMessage = m.getBytes()

        cl, r = Message.fromBytes(byteMessage)

        assert(cl == 4+3)
        assert(r.senderMac == m.senderMac)
        assert(r.receiverMac == m.receiverMac)
        assert(r.messageType == m.messageType)
        assert(r.contentBytes[0] == m.contentBytes[0] and r.contentBytes[1] == m.contentBytes[1] and r.contentBytes[2] == m.contentBytes[2]) #<- ? comparison?