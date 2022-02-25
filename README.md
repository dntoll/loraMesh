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
 * When nodes disappear, the mesh re-routes (NOT IMPLEMENTED)

Non-functional requirements
 * Reduce resources (power, lora usage, CPU etc)
 * Nodes relay messages efficently (Routing and search strategy)
 * API is documentated, code is self-explanatory
 * Relies on automated testing techniques

### Contribution
This project is free to use according to MIT Licence.

## Usage

### Projects
Right now there are a couple of different projects in the same folder, that are not well divided
 * Mesh-library

We would like a bash interface of shellscripts to run the common tasks
 * clean.sh - remove python cache files
 * test.sh - run tests


### Install
We recommend Visual Studio Code 

To run scripts as well as test the app
```bash 
sudo apt-get install python3
pip install -U pytest
``` 
### Update using Visual Studio Code and pymakr plugin
To update a single Node connected to the computer through USB we use the pymakr plugin by pycom.
https://pycom.io/products/supported-networks/pymakr/

Depending on the "Global settings" ("auto_connect": true) and pymakr.conf ("address": "COM7",) you get access to the Node through REPL. 

Right now a secrets.py is needed to run the code in main.py, see below

### OTA update
To update more than one node, the current strategy for OTA is to update nodes through FTP and then reset them through Telnet.

The current release_push.py does have the following problems
 * Very insecure!!! FTP with open password! Also each node has WiFi credentials and knows all IPs of all other nodes
 * TODO: use key-storage
 * Does not remove files, only overwrites old files and uploads new files
 * May upload files not intended...

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


# Evaluation

Evaluation of the project consist of:
 * MeshTestConsole.py - Set up a physical mesh network on actual LoPy4 nodes on the same WiFI network. This should both 
 * Automated unit-tests - Classes can have these, right now these should be added or moved into a test folder and run on PC via pytest instead of on actual devices
 * Automated simulated mesh-network tests -  these are written as unit test and run via pytest
 * Large-simulations of mesh-network with performance metrics as well as visualisations


Build Process

### Test strategy

```bash
python3 -m pytest
```

### Simulations

### Benchmarks


# TODO
 * Explore new more secure versions of OTA-update
 * Receive Que -> hålla reda på mottagna meddelanden
 * Routes - Favor best route
 * Route message
 * Console View
   * Sent Messages and their que + acc status
 * Plotting https://networkx.org/documentation/stable/reference/drawing.html?highlight=visualize
 * CI/CD 