from StatementStato import StatementStato
from Stato import Stato
from StatoConsuntivazione import StatoConsuntivazione
from StatoPresenzaSede import StatoPresenzaSede
from Client import Client
from Server import Server
from flask import Flask, render_template, request, session

app = Flask(__name__)

server = Server()
client = Client(server)

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg').lower()
    return str(client.getResponse(userText))

if __name__ == "__main__":
    app.run()

