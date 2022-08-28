import pytest
from State.Statement_State import Statement_State
from State.State_Null import State_Null
from chatterbot import ChatBot
from Adapter.Adapter_Gate import Adapter_Gate
from State.State_Gate import State_Gate
from State.State_Presence import State_Presence
from sqlalchemy import null


class Test_Adapter_Gate():

    # Creazione Chatbot Temporaneo per Test
    @pytest.fixture
    def chatbot(self):
        return ChatBot("Test")

    # Test Avvio Apertura Cancello
    # T_U31
    def test_Adapter_Gate_Activate(self, chatbot):
        S = Statement_State("apertura cancello", State_Null())
        A = Adapter_Gate(chatbot)
        if A.can_process(S):
            value = A.process(S, None)
        assert value.text == "Apertura cancello avviata : Inserire la sede del cancello"

    # Test Apertura Cancello Sede
    def test_Adapter_Gate_Area(self, chatbot):
        S = Statement_State(
            "imola",
            State_Gate(),
            '12345678-1234-1234-1234-123456789012')
        A = Adapter_Gate(chatbot)
        if A.can_process(S):
            value = A.process(S, None)
        assert value.text == "Sede accettata : Confermare l'apertura del cancello della sede di imola? (si, modifica, annulla)"

    # Test Apertura Cancello Modifica Sede
    def test_Adapter_Gate_Modify(self, chatbot):
        Sg = State_Gate()
        Sg.addData("sede", "imola")
        S = Statement_State(
            "modifica",
            Sg,
            '12345678-1234-1234-1234-123456789012')
        A = Adapter_Gate(chatbot)
        if A.can_process(S):
            value = A.process(S, None)
        assert value.text == "Modifica della sede : Inserire la sede del cancello"

    # Test Apertura Cancello conferma errore
    # T_U32
    def test_Adapter_Gate_Error(self, chatbot):
        Sg = State_Gate()
        Sg.addData("sede", "imola")
        S = Statement_State("conferma", Sg, '12')
        A = Adapter_Gate(chatbot)
        if A.can_process(S):
            value = A.process(S, None)
        assert value.text == "Si è verificato un errore sconosciuto, riprova a confermare"

    # Test Apertura Cancello conferma ancora

    def test_Adapter_Gate_Confirm_Again(self, chatbot):
        Sg = State_Gate()
        Sg.addData("sede", "imola")
        S = Statement_State(
            "asdasdasdsadsad",
            Sg,
            '12345678-1234-1234-1234-123456789012')
        A = Adapter_Gate(chatbot)
        if A.can_process(S):
            value = A.process(S, None)
        assert value.text == "Confermare l'apertura del cancello della sede di imola? (si, modifica annulla)"
    '''
    def test_Adapter_Gate_Location_Correct(self,chatbot):
        client = Client(server)
        login(client)
        client.getResponse("cancello")
        value = client.getResponse("IMOLA")
        assert value == "Sede accettata : Richiesta apertura del cancello avvenuta con successo"
    '''
    # Test Apertura Cancello Sede Incorretta

    def test_Adapter_Gate_Location_Incorrect(self, chatbot):
        S = Statement_State(
            "Imolaaaaaa",
            State_Gate(),
            '12345678-1234-1234-1234-123456789012')
        A = Adapter_Gate(chatbot)
        if A.can_process(S):
            value = A.process(S, None)
        assert value.text == "Sede non trovata : Reinserire la sede del cancello"

    # Test is Ready No Api

    def test_Adapter_Gate_Is_Ready_Error(self, chatbot):
        S = Statement_State("ciao", State_Null(), '')
        A = Adapter_Gate(chatbot)
        assert A.can_process(S) == False

    # Test Apertura Cancello conferma ancora
    def test_Adapter_Gate_Is_Ready_False(self, chatbot):
        Sp = State_Presence()
        Sp.addData("sede", "imola")
        S = Statement_State("conferma", Sp, '')
        A = Adapter_Gate(chatbot)
        value = A.process(S, None)
        assert value.text == "Dati non inseriti correttamente, provare a modificare e reinserire"
