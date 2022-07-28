from StatementStato import StatementStato
from Stato import Stato
from StatoConsuntivazione import StatoConsuntivazione
from StatoPresenzaSede import StatoPresenzaSede
from Client import Client
from Server import Server

server = Server()
client = Client(server)
##print(client.getResponse("Consuntivazione"))
'''
print("\n Per favore consuntiva")

print(client.getResponse("Per favore consuntiva"))

print("Padova")

print(client.getResponse("Padova"))

print("Bel Progetto")

print(client.getResponse("Bel Progetto"))

print("22 Giugno 2022")

print(client.getResponse("22 Giugno 2022"))

print("2 ore")
 
print(client.getResponse("2 ore"))

print("annulla")
 
print(client.getResponse("annulla"))

print(client.getStato().getDati())


'''
var = input("Benvenuto su Chatterbot Bot4Me, l'esclusivo chatterbot di Imola Informatica (TM). Inserisci qualcosa e poi io vedo cosa fare \n")
while var != "Fine" :
    print(client.getResponse(var))
    var = input()
