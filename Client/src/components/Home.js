import React, {useEffect, useRef, useState} from 'react';
import CustomButton from './CustomButton';
import AudioRecorder from './AudioRecorder';
import axios from 'axios';
import validateApiKey from './Regex'

const Home = () => {

    const [message, setMessage] = useState("");

    const [apikey, setApiKey] = useState("");
    const [hidden, setHidden] = useState (false);
    const inputApiKey = useRef(null);


    const msgerForm = get(".msger-inputarea");
    const msgerInput = get(".msger-input");
    const msgerChat = get(".msger-chat");


    const BOT_IMG = "{{ url_for('static', filename='img/logo.png') }}";
    const PERSON_IMG = "{{ url_for('static', filename='img/user.png') }}";
    const BOT_NAME = "Bot4Me";
    const PERSON_NAME = "Utente X";

    useEffect(() => {
      const items = JSON.parse(localStorage.getItem('apikey'));
      if (items) {
       setApiKey(items);
       setHidden(true);
      }
      else {
        setApiKey("")
        setHidden(false)
      }
    }, []);

    const handleMessageChange = (e) =>{
      setMessage(e.target.value)
    }

    const resetMessagge = () => {
      setMessage("");
    }

    const resetApiKey = () => {
      setApiKey("");
    }

    const handleApiKeyChange = (e) => {
      setApiKey(e.target.value)
    }
    
    const saveApiKey = () => {
      if(inputApiKey.current.value !== null){
        if (!validateApiKey.test(inputApiKey.current.value)) {
          alert("API-KEY formato non valido, riprova");
          setApiKey("")
          changeHidden()
       }
       else {
        setApiKey(inputApiKey.current.value);
        localStorage.setItem('apikey', JSON.stringify(apikey));
        //botResponse(apikey)
        changeHidden()
       }
      }  
    }

    const login = () => {
      changeHidden()
      /*appendMessage(PERSON_NAME, PERSON_IMG, "right", "login");
      botResponse("login")*/
    }

    const logout = () => {
      setApiKey("")
      localStorage.setItem('apikey', JSON.stringify(""));
      setHidden(false)
      /*appendMessage(PERSON_NAME, PERSON_IMG, "right", "login");
      botResponse("login")*/
    }

    const finish = () => {
      botResponse("termina")
    }

    const changeHidden = () => {
      if(apikey === ""){
        setHidden(false);
      }
      else setHidden(true);
    }

    const onSubmit = () => {
      if (!message) return; 

      appendMessage(PERSON_NAME, PERSON_IMG, "right", message);
      setMessage("")
      botResponse(message);
    };

    const handleKeyDown = (e) => {
      if (e.key === 'Enter') {
        onSubmit()
      }
    }

    function appendMessage(name, img, side, text) {
      //   Simple solution for small apps
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
    }

    function botResponse(rawText) {

     const url = 'http://127.0.0.1:5000/get'
     
     axios.post(url,{
      textInput: rawText,
     }).then(function(response) {
            appendMessage(BOT_NAME, BOT_IMG, "left", JSON.stringify(response.data).replaceAll('"',''))
      });
    }

    // Utils
    function get(selector, root = document) {
      return root.querySelector(selector);
    }

    function formatDate(date) {
      const h = "0" + date.getHours();
      const m = "0" + date.getMinutes();
      return `${h.slice(-2)}:${m.slice(-2)}`;
    }

    return(
      <div className="msger">
          <header className="msger-header">
          <div className="msger-header-title">
              <i> Ciao sono il tuo assistente Bot4Me </i>
          </div>

          <CustomButton text={"API KEY"} isDisabled={!hidden} 
            className={"msger-apikey-btn"} onSubmit={()=>{login()}} 
            hidden={hidden} icon="Login"/>

          <CustomButton text={"LOGOUT"} isDisabled={!hidden} 
            className={"msger-logout-btn"} onSubmit={()=>{logout()}} 
            hidden={!hidden} icon="Logout"/>
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

          <div className='input-form'>
            <CustomButton text={"CANCELLA API-KEY"} hidden={hidden} isDisabled={(apikey) === "" ? true : false} onSubmit={()=>{resetApiKey()}} className={"msger-reset-btn"} icon="Trash"/>
            <input type="text" ref={inputApiKey} value={apikey} hidden={hidden} className="msger-input" id="apikeyInput" placeholder="Scrivi qui la tua ApiKey..." onChange={handleApiKeyChange}/>
            <CustomButton text={"SALVA API-KEY"}  hidden={hidden} isDisabled={(apikey) === "" ? true : false} onSubmit={()=>{saveApiKey()}} className={"msger-send-btn"} icon="Save"/>
            
            
            <CustomButton text={"TERMINA OPERAZIONE"} hidden={!hidden} onSubmit={()=>{finish()}} className={"msger-undo-btn"} icon="Delete"/>
            <CustomButton text={"CANCELLA MESSAGGIO"} hidden={!hidden} isDisabled={(message) === "" ? true : false} onSubmit={()=>{resetMessagge()}} className={"msger-reset-btn"} icon="Trash"/>
            <input onKeyDown={handleKeyDown} type="text" hidden={!hidden} className="msger-input" id="textInput" value={message} placeholder="Scrivi qui il tuo messaggio..." onChange={handleMessageChange}/>          
            <CustomButton text={"INVIA MESSAGGIO"}  hidden={!hidden} isDisabled={(message) === "" ? true : false} onSubmit={()=>{onSubmit()}} className={"msger-send-btn"} icon="Send"/>
            <AudioRecorder changeMessage={setMessage} hidden={!hidden}/>
          </div>
        </div>
    )
}

export default Home;