from ..Request_Project_Creation import Request_Project_Creation
from State.State_Project_Creation import State_Project_Creation
from unittest.mock import patch


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
