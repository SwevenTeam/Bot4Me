from ..Request_Activity import Request_Activity
from State.State_Activity import State_Activity
from unittest.mock import patch


class Test_Request_Activity():

    def test_Request_Activity_isReady(self):
        S = State_Activity()
        S.addData("1", "codice progetto")
        S.addData("2022-05-01", "data")
        S.addData("5", "ore fatturabili")
        S.addData("5", "ore viaggio")
        S.addData("5", "ore viaggio fatturabili")
        S.addData("Imola", "sede")
        S.addData("True", "fatturabile")
        S.addData("descrizione", "descrizione")
        S.addData("conferma", "conferma")
        Req = Request_Activity(S, "12345678-1234-1234-1234-123456789012")
        assert Req.isReady()
