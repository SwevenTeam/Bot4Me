import React, { useEffect, useRef, useState } from "react";
import CustomButton from "./CustomButton";
import AudioRecorder from "./AudioRecorder";
import axios from "axios";
import validateApiKey from "./Regex";

const Home = () => {
  const [message, setMessage] = useState("");

  const [apikey, setApiKey] = useState("");
  const [clientId, setClientID] = useState("");
  const [hidden, setHidden] = useState(false);
  const inputApiKey = useRef(null);

  const msgerChat = get(".msger-chat");

  const BOT_IMG = "{{ url_for('static', filename='img/logo.png') }}";
  const PERSON_IMG = "{{ url_for('static', filename='img/user.png') }}";
  const BOT_NAME = "Bot4Me";
  const PERSON_NAME = "Utente X";

  useEffect(() => {
    const api = JSON.parse(localStorage.getItem("apikey"));
    if (api && apikey === "") {
      setApiKey(api);
      setHidden(true);
    } else {
      localStorage.removeItem("apikey");
      setHidden(false);
    }
  }, [apikey]);

  const handleMessageChange = (e) => {
    setMessage(e.target.value);
  };

  const resetMessagge = () => {
    setMessage("");
  };

  const resetApiKey = () => {
    setApiKey("");
  };

  const handleApiKeyChange = (e) => {
    setApiKey(e.target.value);
  };

  const saveApiKey = () => {
    /*
      ---
      Function Name :  saveApiKey
      ---
      - Args → 
      - Description → come prima cosa controlla se è presente un clientID nel localStorage altrimenti, 
        manda la richiesta al Server per riceverne uno, successivamente controlla se l'API-KEY fornita dall'utente è valida,
        se lo è la salva all'interno del LocalStorage del browser ed effettua la procedura di Login passando alla schermata di Utente Autenticato; 
        altrimenti comunica all'utente la non validità.
      - Returns → 
    */
    if (!localStorage.getItem("clientId")) {
      getClientID();
    } else {
      /* istanbul ignore next */
      setClientID(localStorage.getItem("clientId"));
    }
    if (inputApiKey.current.value !== null) {
      if (!validateApiKey.test(inputApiKey.current.value)) {
        alert("API-KEY formato non valido, riprova");
        setApiKey("");
      } else {
        setApiKey(inputApiKey.current.value);
        localStorage.setItem("apikey", JSON.stringify(apikey));
        botResponseWithoutResponse("login");
        botResponse(apikey);
        changeHidden();
      }
    }
  };
  /* istanbul ignore next */
  const logout = () => {
    /*
      ---
      Function Name :  logout
      ---
      - Args → 
      - Description → 
        - Effettua la procedura di Logout dal sistema rimuovendo, se presenti nel LocalStorage, clientID e API-KEY.
          Effettua il reload della pagina mostrando la schermata di Utente Non Autenticato.
      - Returns → 
    */
   
    setApiKey("");
    localStorage.removeItem("apikey");
    setClientID("");
    localStorage.removeItem("clientId");
    botResponse("logout");
    setHidden(false);
    window.location.reload();
  };
  /* istanbul ignore next */
  const finish = () => {
    botResponse("termina");
  };
  /* istanbul ignore next */
  const changeHidden = () => {
    if (apikey === "") {
      setHidden(false);
    } else setHidden(true);
  };

  const onSubmit = () => {
    if (!message) return;
    appendMessage(PERSON_NAME, PERSON_IMG, "right", message);
    setMessage("");
    botResponse(message);
  };
  /* istanbul ignore next */
  const handleKeyDown = (e) => {
    if (e.key === "Enter") {
      onSubmit();
    }
  };

  function appendMessage(name, img, side, text) {
    /*
      ---
      Function Name :  appendMessage
      ---
      - Args → 
        - name: nome dell'utente o del chatbot che ha inviato quel dato messaggio.
        - img: icona associata all'utente o al chatbot da visualizzare assieme al messaggio
        - side: posizione del messaggio nello schermo se nel lato sinistro ovvero del chatbot oppure in quello destro ovvero quello dell'utente
        - text: contenuto effettivo del messaggio inviato
      - Description → genera porzione di codice HTML contenenti le informazioni principali del messaggio e le aggiunge alla schermata di visualizzazione della chat
      - Returns → 
    */
    const msgHTML = `
        <div class="msg ${side}-msg">
          <div class="msg-img" style="background-image: url(${img})"></div>
          <div class="msg-bubble">
            <div class="msg-info">
              <div class="msg-info-name">${name}</div>
              <div class="msg-info-time">${formatDate(new Date())}</div>
            </div>
            <div class="msg-text">${text}</div>
          </div>
        </div>
      `;
    msgerChat.insertAdjacentHTML("beforeend", msgHTML);
    msgerChat.scrollTop += 500;
    if (
      text ===
      "Autenticazione Fallita : l'API-KEY inserita non è valida, riprova"
    ) {
      /* istanbul ignore next */
      setHidden(true);
    }
  }

  function botResponse(rawText) {
    /*
      ---
      Function Name :  botResponse
      ---
      - Args → 
        - rawText: variabile testuale che rappresenta la stringa da inviare al Server
      - Description → funzione che invia il messaggio scritto dall'utente al Server, rimananedo in attesa della risposta e stampando a video il risultato della richiesta. 
      - Returns → 
    */
    const url = "http://127.0.0.1:5000/get";
    axios
      .post(url, {
        textInput: rawText,
        clientID: clientId,
      })
      .then(function (response) {
        /* istanbul ignore next */
        if (
          JSON.stringify(response.data).replaceAll('"', "") ===
          "Autenticazione Fallita : l'API-KEY inserita non è valida, riprova"
        ) {
          const myTimeout = setTimeout(logout, 2000);
        }
        appendMessage(
          BOT_NAME,
          BOT_IMG,
          "left",
          JSON.stringify(response.data).replaceAll('"', "")
        );
      });
  }

  function botResponseWithoutResponse(rawText) {
    const url = "http://127.0.0.1:5000/get";
    axios
      .post(url, {
        textInput: rawText,
        clientID: clientId,
      })
      .then(function (response) {
        /* istanbul ignore next */        
        if (
          JSON.stringify(response.data).replaceAll('"', "") ===
          "Autenticazione Fallita : l'API-KEY inserita non è valida, riprova"
        ) {
          const myTimeout = setTimeout(logout, 2000);
        };
      });
  }  

  function getClientID() {
    /*
      ---
      Function Name :  getClientID
      ---
      - Args → 
      - Description → funzione che richiede al Server di fornire un UUID per il client avviato che verrà poi salvato all'interno del LocalStorage 
        del browser con il nome di ClientID in uso e servirà per mantenere la sessione di comunicazione
      - Returns → 
    */
    const url = "http://127.0.0.1:5000/getID";
    axios
      .post(url, {
        clientID: clientId,
      })
      .then(function (response) {
        /* istanbul ignore next */
        saveClientId(response.data);
      });
  }

  useEffect(() => {
    getClientID();
  }, [""]);

  const saveClientId = (idFromServer) => {
    localStorage.setItem("clientId", idFromServer);
    setClientID(idFromServer);
  };

  // Utils
  function get(selector, root = document) {
    return root.querySelector(selector);
  }

  function formatDate(date) {
    const h = "0" + date.getHours();
    const m = "0" + date.getMinutes();
    return `${h.slice(-2)}:${m.slice(-2)}`;
  }

  return (
    /*
      ---
      Function Name :  return 
      ---
      - Args → 
      - Description → funzione che genera il codice HTML relativo ai componenti che compongono la pagina Home.
      - Returns → 
    */
    <div className="msger">
      <header className="msger-header">
        <div className="msger-header-title">
          <i> Ciao sono il tuo assistente Bot4Me </i>
        </div>

        <CustomButton
          text={"API KEY"}
          isDisabled={!hidden}
          className={"msger-apikey-btn"}
          hidden={hidden}
          icon="Login"
        />

        <CustomButton
          text={"LOGOUT"}
          isDisabled={!hidden}
          /* istanbul ignore next */
          className={"msger-logout-btn"}
          onSubmit={() => {
            logout();
          }}
          hidden={!hidden}
          icon="Logout"
        />
      </header>

      <main className="msger-chat">
        <div className="msg left-msg">
          <div className="msg-img"></div>
          <div className="msg-bubble">
            <div className="msg-info">
              <div className="msg-info-name">Bot4Me</div>
              <div className="msg-info-time"></div>
            </div>

            <div className="msg-text">
              Io sono <b>Bot4Me</b>, sarò il tuo assistente personale 😄
            </div>
            <div className="msg-text">
              Posso aiutarti a semplificare i tuoi compiti aziendali come:
              <ul>
                <li>Inserire rendiconto ore</li>
                <li>Registrare la tua presenza in sede</li>
                <li>Aprire il cancello aziendale</li>
                <li>E molto altro ... </li>
              </ul>
              <div className="msg-text">
                Per mettermi alla prova dovrai fornirmi la tua <b>API-KEY</b> 🔐
              </div>
            </div>
          </div>
        </div>
      </main>

      <div className="input-form">
        <CustomButton
          text={"CANCELLA API-KEY"}
          hidden={hidden}
          isDisabled={apikey === "" ? true : false}
          onSubmit={() => {
            resetApiKey();
          }}
          className={"msger-reset-btn"}
          icon="Trash"
        />
        <input
          type="text"
          ref={inputApiKey}
          value={apikey}
          hidden={hidden}
          className="msger-input"
          id="apikeyInput"
          data-testid="apikeyInput"
          placeholder="Scrivi qui la tua ApiKey..."
          onChange={handleApiKeyChange}
        />
        <CustomButton
          text={"SALVA API-KEY"}
          hidden={hidden}
          isDisabled={apikey === "" ? true : false}
          onSubmit={() => {
            saveApiKey();
          }}
          className={"msger-send-btn"}
          icon="Save"
        />

        <CustomButton
          text={"TERMINA OPERAZIONE"}
          hidden={!hidden}
          isDisabled={
            message === "" ||
            message === "Sto traducendo il tuo messaggio ..." ||
            message === "Sto registrando ..."
              ? true
              : false
          }
          onSubmit={() => {
            finish();
          }}
          className={"msger-undo-btn"}
          icon="Delete"
        />
        <CustomButton
          text={"CANCELLA MESSAGGIO"}
          hidden={!hidden}
          isDisabled={
            message === "" ||
            message === "Sto traducendo il tuo messaggio ..." ||
            message === "Sto registrando ..."
              ? true
              : false
          }
          onSubmit={() => {
            resetMessagge();
          }}
          className={"msger-reset-btn"}
          icon="Trash"
        />
        <input
          onKeyDown={handleKeyDown}
          type="text"
          hidden={!hidden}
          className="msger-input"
          id="textInput"
          value={message}
          placeholder="Scrivi qui il tuo messaggio..."
          onChange={handleMessageChange}
        />
        <CustomButton
          text={"INVIA MESSAGGIO"}
          hidden={!hidden}
          isDisabled={
            message === "" ||
            message === "Sto traducendo il tuo messaggio ..." ||
            message === "Sto registrando ..."
              ? true
              : false
          }
          onSubmit={() => {
            onSubmit();
          }}
          className={"msger-send-btn"}
          icon="Send"
        />
        <AudioRecorder changeMessage={setMessage} hidden={!hidden} />
      </div>
    </div>
  );
};

export default Home;
