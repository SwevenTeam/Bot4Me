from ast import And
from decimal import InvalidOperation
from chatterbot.logic import LogicAdapter
from Server.State.State_Login import State_Login
from Server.State.Statement_State import Statement_State
from chatterbot.conversation import Statement
from sqlalchemy import false, true, null
from Server.State.State_Null import State_Null


class Adapter_Logout(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

    def can_process(self, statement):
        if statement.getApiKey() == null:
            return False

        words = ['logout', 'esci']
        if any(x in statement.text.split() for x in words):
            return True
        else:
            return False

    def process(
            self,
            input_statement,
            additional_response_selection_parameters) -> Statement_State:

        # s rappresenta lo Statement_State
        output_statement = Statement_State(
            "Logout avvenuto con successo", State_Null(), null)

        return output_statement
