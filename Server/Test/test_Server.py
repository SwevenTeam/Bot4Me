from re import S
from Adapter import Adapter
from Server import Server
from Client import Client
from State.State import State
from sqlalchemy import null


def test_Server_No_Login():
    server = Server()
    client = Client(server)
    value = client.getResponse("esempio")
    assert value == "Devi prima effettuare l'accesso per utilizzare i nostri servizi"


def test_Server_No_Adapter():
    server = Server()
    client = Client(server)

    client.getResponse("login")
    client.getResponse("12345678-1234-1234-1234-123456789012")
    value = client.getResponse("esempio")
    assert value == "Nessun Logic Adapter Adatto Trovato"
