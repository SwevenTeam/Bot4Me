from StatementStato import StatementStato
from Stato import Stato
from StatoConsuntivazione import StatoConsuntivazione
from StatoPresenzaSede import StatoPresenzaSede
from Client import Client
from Server import Server

server = Server()
client = Client(server)

# Ciclo While per fare test
var = input("Benvenuto su Chatterbot Bot4Me, l'esclusivo chatterbot di Imola Informatica (TM). Inserisci qualcosa e poi io vedo cosa fare \n")
while var != "Fine" :
    print(client.getResponse(var))
    var = input()
