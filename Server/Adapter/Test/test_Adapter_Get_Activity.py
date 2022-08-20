import pytest
from State.Statement_State import Statement_State
from State.State_Null import State_Null
from chatterbot import ChatBot
from .util import ModifyActivity
from Adapter.Adapter_Get_Activity import Adapter_Get_Activity
from State.State_Get_Activity import State_Get_Activity


class Test_Adapter_Get_Activity():

    # Creazione Chatbot Temporaneo per Test
    @pytest.fixture
    def chatbot(self):
        return ChatBot("Test")

    # Test Avvio Ritorno Consuntivazione
    def test_Adapter_Activity_Activate(self, chatbot):
        S = Statement_State("ritorna consuntiva", State_Null())
        A = Adapter_Get_Activity(chatbot)
        if A.can_process(S):
            value = A.process(S, None)
        assert value.text == "Operazione Restituzione di Consuntivazione Avviata : Inserire il codice del Progetto"

    # Test Inserimento Codice Corretto
    def test_Adapter_Activity_Code_Correct(self, chatbot):
        S = Statement_State(
            "1",
            State_Get_Activity(),
            '12345678-1234-1234-1234-123456789012')
        A = Adapter_Get_Activity(chatbot)
        if A.can_process(S):
            value = A.process(S, None)
        assert "Consuntivazione del giorno" in value.text

    # Test Inserimento Codice Incorretto Numero
    def test_Adapter_Activity_Code_Incorrect_Number(self, chatbot):
        S = Statement_State(
            "1999999999999999",
            State_Get_Activity(),
            '12345678-1234-1234-1234-123456789012')
        A = Adapter_Get_Activity(chatbot)
        value = A.process(S, None)
        assert value.text == "Progetto Inesistente : Inserire un nuovo codice" and S.currentState.getData()[
            'codice progetto'] == ""

    # Test Inserimento Codice Incorretto String
    @pytest.mark.parametrize("code",
                             [("esempio"),
                                 ("cacaca")])
    def test_Adapter_Activity_Code_Incorrect_String(self, code, chatbot):
        S = Statement_State(
            code,
            State_Get_Activity(),
            '12345678-1234-1234-1234-123456789012')
        A = Adapter_Get_Activity(chatbot)
        value = A.process(S, None)
        assert value.text == "Inserire il codice del Progetto come numero" and S.currentState.getData()[
            'codice progetto'] == ""
   