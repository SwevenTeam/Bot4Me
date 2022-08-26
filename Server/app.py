from http import client
from Client import Client
from Server import Server
from flask import Flask, render_template, request, session
from flask_cors import CORS
from uuid import uuid4
from sqlalchemy import null

app = Flask(__name__)

CORS(app)

server = Server()
clients = {
    uuid4() : Client(server)
}

@app.route("/getID", methods=['POST'])
def get_client_id():
    #userText = request.args.get('msg').lower()
    if request.method == 'POST':
        userId = uuid4()
        clients.update({str(userId) : Client(server)})
        return str(userId)


@app.route("/get", methods=['POST'])
def get_bot_response():
    #userText = request.args.get('msg').lower()
    if request.method == 'POST':
        userText = request.json.get('textInput')
        userID = request.json.get('clientID')
        print(clients.get(userID))
        return clients.get(userID).getResponse(userText)

if __name__ == "__main__":
    app.run()

"""
var = input("Benvenuto su Chatterbot Bot4Me, l'esclusivo chatterbot di Imola Informatica (TM). Inserisci qualcosa e poi io vedo cosa fare \n")
while var != "Fine" :
    print(client.getResponse(var))
    var = input()
"""