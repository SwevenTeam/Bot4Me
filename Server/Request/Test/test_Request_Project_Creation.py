from ..Request_Project_Creation import Request_Project_Creation
from State.State_Project_Creation import State_Project_Creation
from State.State_Null import State_Null
import requests


class Test_Request_Project_Creation():

    def test_Request_Project_Creation_isReady(self):
        S = State_Project_Creation()
        S.addData("codice progetto", "1")
        S.addData("dettagli", "Dettagli")
        S.addData("cliente", "Tommaso")
        S.addData("manager", "Pablo")
        S.addData("status", "iniziale")
        S.addData("area", "Imola")
        S.addData("data Inizio", "2022-05-01")
        S.addData("data Fine", "2022-05-02")
        S.addData("conferma", "conferma")
        Req = Request_Project_Creation(
            S, "12345678-1234-1234-1234-123456789012")
        assert Req.isReady()

    def test_Request_Project_Creation_isReady_Error_Type(self):
        S = State_Null()
        Req = Request_Project_Creation(
            S, "12345678-1234-1234-1234-123456789012")
        assert Req.isReady() == False

    def test_Request_Project_Creation_isReady_Error_Not_Ready(self):
        S = State_Project_Creation()
        Req = Request_Project_Creation(
            S, "12345678-1234-1234-1234-123456789012")
        assert Req.isReady() == False

    def test_Request_Activity_SendRequest_Error_Not_Ready(self):
        S = State_Project_Creation()
        Req = Request_Project_Creation(S, "")
        assert Req.sendRequest() == False
