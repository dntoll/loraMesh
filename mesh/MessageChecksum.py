

class MessageChecksum:

    def __init__(self, bytes):
        self.checksum = bytes

    def isSame(self, other):
        return self.checksum[0] == other.checksum[0] and self.checksum[1] == other.checksum[1] and self.checksum[2] == other.checksum[2]

    def toBytes(self):
        return self.checksum
    
    def fromMessage(message):
        target = message.route.getTarget()
        origin = message.route.getOrigin()
        contentBytes = message.contentBytes
        sum = 0

        for b in contentBytes:
            sum += int(b)
        
        return MessageChecksum(bytes((target, origin, sum % 255)))