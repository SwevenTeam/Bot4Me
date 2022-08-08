from StatementStato import StatementStato
from Stato import Stato
from StatoConsuntivazione import StatoConsuntivazione
from StatoPresenzaSede import StatoPresenzaSede
from Client import Client
from Server import Server
from flask import Flask, render_template, request, session
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

server = Server()
client = Client(server)

@app.route("/get", methods=['POST'])
def get_bot_response():
    #userText = request.args.get('msg').lower()
    if request.method == 'POST':
        userText = request.json.get('textInput')
        return str(client.getResponse(userText))

if __name__ == "__main__":
    app.run()

"""
var = input("Benvenuto su Chatterbot Bot4Me, l'esclusivo chatterbot di Imola Informatica (TM). Inserisci qualcosa e poi io vedo cosa fare \n")
while var != "Fine" :
    print(client.getResponse(var))
    var = input()
"""
