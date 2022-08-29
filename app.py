from http import client
from Server.Client import Client
from Server.Server import Server
from flask import Flask, render_template, request, session
from flask_cors import CORS
from uuid import uuid4
from sqlalchemy import null

app =Flask(__name__ ,static_folder='Client/Build',static_url_path='')

CORS(app)

server = Server()
clients = {}


@app.route("/getID", methods=['POST'])
def get_client_id():
    #userText = request.args.get('msg').lower()
    if request.method == 'POST':
        userId = str(uuid4())
        clients.update({userId: Client(server)})
        return userId


@app.route("/get", methods=['POST'])
def get_bot_response():
    #userText = request.args.get('msg').lower()
    if request.method == 'POST':
        userText = request.json.get('textInput')
        userID = request.json.get('clientID')
        return clients.get(userID).getResponse(userText)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
"""
var = input("Benvenuto su Chatterbot Bot4Me, l'esclusivo chatterbot di Imola Informatica (TM). Inserisci qualcosa e poi io vedo cosa fare \n")
while var != "Fine" :
    print(client.getResponse(var))
    var = input()
"""
