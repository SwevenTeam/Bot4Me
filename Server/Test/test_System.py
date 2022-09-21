from re import S
from Adapter import Adapter
from Client import Client
from Server import Server
from State.State import State
import pytest
from sqlalchemy import null
from State.State_Presence import State_Presence
from State.State_Null import State_Null


class Test_Client():

    # T_S47
    def test_Check_In(self):
        server = Server()
        # Creo il Client e faccio il Login
        clientOne = Client(server)
        clientOne.getResponse("login")
        clientOne.getResponse("12345678-1234-1234-1234-123456789012")
        # Richiedo il login dopo aver già fatto il Login
        clientOneAnswer = clientOne.getResponse("login")

        assert clientOneAnswer == "Hai già effettuato l'accesso"
