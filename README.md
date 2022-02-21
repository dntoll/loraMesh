
# Project description and vision

Lora Mesh is a application layer lora mesh library that enables pycom LoPy4 units to send messages that gets routed.

LoPy4 (Sender) <-> Mesh network of LoPy4 <-> LoPy4 (Receiver)

## Project goals

Node - (Sender, Receiver)
Message - (Find, Message, ACC)

Functional requirements
 * All Nodes get their own mesh-network Adress
 * Sender send Message to Receiver through the mesh using the Receiver Adress
 * Sender receive ACC-Message when Receiver has received the Message
 * Nodes re-send Message up until timeout
 * Sender gets notified if Receiver cannot be found within timeout

Non-functional requirements
 * Reduce resources (power, lora usage, CPU etc)
 * Nodes relay messages efficently (Routing and search strategy)
 * API is documentated, code is self-explanatory
 * Relies on automated testing techniques

### Contribution

## Usage

### Update using Visual Studio Code and pymakr plugin
To update a single Node connected to the computer through USB we use the pymakr plugin by pycom.
https://pycom.io/products/supported-networks/pymakr/

Depending on the "Global settings" ("auto_connect": true) and pymakr.conf ("address": "COM7",) you get access to the Node through REPL. 

Right now a secrets.py is needed to run the code in main.py, see below

### OTA update
To update more than one node, the current strategy for OTA is to run the 



Add a secrets.py file with credentials for OTA-updates
secrets.py
```python
# wifi-credentials
ssid = 'SSID' #ssid for Wifi used for OTA using the release_push.py
pwa = 'wifipassword' #wifi-passord used OTA using the release_push.py
# telnet and ftp-credentials
userName = 'micro'
passwd = 'python'
# list of clients to update using OTA this one is used in the release_push.py
clients = ["192.168.1.138", "192.168.1.253", "192.168.1.48", "192.168.1.15"]
```

When all nodes have secrets.py and you have a list of wifi-ip-adresses of all nodes then you can run:
```bash
python release_push.py
```


## Evaluation

### Test strategy

### Simulations

### Benchmarks


# TODO
 * Receive Que -> hålla reda på mottagna meddelanden
 * Routes - Favor best route
 * Route message
 * Console View
   * Sent Messages and their que + acc status
 * Plotting https://networkx.org/documentation/stable/reference/drawing.html?highlight=visualize