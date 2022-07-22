from StatementStato import StatementStato
from Stato import Stato
from StatoPresenzaSede import StatoPresenzaSede
from Client import Client
from Server import Server

server = Server()
client = Client(server)
print(client.getResponse("hbuhjuj"))

