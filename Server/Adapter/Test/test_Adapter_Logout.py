import pytest
from Adapter import Adapter 
from Client import Client
from Server import Server
from .util import login

def test_Logout_Correct():
    server = Server()
    client = Client(server)
    login(client)
    value = client.getResponse("logout")
    assert value == "Logout avvenuto con successo"


