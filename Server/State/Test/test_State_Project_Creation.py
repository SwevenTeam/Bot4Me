import pytest
from sqlalchemy import null
from ..State_Project_Creation import State_Project_Creation


class Test_State_Project_Creation:

    def test_State_Project_Creation(self):
        SP = State_Project_Creation()
        assert SP.getData()['area'] == ""

    def test_State_Project_Creation_Correct(self):
        SP = State_Project_Creation()
        SP.addData("area", "Imola")
        assert SP.getData()['area'] == "Imola"

    def test_State_Project_Creation_Incorrect(self):
        SP = State_Project_Creation()
        SP.addData("sedee", "Imola")
        assert SP.getData()['area'] == ""
