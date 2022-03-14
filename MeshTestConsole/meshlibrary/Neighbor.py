class Neighbor:
    def __init__(self, mac, rssi, time):
        self.mac = mac
        self.rssi = rssi
        self.time = time
        self.nodesBeyondSet = set()

    def addNodesBeyond(self, route):
        for r in route.getBytes():
            self.nodesBeyondSet.add(r)

        #print(self.nodesBeyondSet)