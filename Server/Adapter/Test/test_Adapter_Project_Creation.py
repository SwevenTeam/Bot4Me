import pytest
from Client import Client
from Server import Server
from .util import login


def test_Adapter_Creation_Activate():
    server = Server()
    client = Client(server)
    login(client)
    value = client.getResponse("crea progetto")
    assert value == "Creazione Progetto Avviata : Inserire il codice del Progetto"


def test_Adapter_Creation_Code_Correct():
    server = Server()
    client = Client(server)
    login(client)
    client.getResponse("crea progetto")
    value = client.getResponse("1999")
    assert value == "Codice progetto libero : Inserire una descrizione"


def test_Adapter_Creation_Code_Incorrect():
    server = Server()
    client = Client(server)
    login(client)
    client.getResponse("crea progetto")
    value = client.getResponse("1")
    assert value == "Codice progetto in uso : Reinserire un codice diverso"


def test_Adapter_Creation_Description_Correct():
    server = Server()
    client = Client(server)
    login(client)
    client.getResponse("crea progetto")
    client.getResponse("1999")
    value = client.getResponse("template description")
    assert value == "Descrizione Accettata : Inserire Cliente"


def test_Adapter_Creation_Client_Correct():
    server = Server()
    client = Client(server)
    login(client)
    client.getResponse("crea progetto")
    client.getResponse("1999")
    client.getResponse("template description")
    value = client.getResponse("template client")
    assert value == "Cliente Accettato : Inserire Manager"


def test_Adapter_Creation_Manager_Correct():
    server = Server()
    client = Client(server)
    login(client)
    client.getResponse("crea progetto")
    client.getResponse("1999")
    client.getResponse("template description")
    client.getResponse("template client")
    value = client.getResponse("template manager")
    assert value == "Manager Accettato : Inserire Area"


def test_Adapter_Creation_Area_Correct_Imola():
    server = Server()
    client = Client(server)
    login(client)
    client.getResponse("crea progetto")
    client.getResponse("1999")
    client.getResponse("template description")
    client.getResponse("template client")
    client.getResponse("template manager")
    value = client.getResponse("Imola")
    assert value == "Area Accettata : Inserire Data Inizio"


def test_Adapter_Creation_Area_Correct_Bologna():
    server = Server()
    client = Client(server)
    login(client)
    client.getResponse("crea progetto")
    client.getResponse("1999")
    client.getResponse("template description")
    client.getResponse("template client")
    client.getResponse("template manager")
    value = client.getResponse("Bologna")
    assert value == "Area Accettata : Inserire Data Inizio"


def test_Adapter_Creation_Area_Incorrect():
    server = Server()
    client = Client(server)
    login(client)
    client.getResponse("crea progetto")
    client.getResponse("1999")
    client.getResponse("template description")
    client.getResponse("template client")
    client.getResponse("template manager")
    value = client.getResponse("Imolaaaaaaaaaaaaaaaa")
    assert value == "Area non Accettata : Reinserire il nome dell'area"


def test_Adapter_Creation_Start_Date_Correct():
    server = Server()
    client = Client(server)
    login(client)
    client.getResponse("crea progetto")
    client.getResponse("1999")
    client.getResponse("template description")
    client.getResponse("template client")
    client.getResponse("template manager")
    client.getResponse("Bologna")
    value = client.getResponse("2022-01-01")
    assert value == "Data di Inizio accettata : Inserire la Data di Fine"


def test_Adapter_Creation_Start_Date_Incorrect():
    server = Server()
    client = Client(server)
    login(client)
    client.getResponse("crea progetto")
    client.getResponse("1999")
    client.getResponse("template description")
    client.getResponse("template client")
    client.getResponse("template manager")
    client.getResponse("Bologna")
    value = client.getResponse("2022-01-0111")
    assert value == "Data di Inizio non accettata : Reinserire la data del progetto"


def test_Adapter_Creation_End_Date_Correct():
    server = Server()
    client = Client(server)
    login(client)
    client.getResponse("crea progetto")
    client.getResponse("1999")
    client.getResponse("template description")
    client.getResponse("template client")
    client.getResponse("template manager")
    client.getResponse("Bologna")
    client.getResponse("2022-01-01")
    value = client.getResponse("2022-01-02")
    assert value == "Data di Fine accettata : Confermare la creazione?"


def test_Adapter_Creation_End_Date_Incorrect():
    server = Server()
    client = Client(server)
    login(client)
    client.getResponse("crea progetto")
    client.getResponse("1999")
    client.getResponse("template description")
    client.getResponse("template client")
    client.getResponse("template manager")
    client.getResponse("Bologna")
    client.getResponse("2022-01-01")
    value = client.getResponse("2022-01-0111")
    assert value == "Data di Fine non accettata : Reinserire la data del progetto"


def test_Adapter_Creation_Modify_Code():
    server = Server()
    client = Client(server)
    login(client)
    client.getResponse("crea progetto")
    client.getResponse("1999")
    client.getResponse("template description")
    client.getResponse("template client")
    client.getResponse("template manager")
    client.getResponse("Bologna")
    client.getResponse("2022-01-01")
    client.getResponse("2022-01-02")
    client.getResponse("Modifica")
    client.getResponse("codice progetto")
    value = client.getResponse("5")
    assert "Codice progetto libero e dato aggiornato." in value


def test_Adapter_Creation_Modify_Description():
    server = Server()
    client = Client(server)
    login(client)
    client.getResponse("crea progetto")
    client.getResponse("1999")
    client.getResponse("template description")
    client.getResponse("template client")
    client.getResponse("template manager")
    client.getResponse("Bologna")
    client.getResponse("2022-01-01")
    client.getResponse("2022-01-02")
    client.getResponse("Modifica")
    client.getResponse("dettagli")
    value = client.getResponse("asderino")
    assert "Descrizione Accettata e aggiornata." in value


def test_Adapter_Creation_Modify_Client():
    server = Server()
    client = Client(server)
    login(client)
    client.getResponse("crea progetto")
    client.getResponse("1999")
    client.getResponse("template description")
    client.getResponse("template client")
    client.getResponse("template manager")
    client.getResponse("Bologna")
    client.getResponse("2022-01-01")
    client.getResponse("2022-01-02")
    client.getResponse("Modifica")
    client.getResponse("cliente")
    value = client.getResponse("clientino")
    assert "Cliente Accettato e aggiornato." in value


def test_Adapter_Creation_Modify_Manager():
    server = Server()
    client = Client(server)
    login(client)
    client.getResponse("crea progetto")
    client.getResponse("1999")
    client.getResponse("template description")
    client.getResponse("template client")
    client.getResponse("template manager")
    client.getResponse("Bologna")
    client.getResponse("2022-01-01")
    client.getResponse("2022-01-02")
    client.getResponse("Modifica")
    client.getResponse("manager")
    value = client.getResponse("managerino")
    assert "Manager Accettata e aggiornato." in value


def test_Adapter_Creation_Modify_Area():
    server = Server()
    client = Client(server)
    login(client)
    client.getResponse("crea progetto")
    client.getResponse("1999")
    client.getResponse("template description")
    client.getResponse("template client")
    client.getResponse("template manager")
    client.getResponse("Bologna")
    client.getResponse("2022-01-01")
    client.getResponse("2022-01-02")
    client.getResponse("Modifica")
    client.getResponse("area")
    value = client.getResponse("Imola")
    assert "Area Accettata e aggiornata." in value


def test_Adapter_Creation_Modify_Start_Date():
    server = Server()
    client = Client(server)
    login(client)
    client.getResponse("crea progetto")
    client.getResponse("1999")
    client.getResponse("template description")
    client.getResponse("template client")
    client.getResponse("template manager")
    client.getResponse("Bologna")
    client.getResponse("2022-01-01")
    client.getResponse("2022-01-02")
    client.getResponse("Modifica")
    client.getResponse("data Inizio")
    value = client.getResponse("2022-02-02")
    assert "Data di Inizio accettata e aggiornata." in value


def test_Adapter_Creation_Modify_End_Date():
    server = Server()
    client = Client(server)
    login(client)
    client.getResponse("crea progetto")
    client.getResponse("1999")
    client.getResponse("template description")
    client.getResponse("template client")
    client.getResponse("template manager")
    client.getResponse("Bologna")
    client.getResponse("2022-01-01")
    client.getResponse("2022-01-02")
    client.getResponse("Modifica")
    client.getResponse("data Fine")
    value = client.getResponse("2022-02-02")
    assert "Data di Fine accettata e aggiornata." in value


'''
def test_Adapter_Creation():
    server = Server()
    client = Client(server)
    login(client)
    client.getResponse("crea progetto")
    client.getResponse("1999")
    client.getResponse("template description")
    client.getResponse("template client")
    client.getResponse("template manager")
    client.getResponse("Bologna")
    client.getResponse("2022-01-01")
    client.getResponse("2022-01-02")
    value = client.getResponse("conferma")

    assert value == "Operazione avvenuta correttamente"
'''
