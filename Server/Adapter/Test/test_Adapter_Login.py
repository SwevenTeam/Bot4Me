import pytest
from ..Adapter import Adapter
from Client import Client
from Server import Server

class Test_Adapter_Login():

    @pytest.fixture
    def server(self):
        return Server()

    def test_Adapter_Login_Activate(self,server):
        client = Client(server)
        value = client.getResponse("login")
        assert value == "Autenticazione Avviata : Inserire l'API-KEY"


    def test_Adapter_Login_Api_Correct(self,server):
        client = Client(server)
        client.getResponse("login")
        value = client.getResponse("12345678-1234-1234-1234-123456789012")
        assert value == "Autenticazione Avvenuta Con Successo"


    def test_Adapter_Login_Api_Incorrect(self,server):
        client = Client(server)
        client.getResponse("login")
        value = client.getResponse("asd")
        assert value == "Autenticazione Fallita : l'API-KEY inserita non è valida, riprova"


    def test_Adapter_Login_Already_Logged(self,server):
        client = Client(server)
        client.getResponse("login")
        client.getResponse("12345678-1234-1234-1234-123456789012")
        value = client.getResponse("login")
        assert value == "Hai già effettuato l'accesso"
