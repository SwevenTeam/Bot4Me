import pytest
from Client import Client
from Server import Server
from .util import login


def test_Adapter_Presence_Activate():
    server = Server()
    client = Client(server)
    login(client)
    value = client.getResponse("presenza")
    assert value == "Operazione di registrazione della presenza avviata : inserire il nome di una sede"


def test_Adapter_Presence_Location_Correct():
    server = Server()
    client = Client(server)
    login(client)
    client.getResponse("presenza")
    value = client.getResponse("Imola")
    assert value == "Registrazione presenza effettuata con Successo"


def test_Adapter_Presence_Location_Incorrect():
    server = Server()
    client = Client(server)
    login(client)
    client.getResponse("presenza")
    value = client.getResponse("Padova")
    assert value == "Sede non Accettata : Reinserire il nome della Sede"
