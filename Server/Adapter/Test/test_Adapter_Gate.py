import pytest
from Client import Client
from Server import Server
from .util import login


def test_Adapter_Gate_Activate():
    server = Server()
    client = Client(server)
    login(client)
    value = client.getResponse("apertura cancello")
    assert value == "Apertura cancello avviata : Inserire la sede del cancello"


'''
def test_Adapter_Gate_Location_Correct():
    server = Server()
    client = Client(server)
    login(client)
    client.getResponse("cancello")
    value = client.getResponse("IMOLA")
    assert value == "Sede accettata : Richiesta apertura del cancello avvenuta con successo"
'''


def test_Adapter_Presence_Location_Incorrect():
    server = Server()
    client = Client(server)
    login(client)
    client.getResponse("cancello")
    value = client.getResponse("Imolaaaaaa")
    assert value == "Sede non trovata : Reinserire la sede del cancello"
