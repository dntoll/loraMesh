

PymeshAdapter is too hard to read due to locks... 

We also need better console view

# SendQue -> hålla reda på vilka meddelanden som är skickade och vilka som är accade
meddelande läggs till när vi vill skicka ett meddelande.
Det ligger kvar i sändkön tills acc kommer
Ett meddelande kan skickas flera gånger tills en acc kommer
Om ingen route finns kanske vi skickar ett sök-meddelande först?

# Receive Que -> hålla reda på mottagna meddelanden
Se till att vi accar dem? 
Dubbletter av meddelanden försvinner

# Routes
Derive routes from messages
Get best route
Ask for unknown routes

# Route message

# Console View
MyMac
Neighbors and routes known
Received Messages
Sent Messages and their que + acc status