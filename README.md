
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

secrets.py
```python
# wifi-credentials
ssid = 'SSID' #ssid for Wifi used for OTA using the release_push.py
pwa = 'wifipassword' #wifi-passord used OTA using the release_push.py
# telnet and ftp-credentials
userName = 'micro'
passwd = 'python'
# list of clients to update using OTA
clients = ["192.168.1.138", "192.168.1.253", "192.168.1.48", "192.168.1.15"]
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