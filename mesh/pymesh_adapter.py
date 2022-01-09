
import time

try:
    from pymesh_config import PymeshConfig
except:
    from _pymesh_config import PymeshConfig

try:
    from pymesh import Pymesh
except:
    from _pymesh import Pymesh

globalView = None

class PymeshAdapter:

    def __init__(self, pybytes, view, pyMeshDebugLevel):
        global globalView
        globalView = view
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
        

        return self.pymesh.mesh.mesh.mesh.mac_short
    
    def isPartOfANetwork(self):
        return self.pymesh.is_connected()

    def printDebug(self):
        print("Mac ")
        print(self.pymesh.mac());
        print("Status_str")
        print(self.pymesh.status_str())
        print("All ips")
        print(self.getAllIPs())
        print("ip_eid")
        print(self.pymesh.mesh.mesh.mesh.ip_eid)
        print("pairs:")
        mesh_pairs = self.pymesh.mesh.mesh.get_mesh_pairs()
        print('last_mesh_pairs', mesh_pairs)
    
    def update(self):
        if not self.pymesh.is_connected():
            self.view.notConnected(self.pymesh.status_str())
        else:
            self.view.isConnected(self.getMyAddress(), self.getAllIPs())

    def sendMessage(self, target_ip, message):
        self.view.sendMessage(target_ip, message)
        self.pymesh.send_mess(target_ip, message)

    def getAllIPs(self):
        ipsIncludingMine = self.pymesh.mesh.get_mesh_mac_list()
        
        if len(ipsIncludingMine) > 0:
            ipsIncludingMine = ipsIncludingMine[0]
            
            #Remove all my addresses
            ips = [] #self.pymesh.mesh.mesh.mesh.mesh.ipaddr()
            ips.append(self.pymesh.mesh.mesh.mesh.mac_short)
            
            for ip in ips:            
                #print(ip)
                if ip in ipsIncludingMine:
                    ipsIncludingMine.remove(ip)
            return ipsIncludingMine
        return []
        

    def new_message_cb(rcv_ip, rcv_port, rcv_data):
        global globalView
        globalView.receiveMessage(rcv_ip, rcv_data)

