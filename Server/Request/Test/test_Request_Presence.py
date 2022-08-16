from ..Request_Presence import Request_Presence
from State.State_Presence import State_Presence
from unittest.mock import patch

class Test_Request_Presence() :
    
    def test_Request_Presence_isReady(self):
        S = State_Presence()
        S.addData("Imola","sede")
        Req = Request_Presence(S,"12345678-1234-1234-1234-123456789012")
        assert Req.isReady() == True
