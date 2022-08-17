import pytest
from ..Adapter import Adapter
from Client import Client
from Server import Server
from .util import login
from Request.Request_Presence import Request_Presence

class Test_Adapter():

    @pytest.fixture
    def server(self):
        return Server()

    def test_Adapter_Presence_Activate(self, server):
        client = Client(server)
        login(client)
        value = client.getResponse("presenza")
        assert value == "Operazione di registrazione della presenza avviata : inserire il nome di una sede"

    @pytest.mark.parametrize("sede", [("Imola"), ("Bologna")])
    def test_Adapter_Presence_Location_Correct(self, sede, server):
        client = Client(server)
        login(client)
        client.getResponse("presenza")
        value = client.getResponse(sede)
        assert value == "Registrazione presenza effettuata con Successo"

    def test_Adapter_Presence_Location_Incorrect(self, server):
        client = Client(server)
        login(client)
        client.getResponse("presenza")
        value = client.getResponse("Padova")
        assert value == "Sede non Accettata : Reinserire il nome della Sede"