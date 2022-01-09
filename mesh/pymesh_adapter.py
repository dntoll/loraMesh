
import time
import machine

try:
    from pymesh_config import PymeshConfig
except:
    from _pymesh_config import PymeshConfig

try:
    from pymesh import Pymesh
except:
    from _pymesh import Pymesh

globalView = None
this = None

class PymeshAdapter:

    def __init__(self, pybytes, view, pyMeshDebugLevel):
        global globalView
        global this
        globalView = view
        this = self

        self.numMessages = 0;
        
        self.view = view
        
        # read config file, or set default values
        pymesh_config = PymeshConfig.read_config()
        #initialize Pymesh
        self.pymesh = pybytes.__pymesh.__pymesh
        self.pymesh.mesh.mesh.message_cb = PymeshAdapter.new_message_cb
        
        self.pymesh.debug_level(pyMeshDebugLevel)
        view.donePymeshInit(self.getMyAddress())
        
    def getMyAddress(self):
        #https://github.com/pycom/pycom-libraries/blob/master/pymesh/pymesh_frozen/lib/loramesh.py#L153
        
        #Note we go beyond the mesh_interface we should use to get this one
        return self.pymesh.mesh.mesh.mesh.mac_short
    
    def isPartOfANetwork(self):
        return self.pymesh.is_connected()


    def stateToString(self, state):
        return {
            0: "STATE_DISABLED",
            1: "STATE_DETACHED",
            2: "STATE_CHILD",
            3: "STATE_ROUTER",
            4: "STATE_LEADER",
            5: "STATE_LEADER_SINGLE" }[state]
        return "STATE_UNKNOWN"

    def printDebug(self):
        print("Role:" + self.stateToString(self.pymesh.mesh.mesh.mesh.mesh.state()))
        print("Mac:")
        print(self.pymesh.mac());
        print("Status_str:")
        print(self.pymesh.status_str())
        print("All ips:")
        print(self.getAllIPs())
        print("ip_eid:")
        print(self.pymesh.mesh.mesh.mesh.ip_eid)
        print("pairs:")
        mesh_pairs = self.pymesh.mesh.get_mesh_pairs()
        print('last_mesh_pairs', mesh_pairs)
        print("Buffer info:", self.pymesh.mesh.mesh.mesh.mesh.cli("bufferinfo"))
    
    def update(self):
        if not self.pymesh.is_connected():
            self.view.notConnected(self.pymesh.status_str())
        else:
            self.view.isConnected(self.getMyAddress(), self.getAllIPs())

        #Too many messages sent and received... must reboot
        
        """print(self.numMessages)"""
        if self.numMessages > 90:
            print("too many messages sent, reset")
            self.numMessages = 0
            machine.reset()
            #this did not work either
            """self.pymesh.pause()
            self.pymesh.resume()"""


    def sendMessage(self, target_ip, message):
        self.view.sendMessage(target_ip, message)
        self.pymesh.send_mess(target_ip, message)

        self.numMessages += 1
        ##We seem to eat up memory, perhaps the socket needs closing at differnt points...
        #hm did not seem to make any difference... 
        #self.pymesh.mesh.mesh.sock.close()
        #self.pymesh.mesh.mesh.create_socket()

    def getAllIPs(self):
        ipsIncludingMine = self.pymesh.mesh.get_mesh_mac_list()
        
        if len(ipsIncludingMine) > 0:
            excludingMine = ipsIncludingMine[0]
            if self.getMyAddress() in excludingMine:
                excludingMine.remove(self.getMyAddress())
            return excludingMine
        return []
        

    def new_message_cb(rcv_ip, rcv_port, rcv_data):
        global globalView
        global this

        this.numMessages += 1

        globalView.receiveMessage(rcv_ip, rcv_data)

