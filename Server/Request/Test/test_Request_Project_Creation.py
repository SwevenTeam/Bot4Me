from ..Request_Project_Creation import Request_Project_Creation
from State.State_Project_Creation import State_Project_Creation
from State.State_Null import State_Null
from unittest.mock import patch
import requests

class Test_Request_Project_Creation():

    def test_Request_Project_Creation_isReady(self):
        S = State_Project_Creation()
        S.addData("1", "codice progetto")
        S.addData("Dettagli", "dettagli")
        S.addData("Tommaso", "cliente")
        S.addData("Pablo", "manager")
        S.addData("iniziale", "status")
        S.addData("Imola", "area")
        S.addData("2022-05-01", "data Inizio")
        S.addData("2022-05-02", "data Fine")
        S.addData("conferma", "conferma")
        Req = Request_Project_Creation(
            S, "12345678-1234-1234-1234-123456789012")
        assert Req.isReady()

    def test_Request_Project_Creation_isReady_Error_Type(self):
        S = State_Null()
        Req = Request_Project_Creation(S, "12345678-1234-1234-1234-123456789012")
        assert Req.isReady() == False
    
    def test_Request_Project_Creation_isReady_Error_Not_Ready(self):
        S = State_Project_Creation()
        Req = Request_Project_Creation(S, "12345678-1234-1234-1234-123456789012")
        assert Req.isReady() == False

    def test_Request_Activity_SendRequest_Error_Not_Ready(self):
        S = State_Project_Creation()
        Req = Request_Project_Creation(S, "")
        assert Req.sendRequest() == False

