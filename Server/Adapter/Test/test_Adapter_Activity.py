import pytest
from State.Statement_State import Statement_State
from State.State_Null import State_Null
from chatterbot import ChatBot
from .util import ModifyActivity
from Adapter.Adapter_Activity import Adapter_Activity
from State.State_Activity import State_Activity


class Test_Adapter_Activity():

    # Creazione Chatbot Temporaneo per Test
    @pytest.fixture
    def chatbot(self):
        return ChatBot("Test")

    # Test Avvio Consuntivazione
    # T_U29
    def test_Adapter_Activity_Activate(self, chatbot):
        S = Statement_State("consuntiva", State_Null())
        A = Adapter_Activity(chatbot)
        value = A.process(S, None)
        assert value.text == "Consuntivazione Avviata : Inserire il codice del Progetto"

    # Test Inserimento Codice Corretto
    def test_Adapter_Activity_Code_Correct(self, chatbot):
        S = Statement_State(
            "1",
            State_Activity(),
            '12345678-1234-1234-1234-123456789012')
        A = Adapter_Activity(chatbot)
        value = A.process(S, None)
        assert value.text == "Progetto esistente : Inserire la data di consuntivazione ( formato aaaa-mm-gg )" and S.currentState.getData()[
            'codice progetto'] == "1"

    # Test Inserimento Codice Incorretto
    @pytest.mark.parametrize("code",
                             [("1999999999999999"),
                              ("esempio"),
                                 ("cacaca")])
    def test_Adapter_Activity_Code_Incorrect(self, code, chatbot):
        S = Statement_State(
            code,
            State_Activity(),
            '12345678-1234-1234-1234-123456789012')
        A = Adapter_Activity(chatbot)
        value = A.process(S, None)
        assert value.text == "Progetto non esistente : Reinserire un codice diverso o creare un nuovo progetto" and S.currentState.getData()[
            'codice progetto'] == ""

    # Test Inserimento Data Corretta
    def test_Adapter_Activity_Date_Correct(self, chatbot):
        Sa = State_Activity()
        Sa.addData('codice progetto', "1")
        S = Statement_State(
            "2022-01-01",
            Sa,
            '12345678-1234-1234-1234-123456789012')
        A = Adapter_Activity(chatbot)
        value = A.process(S, None)
        assert value.text == "Data accettata : Inserire le ore fatturabili" and S.currentState.getData(
        )['codice progetto'] == "1" and S.currentState.getData()['data'] == "2022-01-01"

    # Test Inserimento Data Incorretta
    @pytest.mark.parametrize("date",
                             [("2022-02-30"),
                              ("2022-02-0111"),
                                 ("1999-13-25")])
    def test_Adapter_Activity_Date_Incorrect(self, date, chatbot):
        Sa = State_Activity()
        Sa.addData('codice progetto', "1")
        S = Statement_State(date, Sa, '12345678-1234-1234-1234-123456789012')
        A = Adapter_Activity(chatbot)
        value = A.process(S, None)
        assert value.text == "Data non accettata : Reinserire la data del progetto" and S.currentState.getData()[
            'data'] == ""

    # Test Inserimento Ore Fatturabili Corrette
    def test_Adapter_Activity_Billable_Hours_Correct(self, chatbot):
        Sa = State_Activity()
        Sa.addData('codice progetto', "1")
        Sa.addData('data', "2022-01-01")
        S = Statement_State("3", Sa, '12345678-1234-1234-1234-123456789012')
        A = Adapter_Activity(chatbot)
        value = A.process(S, None)
        assert value.text == "Ore fatturabili accettate : Inserire le ore di viaggio" and S.currentState.getData()[
            'ore fatturabili'] == "3"

    # Test Inserimento Ore Fatturabili Incorrette
    @pytest.mark.parametrize("billable_hours", [("no"), ("-5.4"), ("cinque")])
    def test_Adapter_Activity_Billable_Hours_Incorrect(
            self, billable_hours, chatbot):
        Sa = State_Activity()
        Sa.addData('codice progetto', "1")
        Sa.addData('data', "2022-01-01")
        S = Statement_State(
            billable_hours,
            Sa,
            '12345678-1234-1234-1234-123456789012')
        A = Adapter_Activity(chatbot)
        value = A.process(S, None)
        assert value.text == "Ore fatturabili non accettate : Reinserire le ore fatturabili come numero" and S.currentState.getData()[
            'ore fatturabili'] == ""

    # Test Inserimento Ore di Viaggio Corrette
    def test_Adapter_Activity_Travel_Hours_Correct(self, chatbot):
        Sa = State_Activity()
        Sa.addData('codice progetto', "1")
        Sa.addData('data', "2022-01-01")
        Sa.addData('ore fatturabili', "3")
        S = Statement_State("3", Sa, '12345678-1234-1234-1234-123456789012')
        A = Adapter_Activity(chatbot)
        value = A.process(S, None)
        assert value.text == "Ore viaggio accettate : Inserire le ore di viaggio fatturabili" and S.currentState.getData()[
            'ore viaggio'] == "3"

    # Test Inserimento Ore di Viaggio Incorrette
    @pytest.mark.parametrize("travel_hours", [("no"), ("-5.4"), ("cinque")])
    def test_Adapter_Activity_Travel_Hours_Incorrect(
            self, travel_hours, chatbot):
        Sa = State_Activity()
        Sa.addData('codice progetto', "1")
        Sa.addData('data', "2022-01-01")
        Sa.addData('ore fatturabili', "3")
        S = Statement_State(
            travel_hours,
            Sa,
            '12345678-1234-1234-1234-123456789012')
        A = Adapter_Activity(chatbot)
        value = A.process(S, None)
        assert value.text == "Ore viaggio non accettate : Reinserire le ore di viaggio come numero" and S.currentState.getData()[
            'ore viaggio'] == ""

    # Test Inserimento Ore di Viaggio Fatturabili Corrette
    def test_Adapter_Activity_Billable_Travel_Hours_Correct(self, chatbot):
        Sa = State_Activity()
        Sa.addData('codice progetto', "1")
        Sa.addData('data', "2022-01-01")
        Sa.addData('ore fatturabili', "3")
        Sa.addData('ore viaggio', "3")
        S = Statement_State("3", Sa, '12345678-1234-1234-1234-123456789012')
        A = Adapter_Activity(chatbot)
        value = A.process(S, None)
        assert value.text == "Ore viaggio fatturabili Accettate : Inserire la sede" and S.currentState.getData()[
            'ore viaggio fatturabili'] == "3"

    # Test Inserimento Ore di Viaggio Fatturabili Incorrette
    @pytest.mark.parametrize("billable_travel_hours",
                             [("no"), ("-5.4"), ("cinque")])
    def test_Adapter_Activity_Billable_Travel_Hours_Incorrect(
            self, billable_travel_hours, chatbot):
        Sa = State_Activity()
        Sa.addData('codice progetto', "1")
        Sa.addData('data', "2022-01-01")
        Sa.addData('ore fatturabili', "3")
        Sa.addData('ore viaggio', "3")
        S = Statement_State(
            billable_travel_hours,
            Sa,
            '12345678-1234-1234-1234-123456789012')
        A = Adapter_Activity(chatbot)
        value = A.process(S, None)
        assert value.text == "Ore viaggio fatturabili non accettate : Reinserire le ore di viaggio fatturabili come numero" and S.currentState.getData()[
            'ore viaggio fatturabili'] == ""

    # Test Inserimento Sede Corretta
    @pytest.mark.parametrize("Sede",
                             [("Imona"),
                              ("Imola"),
                                 ("Imole"),
                                 ("boligna"),
                                 ("Bologna"),
                                 ("bolonia")])
    def test_Adapter_Activity_Area_Correct_Imola(self, Sede, chatbot):
        Sa = State_Activity()
        Sa.addData('codice progetto', "1")
        Sa.addData('data', "2022-01-01")
        Sa.addData('ore fatturabili', "3")
        Sa.addData('ore viaggio', "3")
        Sa.addData('ore viaggio fatturabili', "3")
        S = Statement_State(Sede, Sa, '12345678-1234-1234-1234-123456789012')
        A = Adapter_Activity(chatbot)
        value = A.process(S, None)
        assert value.text == "Sede Accettata : È fatturabile?" and any(
            i in S.currentState.getData()['sede'] for i in Sede)

    # Test Inserimento Sede Incorretta
    @pytest.mark.parametrize("Sede", [("Padova"), ("Molise"), ("Francia")])
    def test_Adapter_Activity_Area_Incorrect(self, Sede, chatbot):
        Sa = State_Activity()
        Sa.addData('codice progetto', "1")
        Sa.addData('data', "2022-01-01")
        Sa.addData('ore fatturabili', "3")
        Sa.addData('ore viaggio', "3")
        Sa.addData('ore viaggio fatturabili', "3")
        S = Statement_State(Sede, Sa, '12345678-1234-1234-1234-123456789012')
        A = Adapter_Activity(chatbot)
        value = A.process(S, None)
        assert value.text == "Sede non Accettata : Reinserire il nome della Sede" and S.currentState.getData()[
            'sede'] == ""

    # Test Scelta Fatturabilità Corretta
    @pytest.mark.parametrize("Scelta",
                             [("sì"),
                              ("true"),
                                 ("vero"),
                                 ("no"),
                                 ("false"),
                                 ("falso")])
    def test_Adapter_Activity_Billable_True(self, Scelta, chatbot):
        Sa = State_Activity()
        Sa.addData('codice progetto', "1")
        Sa.addData('data', "2022-01-01")
        Sa.addData('ore fatturabili', "3")
        Sa.addData('ore viaggio', "3")
        Sa.addData('ore viaggio fatturabili', "3")
        Sa.addData('sede', "imola")
        S = Statement_State(Scelta, Sa, '12345678-1234-1234-1234-123456789012')
        A = Adapter_Activity(chatbot)
        value = A.process(S, None)
        assert value.text == "Scelta Fatturabilità accettata : Inserire la descrizione (tra Sviluppo, Formazione e Collaborazione )" and (
            S.currentState.getData()['fatturabile'] == 'True' or S.currentState.getData()['fatturabile'] == 'False')

    # Test Scelta Fatturabilità Incorretta
    def test_Adapter_Activity_Billable_Incorrect(self, chatbot):
        Sa = State_Activity()
        Sa.addData('codice progetto', "1")
        Sa.addData('data', "2022-01-01")
        Sa.addData('ore fatturabili', "3")
        Sa.addData('ore viaggio', "3")
        Sa.addData('ore viaggio fatturabili', "3")
        Sa.addData('sede', "imola")
        S = Statement_State(
            'bzorg', Sa, '12345678-1234-1234-1234-123456789012')
        A = Adapter_Activity(chatbot)
        value = A.process(S, None)
        assert value.text == "Scelta Fatturabilità non accettata : reinserire una risposta corretta ( esempio : sì/no)" and S.currentState.getData()[
            'fatturabile'] == ''

    # Test Descrizione
    def test_Adapter_Activity_Description(self, chatbot):
        Sa = State_Activity()
        Sa.addData('codice progetto', "1")
        Sa.addData('data', "2022-01-01")
        Sa.addData('ore fatturabili', "3")
        Sa.addData('ore viaggio', "3")
        Sa.addData('ore viaggio fatturabili', "3")
        Sa.addData('sede', "imola")
        Sa.addData('fatturabile', "True")
        S = Statement_State(
            'sviluppo', Sa, '12345678-1234-1234-1234-123456789012')
        A = Adapter_Activity(chatbot)
        value = A.process(S, None)
        assert "Descrizione Accettata : Inserimento completato <br>" in value.text and S.currentState.getData()[
            'descrizione'] == "sviluppo"
    
    # Test Descrizione
    def test_Adapter_Activity_Description_Incorrect(self, chatbot):
        Sa = State_Activity()
        Sa.addData('codice progetto', "1")
        Sa.addData('data', "2022-01-01")
        Sa.addData('ore fatturabili', "3")
        Sa.addData('ore viaggio', "3")
        Sa.addData('ore viaggio fatturabili', "3")
        Sa.addData('sede', "imola")
        Sa.addData('fatturabile', "True")
        S = Statement_State(
            'lul', Sa, '12345678-1234-1234-1234-123456789012')
        A = Adapter_Activity(chatbot)
        value = A.process(S, None)
        assert "Descrizione non accettata : reinserire una descrizione valida (tra Sviluppo, Formazione e Collaborazione )" in value.text and S.currentState.getData()[
            'descrizione'] == ""


    # Test Modifica Chiave Non Accettata
    def test_Adapter_Activity_Modify_Fail(self, chatbot):
        Sa = State_Activity()
        Sa = ModifyActivity(Sa)
        Sa.addData('conferma', 'modifica')
        S = Statement_State(
            'asdasdsadsadsadsadsadsadsa',
            Sa,
            '12345678-1234-1234-1234-123456789012')
        A = Adapter_Activity(chatbot)
        value = A.process(S, None)
        assert "Chiave non accettata. Provare con una chiave diversa" in value.text

    # Test Modifica
    def test_Adapter_Activity_Modify(self, chatbot):
        Sa = State_Activity()
        Sa = ModifyActivity(Sa)
        S = Statement_State(
            'modifica',
            Sa,
            '12345678-1234-1234-1234-123456789012')
        A = Adapter_Activity(chatbot)
        value = A.process(S, None)
        assert "Inserire elemento che si vuole modificare" in value.text

    # Test Modifica Chiave
    def test_Adapter_Activity_Modify_Key(self, chatbot):
        Sa = State_Activity()
        Sa = ModifyActivity(Sa)
        Sa.addData('conferma', 'modifica')
        S = Statement_State(
            'data',
            Sa,
            '12345678-1234-1234-1234-123456789012')
        A = Adapter_Activity(chatbot)
        value = A.process(S, None)
        assert "Inserire nuovo valore per data" in value.text

    # Test Errore
    def test_Adapter_Activity_Error(self, chatbot):
        Sa = State_Activity()
        Sa = ModifyActivity(Sa)
        Sa.addData('conferma', "")
        S = Statement_State(
            'data',
            Sa,
            '12345678-1234-1234-1234-123456789012')
        A = Adapter_Activity(chatbot)
        value = A.process(S, None)
        assert "È avvenuto un errore sconosciuto" == value.text

    # Test Annullamento Operazione
    def test_Adapter_Activity_Modify_Undo(self, chatbot):
        Sa = State_Activity()
        Sa = ModifyActivity(Sa)
        S = Statement_State(
            'Annulla', Sa, '12345678-1234-1234-1234-123456789012')
        A = Adapter_Activity(chatbot)
        value = A.process(S, None)
        assert "Operazione annullata" in value.text

    # Test Input non Valido
    def test_Adapter_Activity_Modify_Wrong_Input(self, chatbot):
        Sa = State_Activity()
        Sa = ModifyActivity(Sa)
        S = Statement_State('5', Sa, '12345678-1234-1234-1234-123456789012')
        A = Adapter_Activity(chatbot)
        value = A.process(S, None)
        assert "Input non valido, Reinserire" in value.text

    # Test Modifica Codice
    def test_Adapter_Activity_Modify_Code(self, chatbot):
        Sa = State_Activity()
        Sa = ModifyActivity(Sa)
        Sa.addData('conferma', 'codice progetto')
        S = Statement_State('1', Sa, '12345678-1234-1234-1234-123456789012')
        A = Adapter_Activity(chatbot)
        value = A.process(S, None)
        assert "Progetto esistente e dato aggiornato. Visualizzazione Dati Aggiornati" in value.text and S.currentState.getData()[
            'codice progetto'] == "1"

    # Test Modifica Data
    def test_Adapter_Activity_Modify_Date(self, chatbot):
        Sa = State_Activity()
        Sa = ModifyActivity(Sa)
        Sa.addData('conferma', 'data')
        S = Statement_State(
            '2022-02-02',
            Sa,
            '12345678-1234-1234-1234-123456789012')
        A = Adapter_Activity(chatbot)
        value = A.process(S, None)
        assert "Data accettata e aggiornata. Visualizzazione Dati Aggiornati" in value.text and S.currentState.getData()[
            'data'] == "2022-02-02"

    # Test Modifica Ore Fatturabili
    def test_Adapter_Activity_Modify_Billable_Hours(self, chatbot):
        Sa = State_Activity()
        Sa = ModifyActivity(Sa)
        Sa.addData('conferma', 'ore fatturabili')
        S = Statement_State('5', Sa, '12345678-1234-1234-1234-123456789012')
        A = Adapter_Activity(chatbot)
        value = A.process(S, None)
        assert "Ore Fatturabili accettate e aggiornate. Visualizzazione Dati Aggiornati" in value.text and S.currentState.getData()[
            'ore fatturabili'] == "5"

    # Test Modifica Ore Vaggio
    def test_Adapter_Activity_Modify_Travel_Hours(self, chatbot):
        Sa = State_Activity()
        Sa = ModifyActivity(Sa)
        Sa.addData('conferma', 'ore viaggio')
        S = Statement_State('5', Sa, '12345678-1234-1234-1234-123456789012')
        A = Adapter_Activity(chatbot)
        value = A.process(S, None)
        assert "Ore di viaggio accettate e aggiornate. Visualizzazione Dati Aggiornati" in value.text and S.currentState.getData()[
            'ore viaggio'] == "5"

    # Test Modifica Ore Vaggio Fatturabili
    def test_Adapter_Activity_Modify_Billable_Travel_Hours(self, chatbot):
        Sa = State_Activity()
        Sa = ModifyActivity(Sa)
        Sa.addData('conferma', 'ore viaggio fatturabili')
        S = Statement_State('5', Sa, '12345678-1234-1234-1234-123456789012')
        A = Adapter_Activity(chatbot)
        value = A.process(S, None)
        assert "Ore di viaggio fatturabili accettate e aggiornate. Visualizzazione Dati Aggiornati" in value.text and S.currentState.getData()[
            'ore viaggio fatturabili'] == "5"

    # Test Modifica Sede
    def test_Adapter_Activity_Modify_Area(self, chatbot):
        Sa = State_Activity()
        Sa = ModifyActivity(Sa)
        Sa.addData('conferma', 'sede')
        S = Statement_State(
            'Bologna', Sa, '12345678-1234-1234-1234-123456789012')
        A = Adapter_Activity(chatbot)
        value = A.process(S, None)
        assert "Sede Accettata e aggiornata." in value.text and S.currentState.getData()[
            'sede'] == "bologna"

    # Test Modifica Fatturabile Vero
    def test_Adapter_Activity_Modify_Billable_True(self, chatbot):
        Sa = State_Activity()
        Sa = ModifyActivity(Sa)
        Sa.addData('conferma', 'fatturabile')
        S = Statement_State('True', Sa, '12345678-1234-1234-1234-123456789012')
        A = Adapter_Activity(chatbot)
        value = A.process(S, None)
        assert "Fatturabilità Accettata e aggiornata" in value.text and S.currentState.getData()[
            'fatturabile'] == "True"

    # Test Modifica Fatturabile Vero
    def test_Adapter_Activity_Modify_Billable_False(self, chatbot):
        Sa = State_Activity()
        Sa = ModifyActivity(Sa)
        Sa.addData('conferma', 'fatturabile')
        S = Statement_State(
            'False', Sa, '12345678-1234-1234-1234-123456789012')
        A = Adapter_Activity(chatbot)
        value = A.process(S, None)
        assert "Fatturabilità Accettata e aggiornata" in value.text and S.currentState.getData()[
            'fatturabile'] == "False"

    # Test Modifica Descrizione Vero
    def test_Adapter_Activity_Modify_Description(self, chatbot):
        Sa = State_Activity()
        Sa = ModifyActivity(Sa)
        Sa.addData('conferma', 'descrizione')
        S = Statement_State(
            'Collaborazione',
            Sa,
            '12345678-1234-1234-1234-123456789012')
        A = Adapter_Activity(chatbot)
        value = A.process(S, None)
        assert "Descrizione Accettata e aggiornata" in value.text and S.currentState.getData()[
            'descrizione'] == "Collaborazione"

    # Test Modifica Descrizione Vero
    def test_Adapter_Activity_Confirm_Fail(self, chatbot):
        Sa = State_Activity()
        Sa = ModifyActivity(Sa)
        S = Statement_State(
            'Conferma',
            Sa,
            '12345672')
        A = Adapter_Activity(chatbot)
        value = A.process(S, None)
        assert "Operazione non avvenuta, riprovare? (inviare annulla per annullare)" == value.text

    def test_Adapter_Activity_Confirm_Fail_Api(self, chatbot):
        Sa = State_Activity()
        Sa = ModifyActivity(Sa)
        S = Statement_State(
            'Conferma',
            Sa,
            '')
        A = Adapter_Activity(chatbot)
        value = A.process(S, None)
        assert "Operazione non avvenuta correttamente, riprovare? (inviare annulla per annullare)" == value.text

