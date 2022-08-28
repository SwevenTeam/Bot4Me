from re import S
from Adapter import Adapter
from Client import Client
from State.State import State
import pytest
from sqlalchemy import null
from State.State_Presence import State_Presence
from State.State_Null import State_Null


class Test_Client():

    # T_U1
    def test_Client_State(self):
        client = Client(null)
        assert client.state.getCurrentState() == State_Null().getCurrentState()

    # T_U2
    def test_Client_Api(self):
        client = Client(null)
        assert client.apiKey == null

    # T_U3
    def test_Client_Upgrade_State(self):
        client = Client(null)
        client.upgradeState(State_Presence())
        assert client.state.getCurrentState() == State_Presence().getCurrentState()

    # T_U4
    def test_Client_Upgrade_Api(self):
        client = Client(null)
        client.upgradeApiKey('5')
        assert client.apiKey == '5'
