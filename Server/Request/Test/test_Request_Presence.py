from ..Request_Presence import Request_Presence
from State.State_Presence import State_Presence
from State.State_Gate import State_Gate
import requests
import json


class Test_Request_Presence():

    def test_Request_Presence_isReady(self):
        S = State_Presence()
        S.addData("sede", "Imola")
        print(S.getData())
        Req = Request_Presence(S, "12345678-1234-1234-1234-123456789012")
        assert Req.isReady()

    def test_Request_Presence_isReady_Error_Data(self):
        S = State_Presence()
        Req = Request_Presence(S, "12345678-1234-1234-1234-123456789012")
        assert Req.isReady() == False

    def test_Request_Presence_isReady_Error_State(self):
        S = State_Gate()
        S.addData("sede", "Imola")
        Req = Request_Presence(S, "12345678-1234-1234-1234-123456789012")
        assert Req.isReady() == False

    def test_Request_Presence(self):
        headers = {
            'api_key': "12345678-1234-1234-1234-123456789012",
            'accept': 'application/json',
            'Content-Type': 'application/json'
        }
        url = "https://apibot4me.imolinfo.it/v1/locations/Imola/presence"
        response = requests.post(url, headers=headers, data={})
        assert response.status_code >= 200 and response.status_code < 300

    def test_Request_Presence_Error_Api(self):
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        }
        url = "https://apibot4me.imolinfo.it/v1/locations/Imola/presence"
        response = requests.post(url, headers=headers, data={})
        assert response.status_code >= 400
