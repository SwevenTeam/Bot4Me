import pytest
from ..Adapter import Adapter
from Client import Client
from Server import Server
from .util import login


class Test_Adapter_Activity():

    @pytest.fixture
    def server(self):
        return Server()

    def test_Adapter_Activity_Activate(self, server):
        client = Client(server)
        login(client)
        value = client.getResponse("consuntiva")
        assert value == "Consuntivazione Avviata : Inserire il codice del Progetto"

    def test_Adapter_Activity_Code_Correct(self, server):
        client = Client(server)
        login(client)
        client.getResponse("consuntiva")
        value = client.getResponse("1")
        assert value == "Progetto esistente : Inserire la data di consuntivazione ( formato aaaa-mm-gg )"

    @pytest.mark.parametrize("code",
                             [("1999999999999999"),
                              ("esempio"),
                                 ("cacaca")])
    def test_Adapter_Activity_Code_Incorrect(self, code, server):
        client = Client(server)
        login(client)
        client.getResponse("consuntiva")
        value = client.getResponse(code)
        assert value == "Progetto non esistente : Reinserire un codice diverso o creare un nuovo progetto"

    def test_Adapter_Activity_Date_Correct(self, server):
        client = Client(server)
        login(client)
        client.getResponse("consuntiva")
        client.getResponse("1")
        value = client.getResponse("2022-01-01")
        assert value == "Data accettata : Inserire le ore fatturabili"

    @pytest.mark.parametrize("date",
                             [("2022-02-30"),
                              ("2022-02-0111"),
                                 ("1999-13-25")])
    def test_Adapter_Activity_Date_Incorrect(self, date, server):
        client = Client(server)
        login(client)
        client.getResponse("consuntiva")
        client.getResponse("1")
        value = client.getResponse(date)
        assert value == "Data non accettata : Reinserire la data del progetto"

    def test_Adapter_Activity_Billable_Hours_Correct(self, server):
        client = Client(server)
        login(client)
        client.getResponse("consuntiva")
        client.getResponse("1")
        client.getResponse("2022-01-01")
        value = client.getResponse("3")
        assert value == "Ore fatturabili accettate : Inserire le ore di viaggio"

    @pytest.mark.parametrize("billable_hours", [("no"), ("-5.4"), ("cinque")])
    def test_Adapter_Activity_Billable_Hours_Incorrect(
            self, billable_hours, server):
        client = Client(server)
        login(client)
        client.getResponse("consuntiva")
        client.getResponse("1")
        client.getResponse("2022-01-01")
        value = client.getResponse(billable_hours)
        assert value == "Ore fatturabili non accettate : Reinserire le ore fatturabili come numero"

    def test_Adapter_Activity_Travel_Hours_Correct(self, server):
        client = Client(server)
        login(client)
        client.getResponse("consuntiva")
        client.getResponse("1")
        client.getResponse("2022-01-01")
        client.getResponse("3")
        value = client.getResponse("3")
        assert value == "Ore viaggio accettate : Inserire le ore di viaggio fatturabili"

    @pytest.mark.parametrize("travel_hours", [("no"), ("-5.4"), ("cinque")])
    def test_Adapter_Activity_Travel_Hours_Incorrect(
            self, travel_hours, server):
        client = Client(server)
        login(client)
        client.getResponse("consuntiva")
        client.getResponse("1")
        client.getResponse("2022-01-01")
        client.getResponse("3")
        value = client.getResponse(travel_hours)
        assert value == "Ore viaggio non accettate : Reinserire le ore di viaggio come numero"

    def test_Adapter_Activity_Billable_Travel_Hours_Correct(self, server):
        client = Client(server)
        login(client)
        client.getResponse("consuntiva")
        client.getResponse("1")
        client.getResponse("2022-01-01")
        client.getResponse("3")
        client.getResponse("3")
        value = client.getResponse("3")
        assert value == "Ore viaggio fatturabili Accettate : Inserire la sede"

    @pytest.mark.parametrize("billable_travel_hours",
                             [("no"), ("-5.4"), ("cinque")])
    def test_Adapter_Activity_Billable_Travel_Hours_Incorrect(
            self, billable_travel_hours, server):

        client = Client(server)
        login(client)
        client.getResponse("consuntiva")
        client.getResponse("1")
        client.getResponse("2022-01-01")
        client.getResponse("3")
        client.getResponse("3")
        value = client.getResponse(billable_travel_hours)
        assert value == "Ore viaggio fatturabili non accettate : Reinserire le ore di viaggio fatturabili come numero"

    @pytest.mark.parametrize("Imola", [("Imona"), ("Imola"), ("Imole")])
    def test_Adapter_Activity_Area_Correct_Imola(self, Imola, server):
        client = Client(server)
        login(client)
        client.getResponse("consuntiva")
        client.getResponse("1")
        client.getResponse("2022-01-01")
        client.getResponse("3")
        client.getResponse("3")
        client.getResponse("3")
        value = client.getResponse(Imola)
        assert value == "Sede Accettata : È fatturabile?"

    @pytest.mark.parametrize("Bologna",
                             [("boligna"), ("Bologna"), ("bolonia")])
    def test_Adapter_Activity_Area_Correct_Bologna(self, Bologna, server):
        client = Client(server)
        login(client)
        client.getResponse("consuntiva")
        client.getResponse("1")
        client.getResponse("2022-01-01")
        client.getResponse("3")
        client.getResponse("3")
        client.getResponse("3")
        value = client.getResponse(Bologna)
        assert value == "Sede Accettata : È fatturabile?"

    @pytest.mark.parametrize("Sede", [("Padova"), ("Molise"), ("Francia")])
    def test_Adapter_Activity_Area_Incorrect(self, Sede, server):
        client = Client(server)
        login(client)
        client.getResponse("consuntiva")
        client.getResponse("1")
        client.getResponse("2022-01-01")
        client.getResponse("3")
        client.getResponse("3")
        client.getResponse("3")
        value = client.getResponse(Sede)
        assert value == "Sede non Accettata : Reinserire il nome della Sede"

    @pytest.mark.parametrize("Conferma", [("sì"), ("true"), ("vero")])
    def test_Adapter_Activity_Billable_True(self, Conferma, server):
        client = Client(server)
        login(client)
        client.getResponse("consuntiva")
        client.getResponse("1")
        client.getResponse("2022-01-01")
        client.getResponse("3")
        client.getResponse("3")
        client.getResponse("3")
        client.getResponse("Imola")
        value = client.getResponse(Conferma)
        assert value == "Scelta Fatturabilità accettata : Inserire la descrizione"

    @pytest.mark.parametrize("Negazione", [("no"), ("false"), ("falso")])
    def test_Adapter_Activity_Billable_No(self, Negazione, server):
        client = Client(server)
        login(client)
        client.getResponse("consuntiva")
        client.getResponse("1")
        client.getResponse("2022-01-01")
        client.getResponse("3")
        client.getResponse("3")
        client.getResponse("3")
        client.getResponse("Imola")
        value = client.getResponse(Negazione)
        assert value == "Scelta Fatturabilità accettata : Inserire la descrizione"

    def test_Adapter_Activity_Billable_Incorrect(self, server):
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

    def test_Adapter_Activity_Modify_Code(self, server):
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
        client.getResponse("Ez")
        client.getResponse("Modifica")
        client.getResponse("codice progetto")
        value = client.getResponse("1")
        assert "Progetto esistente e dato aggiornato. Visualizzazione Dati Aggiornati" in value

    def test_Adapter_Activity_Modify_Fail(self, server):
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
        client.getResponse("Ez")
        client.getResponse("Modifica")
        value = client.getResponse("asdasdasd")
        assert "Chiave non accettata. Provare con una chiave diversa" in value

    def test_Adapter_Activity_Modify_Undo(self, server):
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
        client.getResponse("Ez")
        value = client.getResponse("Annulla")
        assert "Operazione annullata" in value

    def test_Adapter_Activity_Modify_Wrong_Input(self, server):
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
        client.getResponse("Ez")
        value = client.getResponse("zazazaz")
        assert "Input non valido, Reinserire" in value

    def test_Adapter_Activity_Modify_Date(self, server):
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
        client.getResponse("Ez")
        client.getResponse("Modifica")
        client.getResponse("data")
        value = client.getResponse("2022-02-02")
        assert "Data accettata e aggiornata. Visualizzazione Dati Aggiornati" in value

    def test_Adapter_Activity_Modify_Billable_Hours(self, server):
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
        client.getResponse("Ez")
        client.getResponse("Modifica")
        client.getResponse("ore fatturabili")
        value = client.getResponse("5")
        assert "Ore Fatturabili accettate e aggiornate. Visualizzazione Dati Aggiornati" in value

    def test_Adapter_Activity_Modify_Travel_Hours(self, server):
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
        client.getResponse("Ez")
        client.getResponse("Modifica")
        client.getResponse("ore viaggio")
        value = client.getResponse("5")
        assert "Ore di viaggio accettate e aggiornate. Visualizzazione Dati Aggiornati" in value

    def test_Adapter_Activity_Modify_Billable_Travel_Hours(self, server):
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
        client.getResponse("Ez")
        client.getResponse("Modifica")
        client.getResponse("ore viaggio fatturabili")
        value = client.getResponse("5")
        assert "Ore di viaggio fatturabili accettate e aggiornate. Visualizzazione Dati Aggiornati" in value

    def test_Adapter_Activity_Modify_Area(self, server):
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
        client.getResponse("Ez")
        client.getResponse("Modifica")
        client.getResponse("sede")
        value = client.getResponse("Bologna")
        assert "Sede Accettata e aggiornata." in value

    def test_Adapter_Activity_Modify_Billable_True(self, server):
        client = Client(server)
        login(client)
        client.getResponse("consuntiva")
        client.getResponse("1")
        client.getResponse("2022-01-01")
        client.getResponse("3")
        client.getResponse("3")
        client.getResponse("3")
        client.getResponse("Imola")
        client.getResponse("no")
        client.getResponse("Ez")
        client.getResponse("Modifica")
        client.getResponse("fatturabile")
        value = client.getResponse("sì")
        assert "Fatturabilità Accettata e aggiornata" in value

    def test_Adapter_Activity_Modify_Billable_False(self, server):
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
        client.getResponse("Ez")
        client.getResponse("Modifica")
        client.getResponse("fatturabile")
        value = client.getResponse("no")
        assert "Fatturabilità Accettata e aggiornata" in value

    def test_Adapter_Activity_Modify_Description(self, server):
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
        client.getResponse("Ez")
        client.getResponse("Modifica")
        client.getResponse("descrizione")
        value = client.getResponse("zazazazazaza")
        assert "Descrizione Accettata e aggiornata" in value
