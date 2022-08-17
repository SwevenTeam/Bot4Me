import pytest
from sqlalchemy import null
from ..State_Presence import State_Presence


class Test_State_Presence:

    def test_State_Presence(self):
        SP = State_Presence()
        assert SP.getData()['sede'] == ""

    def test_State_Presence_Correct(self):
        SP = State_Presence()
        SP.addData("sede", "Imola")
        assert SP.getData()['sede'] == "Imola"

    def test_State_Presence_Incorrect(self):
        SP = State_Presence()
        SP.addData("sedee", "Imola")
        assert SP.getData()['sede'] == ""
