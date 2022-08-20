import pytest
from State.Statement_State import Statement_State
from State.State_Null import State_Null
from chatterbot import ChatBot
from .util import ModifyCreation
from Adapter.Adapter_Project_Creation import Adapter_Project_Creation
from State.State_Project_Creation import State_Project_Creation


class Test_Adapter_Project_Creation():

    # Creazione Chatbot Temporaneo per Test
    @pytest.fixture
    def chatbot(self):
        return ChatBot("Test")

    # Test Avvio Creazione Progetto
    def test_Adapter_Creation_Activate(self, chatbot):
        S = Statement_State("crea progetto", State_Null())
        A = Adapter_Project_Creation(chatbot)
        if A.can_process(S):
            value = A.process(S, None)
        assert value.text == "Creazione Progetto Avviata : Inserire il codice del Progetto"

    # Test Inserimento Codice Progetto Corretto
    def test_Adapter_Creation_Code_Correct(self, chatbot):
        S = Statement_State(
            "1999",
            State_Project_Creation(),
            '12345678-1234-1234-1234-123456789012')
        A = Adapter_Project_Creation(chatbot)
        if A.can_process(S):
            value = A.process(S, None)
        assert value.text == "Codice progetto libero : Inserire una descrizione" and S.currentState.getData()[
            'codice progetto'] == "1999"

    # Test Inserimento Codice Progetto Incorretto
    def test_Adapter_Creation_Code_Incorrect(self, chatbot):
        S = Statement_State(
            "1",
            State_Project_Creation(),
            '12345678-1234-1234-1234-123456789012')
        A = Adapter_Project_Creation(chatbot)
        if A.can_process(S):
            value = A.process(S, None)
        assert value.text == "Codice progetto in uso : Reinserire un codice diverso" and S.currentState.getData()[
            'codice progetto'] == ""

    # Test Inserimento Descrizione Progetto
    def test_Adapter_Creation_Details_Correct(self, chatbot):
        Spc = State_Project_Creation()
        Spc.addData("codice progetto", "1999")
        S = Statement_State(
            "template details",
            Spc,
            '12345678-1234-1234-1234-123456789012')
        A = Adapter_Project_Creation(chatbot)
        if A.can_process(S):
            value = A.process(S, None)
        assert value.text == "Descrizione Accettata : Inserire Cliente" and S.currentState.getData()[
            'dettagli'] == "template details"

    # Test Inserimento Cliente
    def test_Adapter_Creation_Client_Correct(self, chatbot):
        Spc = State_Project_Creation()
        Spc.addData("codice progetto", "1999")
        Spc.addData("dettagli", "template details")
        S = Statement_State(
            "cliente",
            Spc,
            '12345678-1234-1234-1234-123456789012')
        A = Adapter_Project_Creation(chatbot)
        if A.can_process(S):
            value = A.process(S, None)
        assert value.text == "Cliente Accettato : Inserire Manager" and S.currentState.getData()[
            'cliente'] == "cliente"

    # Test Inserimento Manager
    def test_Adapter_Creation_Manager_Correct(self, chatbot):
        Spc = State_Project_Creation()
        Spc.addData("codice progetto", "1999")
        Spc.addData("dettagli", "template details")
        Spc.addData("cliente", "cliente")
        S = Statement_State(
            "manager",
            Spc,
            '12345678-1234-1234-1234-123456789012')
        A = Adapter_Project_Creation(chatbot)
        if A.can_process(S):
            value = A.process(S, None)
        assert value.text == "Manager Accettato : Inserire Area" and S.currentState.getData()[
            'manager'] == "manager"

    # Test Inserimento Area Corretta
    @pytest.mark.parametrize("area",
                             [("imola"),
                              ("bologna")])
    def test_Adapter_Creation_Area_Correct(self, area, chatbot):
        Spc = State_Project_Creation()
        Spc.addData("codice progetto", "1999")
        Spc.addData("dettagli", "template details")
        Spc.addData("cliente", "cliente")
        Spc.addData("manager", "manager")
        S = Statement_State(area, Spc, '12345678-1234-1234-1234-123456789012')
        A = Adapter_Project_Creation(chatbot)
        if A.can_process(S):
            value = A.process(S, None)
        assert value.text == "Area Accettata : Inserire Data Inizio" and S.currentState.getData()[
            'area'] in area

    # Test Inserimento Area Incorretta
    def test_Adapter_Creation_Area_Incorrect(self, chatbot):
        Spc = State_Project_Creation()
        Spc.addData("codice progetto", "1999")
        Spc.addData("dettagli", "template details")
        Spc.addData("cliente", "cliente")
        Spc.addData("manager", "manager")
        S = Statement_State(
            "area", Spc, '12345678-1234-1234-1234-123456789012')
        A = Adapter_Project_Creation(chatbot)
        if A.can_process(S):
            value = A.process(S, None)
        assert value.text == "Area non Accettata : Reinserire il nome dell'area" and S.currentState.getData()[
            'area'] == ""

    # Test Inserimento Data Inizio Corretta
    def test_Adapter_Creation_Start_Date_Correct(self, chatbot):
        Spc = State_Project_Creation()
        Spc.addData("codice progetto", "1999")
        Spc.addData("dettagli", "template details")
        Spc.addData("cliente", "cliente")
        Spc.addData("manager", "manager")
        Spc.addData("area", "bologna")
        S = Statement_State(
            "2022-01-01",
            Spc,
            '12345678-1234-1234-1234-123456789012')
        A = Adapter_Project_Creation(chatbot)
        if A.can_process(S):
            value = A.process(S, None)
        assert value.text == "Data di Inizio accettata : Inserire la Data di Fine" and S.currentState.getData()[
            'data Inizio'] == "2022-01-01"

    # Test Inserimento Data Inizio Incorretta
    def test_Adapter_Creation_Start_Date_Incorrect(self, chatbot):
        Spc = State_Project_Creation()
        Spc.addData("codice progetto", "1999")
        Spc.addData("dettagli", "template details")
        Spc.addData("cliente", "cliente")
        Spc.addData("manager", "manager")
        Spc.addData("area", "bologna")
        S = Statement_State(
            "2022-01-011",
            Spc,
            '12345678-1234-1234-1234-123456789012')
        A = Adapter_Project_Creation(chatbot)
        if A.can_process(S):
            value = A.process(S, None)
        assert value.text == "Data di Inizio non accettata : Reinserire la data del progetto" and S.currentState.getData()[
            'data Inizio'] == ""

    # Test Inserimento Data Fine Corretta
    def test_Adapter_Creation_End_Date_Correct(self, chatbot):
        Spc = State_Project_Creation()
        Spc.addData("codice progetto", "1999")
        Spc.addData("dettagli", "template details")
        Spc.addData("cliente", "cliente")
        Spc.addData("manager", "manager")
        Spc.addData("area", "bologna")
        Spc.addData("data Inizio", "2022-01-01")
        S = Statement_State(
            "2022-01-02",
            Spc,
            '12345678-1234-1234-1234-123456789012')
        A = Adapter_Project_Creation(chatbot)
        if A.can_process(S):
            value = A.process(S, None)
        assert value.text == "Data di Fine accettata : Confermare la creazione?" and S.currentState.getData()[
            'data Fine'] == "2022-01-02"

    # Test Inserimento Data Fine Incorretta
    def test_Adapter_Creation_End_Date_Incorrect(self, chatbot):
        Spc = State_Project_Creation()
        Spc.addData("codice progetto", "1999")
        Spc.addData("dettagli", "template details")
        Spc.addData("cliente", "cliente")
        Spc.addData("manager", "manager")
        Spc.addData("area", "bologna")
        Spc.addData("data Inizio", "2022-01-01")
        S = Statement_State(
            "2022-01-022",
            Spc,
            '12345678-1234-1234-1234-123456789012')
        A = Adapter_Project_Creation(chatbot)
        if A.can_process(S):
            value = A.process(S, None)
        assert value.text == "Data di Fine non accettata : Reinserire la data del progetto" and S.currentState.getData()[
            'data Fine'] == ""

    # Test Annulla
    def test_Adapter_Creation_Undo(self, chatbot):
        Spc = State_Project_Creation()
        Spc = ModifyCreation(Spc)
        S = Statement_State(
            'annulla',
            Spc,
            '12345678-1234-1234-1234-123456789012')
        A = Adapter_Project_Creation(chatbot)
        value = A.process(S, None)
        assert "Operazione annullata" in value.text

    # Test Modifica
    def test_Adapter_Creation_Modify(self, chatbot):
        Spc = State_Project_Creation()
        Spc = ModifyCreation(Spc)
        S = Statement_State(
            'modifica',
            Spc,
            '12345678-1234-1234-1234-123456789012')
        A = Adapter_Project_Creation(chatbot)
        value = A.process(S, None)
        assert "Inserire elemento che si vuole modificare" in value.text

    # Test Chiave non accettata
    def test_Adapter_Creation_Key_Incorrect(self, chatbot):
        Spc = State_Project_Creation()
        Spc = ModifyCreation(Spc)
        Spc.addData("conferma", "modifica")
        S = Statement_State(
            'asdasdasd',
            Spc,
            '12345678-1234-1234-1234-123456789012')
        A = Adapter_Project_Creation(chatbot)
        value = A.process(S, None)
        assert "Chiave non accettata. Provare con una chiave diversa" in value.text

    # Test Errore
    def test_Adapter_Creation_Incorrect(self, chatbot):
        Spc = State_Project_Creation()
        Spc = ModifyCreation(Spc)
        S = Statement_State(
            'asdasdasd',
            Spc,
            '12345678-1234-1234-1234-123456789012')
        A = Adapter_Project_Creation(chatbot)
        value = A.process(S, None)
        assert "Input non valido, Reinserire" in value.text

    # Test Errore
    def test_Adapter_Creation_Incorrect(self, chatbot):
        Spc = State_Project_Creation()
        Spc = ModifyCreation(Spc)
        Spc.addData("conferma", "")
        S = Statement_State(
            'asdasdasd',
            Spc,
            '12345678-1234-1234-1234-123456789012')
        A = Adapter_Project_Creation(chatbot)
        value = A.process(S, None)
        assert "È avvenuto un errore sconosciuto" in value.text

    # Test Modifica Codice Progetto
    def test_Adapter_Creation_Modify_Code(self, chatbot):
        Sc = State_Project_Creation()
        Sc = ModifyCreation(Sc)
        Sc.addData('conferma', 'codice progetto')
        S = Statement_State('5', Sc, '12345678-1234-1234-1234-123456789012')
        A = Adapter_Project_Creation(chatbot)
        value = A.process(S, None)
        assert "Codice progetto libero e dato aggiornato." in value.text and S.currentState.getData()[
            'codice progetto'] == "5"

    # Test Modifica Dettagli
    def test_Adapter_Creation_Modify_Details(self, chatbot):
        Sc = State_Project_Creation()
        Sc = ModifyCreation(Sc)
        Sc.addData('conferma', 'dettagli')
        S = Statement_State(
            'descrizopme',
            Sc,
            '12345678-1234-1234-1234-123456789012')
        A = Adapter_Project_Creation(chatbot)
        value = A.process(S, None)
        assert "Descrizione Accettata e aggiornata." in value.text and S.currentState.getData()[
            'dettagli'] == "descrizopme"

    # Test Modifica Cliente
    def test_Adapter_Creation_Modify_Client(self, chatbot):
        Sc = State_Project_Creation()
        Sc = ModifyCreation(Sc)
        Sc.addData('conferma', 'cliente')
        S = Statement_State(
            'clientino',
            Sc,
            '12345678-1234-1234-1234-123456789012')
        A = Adapter_Project_Creation(chatbot)
        value = A.process(S, None)
        assert "Cliente Accettato e aggiornato." in value.text and S.currentState.getData()[
            'cliente'] == "clientino"

    # Test Modifica Manager
    def test_Adapter_Creation_Modify_Manager(self, chatbot):
        Sc = State_Project_Creation()
        Sc = ModifyCreation(Sc)
        Sc.addData('conferma', 'manager')
        S = Statement_State(
            'managerino',
            Sc,
            '12345678-1234-1234-1234-123456789012')
        A = Adapter_Project_Creation(chatbot)
        value = A.process(S, None)
        assert "Manager Accettato e aggiornato." in value.text and S.currentState.getData()[
            'manager'] == "managerino"

    def test_Adapter_Creation_Modify_Area(self, chatbot):
        Sc = State_Project_Creation()
        Sc = ModifyCreation(Sc)
        Sc.addData('conferma', 'area')
        S = Statement_State(
            'Imola', Sc, '12345678-1234-1234-1234-123456789012')
        A = Adapter_Project_Creation(chatbot)
        value = A.process(S, None)
        assert "Area Accettata e aggiornata." in value.text and S.currentState.getData()[
            'area'] == "imola"

    def test_Adapter_Creation_Modify_Start_Date(self, chatbot):
        Sc = State_Project_Creation()
        Sc = ModifyCreation(Sc)
        Sc.addData('conferma', 'data Inizio')
        S = Statement_State(
            '2022-05-05',
            Sc,
            '12345678-1234-1234-1234-123456789012')
        A = Adapter_Project_Creation(chatbot)
        value = A.process(S, None)
        assert "Data di Inizio accettata e aggiornata." in value.text and S.currentState.getData()[
            'data Inizio'] == "2022-05-05"

    def test_Adapter_Creation_Modify_End_Date(self, chatbot):
        Sc = State_Project_Creation()
        Sc = ModifyCreation(Sc)
        Sc.addData('conferma', 'data Fine')
        S = Statement_State(
            '2022-05-05',
            Sc,
            '12345678-1234-1234-1234-123456789012')
        A = Adapter_Project_Creation(chatbot)
        value = A.process(S, None)
        assert "Data di Fine accettata e aggiornata." in value.text and S.currentState.getData()[
            'data Fine'] == "2022-05-05"

    '''
    def test_Adapter_Creation(self, chatbot):
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

        assert value.text == "Operazione avvenuta correttamente"
    '''
