import pytest
from Adapter import Adapter 
from Client import Client
from Server import Server
from .util import login

def test_Adapter_Activity_Activate():
    server = Server()
    client = Client(server)
    login(client)
    value = client.getResponse("consuntiva")
    assert value == "Consuntivazione Avviata : Inserire il codice del Progetto"

def test_Adapter_Activity_Code_Correct():
    server = Server()
    client = Client(server)
    login(client)
    client.getResponse("consuntiva")
    value = client.getResponse("1")
    assert value == "Progetto esistente : Inserire la data di consuntivazione ( formato aaaa-mm-gg )"

def test_Adapter_Activity_Code_Incorrect():
    server = Server()
    client = Client(server)
    login(client)
    client.getResponse("consuntiva")
    value = client.getResponse("1999999999999999")
    assert value == "Progetto non esistente : Reinserire un codice diverso o creare un nuovo progetto"

def test_Adapter_Activity_Date_Correct():
    server = Server()
    client = Client(server)
    login(client)
    client.getResponse("consuntiva")
    client.getResponse("1")
    value = client.getResponse("2022-01-01")
    assert value == "Data accettata : Inserire le ore fatturabili"

def test_Adapter_Activity_Date_Incorrect():
    server = Server()
    client = Client(server)
    login(client)
    client.getResponse("consuntiva")
    client.getResponse("1")
    value = client.getResponse("2022-01-0111")
    assert value == "Data non accettata : Reinserire la data del progetto"

def test_Adapter_Activity_Billable_Hours_Correct():
    server = Server()
    client = Client(server)
    login(client)
    client.getResponse("consuntiva")
    client.getResponse("1")
    client.getResponse("2022-01-01")
    value = client.getResponse("3")
    assert value == "Ore fatturabili accettate : Inserire le ore di viaggio"

def test_Adapter_Activity_Billable_Hours_Incorrect():
    server = Server()
    client = Client(server)
    login(client)
    client.getResponse("consuntiva")
    client.getResponse("1")
    client.getResponse("2022-01-01")
    value = client.getResponse("no")
    assert value == "Ore fatturabili non accettate : Reinserire le ore fatturabili come numero"

def test_Adapter_Activity_Travel_Hours_Correct():
    server = Server()
    client = Client(server)
    login(client)
    client.getResponse("consuntiva")
    client.getResponse("1")
    client.getResponse("2022-01-01")
    client.getResponse("3")
    value = client.getResponse("3")
    assert value == "Ore viaggio accettate : Inserire le ore di viaggio fatturabili"

def test_Adapter_Activity_Travel_Hours_Incorrect():
    server = Server()
    client = Client(server)
    login(client)
    client.getResponse("consuntiva")
    client.getResponse("1")
    client.getResponse("2022-01-01")
    client.getResponse("3")
    value = client.getResponse("no")
    assert value == "Ore viaggio non accettate : Reinserire le ore di viaggio come numero"

def test_Adapter_Activity_Billable_Travel_Hours_Correct():
    server = Server()
    client = Client(server)
    login(client)
    client.getResponse("consuntiva")
    client.getResponse("1")
    client.getResponse("2022-01-01")
    client.getResponse("3")
    client.getResponse("3")
    value = client.getResponse("3")
    assert value == "Ore viaggio fatturabili Accettate : Inserire la sede"

def test_Adapter_Activity_Billable_Travel_Hours_Incorrect():
    server = Server()
    client = Client(server)
    login(client)
    client.getResponse("consuntiva")
    client.getResponse("1")
    client.getResponse("2022-01-01")
    client.getResponse("3")
    client.getResponse("3")
    value = client.getResponse("no")
    assert value == "Ore viaggio fatturabili non accettate : Reinserire le ore di viaggio fatturabili come numero"

def test_Adapter_Activity_Area_Correct_Imola():
    server = Server()
    client = Client(server)
    login(client)
    client.getResponse("consuntiva")
    client.getResponse("1")
    client.getResponse("2022-01-01")
    client.getResponse("3")
    client.getResponse("3")
    client.getResponse("3")
    value = client.getResponse("Imola")
    assert value == "Sede Accettata : È fatturabile?"

def test_Adapter_Activity_Area_Correct_Bologna():
    server = Server()
    client = Client(server)
    login(client)
    client.getResponse("consuntiva")
    client.getResponse("1")
    client.getResponse("2022-01-01")
    client.getResponse("3")
    client.getResponse("3")
    client.getResponse("3")
    value = client.getResponse("Bologna")
    assert value == "Sede Accettata : È fatturabile?"

def test_Adapter_Activity_Area_Incorrect():
    server = Server()
    client = Client(server)
    login(client)
    client.getResponse("consuntiva")
    client.getResponse("1")
    client.getResponse("2022-01-01")
    client.getResponse("3")
    client.getResponse("3")
    client.getResponse("3")
    value = client.getResponse("Padova")
    assert value == "Sede non Accettata : Reinserire il nome della Sede"

def test_Adapter_Activity_Billable_True():
    server = Server()
    client = Client(server)
    login(client)
    client.getResponse("consuntiva")
    client.getResponse("1")
    client.getResponse("2022-01-01")
    client.getResponse("3")
    client.getResponse("3")
    client.getResponse("3")
    client.getResponse("Imola")
    value = client.getResponse("sì")
    assert value == "Scelta Fatturabilità accettata : Inserire la descrizione"

def test_Adapter_Activity_Billable_No():
    server = Server()
    client = Client(server)
    login(client)
    client.getResponse("consuntiva")
    client.getResponse("1")
    client.getResponse("2022-01-01")
    client.getResponse("3")
    client.getResponse("3")
    client.getResponse("3")
    client.getResponse("Imola")
    value = client.getResponse("no")
    assert value == "Scelta Fatturabilità accettata : Inserire la descrizione"

def test_Adapter_Activity_Billable_Incorrect():
    server = Server()
    client = Client(server)
    login(client)
    client.getResponse("consuntiva")
    client.getResponse("1")
    client.getResponse("2022-01-01")
    client.getResponse("3")
    client.getResponse("3")
    client.getResponse("3")
    client.getResponse("Imola")
    value = client.getResponse("bzorg")
    assert value == "Scelta Fatturabilità non accettata : reinserire una risposta corretta ( esempio : sì/no)"
'''
def test_Adapter_Activity_Description():
    server = Server()
    client = Client(server)
    login(client)
    client.getResponse("consuntiva")
    client.getResponse("1")
    client.getResponse("2022-01-01")
    client.getResponse("3")
    client.getResponse("3")
    client.getResponse("3")
    client.getResponse("Imola")
    client.getResponse("sì")
    value = client.getResponse("Ez")
    print(value)
    assert value == "Descrizione Accettata : Inserimento completato <br>codice progetto : 1<br>data : 2022-01-01<br>ore fatturabili : 3<br>ore viaggio : 3<br>ore viaggio fatturabili : 3<br>sede : Imola<br>fatturabile : True<br>descrizione : Ez<br>conferma : non confermato<br>vuoi consuntivare? ( consuntiva per consuntivare, modifica per modificare, annulla per annullare )"

'''
