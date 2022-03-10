
from meshlibrary.Message import ToShortMessageException
from meshlibrary.Message import NotAMessageException
from meshlibrary.Message import Message

class ReceiveBuffer:
    BUFFER_SIZE = 256

    def __init__(self):
        self.savedBuffer = bytearray()

    #This is run by the receiver thread...
    def getMessages(self, receivedBytes):

        ret = []
        newBuffer = bytearray(len(self.savedBuffer) + len(receivedBytes))
        newBuffer[0:len(self.savedBuffer)] = self.savedBuffer
        newBuffer[len(self.savedBuffer):] = receivedBytes

        while(len(newBuffer) > 0):
            try:
                bytesEaten, m = Message.fromBytes(newBuffer)
                
                if bytesEaten > 0:
                    newBuffer = newBuffer[bytesEaten:]
                    
                    ret.append(m)
            except ToShortMessageException:
                print("not full message received")
                newBuffer = newBuffer[1:]
                break
            except NotAMessageException:
                #print("not a message")
                newBuffer = newBuffer[1:]
                break
            except Exception as err:
                print("Exception in getBytes")
                print(err)
                #print("Reducing received buffer -- {0}".format(err) + str(newBuffer))
                newBuffer = newBuffer[1:]

        self.savedBuffer = bytearray(len(newBuffer))
        self.savedBuffer[0:] = newBuffer
        return ret