
#from CircularBuffer import CircularBuffer

class Value:

    def __init__(self):
        self.value = 0
        self.total = 0
        self.min = None
        self.max = None
        self.numValues = 0
        #self.buffer = CircularBuffer(10)

    def getAverage(self):
        return self.total / self.numValues
    
    def set(self, value):
        self.value = value
        #self.buffer.add(value)
        self.total += value
        self.numValues += 1
        if self.min == None or self.min > value:
            self.min = value
        if self.max == None or self.max < value:
            self.max = value