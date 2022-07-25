import React, {useRef, useState} from 'react';
import CustomButton from './CustomButton';
import AudioRecorder from './AudioRecorder';

const Home = () => {

    const [message, setMessage] = useState("");

    const [apikey, setApiKey] = useState("");
    const [hidden, setHidden] = useState (true);
    const inputApiKey = useRef(null);


    const msgerForm = get(".msger-inputarea");
    const msgerInput = get(".msger-input");
    const msgerChat = get(".msger-chat");


    const BOT_IMG = "{{ url_for('static', filename='img/logo.png') }}";
    const PERSON_IMG = "{{ url_for('static', filename='img/user.png') }}";
    const BOT_NAME = "Bot4Me";
    const PERSON_NAME = "Utente X";

    const handleMessageChange = (e) =>{
      setMessage(e.target.value)
    }

    const handleApiKeyChange = (e) => {
      setApiKey(e.target.value)
    }
    
    const saveApiKey = () => {
      if(inputApiKey.current.value !== null){
        setApiKey(inputApiKey.current.value);
      }
      changeHidden()
    }

    const changeHidden = () => {
      if(hidden === true){
        setHidden(false);
        if(apikey === "")
          inputApiKey.current.value = "";
        else 
          inputApiKey.current.value = apikey;
      }
      else setHidden(true);
    }

    const onSubmit = () => {
    //   const msgText = msgerInput.value;
    //   if (!msgText) return;
      if (!message) return; 

      appendMessage(PERSON_NAME, PERSON_IMG, "right", message);
      setMessage("")
      botResponse(message);
    };

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
      // Fetch --> localhost:3000/get 
      // Fetch --> localhost:8080/get
      // Bot Response
      
      fetch('http://127.0.0.1:5000/get?msg='+rawText).then(function(response) {
        response.text().then(function(data) {
          if(response.status === 403){
            data = "Non sei autorizzato a visualizzare questo contenuto"
          }
            console.log(rawText);
            console.log(data);
            appendMessage(BOT_NAME, BOT_IMG, "left", data);
        });
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
          <CustomButton text={"API KEY"} isDisabled={false} className={"msger-apikey-btn"} onSubmit={()=>{changeHidden()}}/>
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
                Benvenuto su Bot4Me, sarò il tuo assistente personale 😄
              </div>
              <div className="msg-text">
                  Posso aiutarti a semplificare i tuoi compiti aziendali come: 
                  <ul>
                  <li>Inserire rendiconto ore</li>
                  <li>Registrare la tua presenza in sede</li>
                  <li>Aprire il cancello aziendale</li>
                  <li>E molto altro ... </li>
                  </ul>
                  Mettimi alla prova!
              </div>
              </div>
          </div>

          </main>

          <div className='input-form'>
            <input type="text" ref={inputApiKey} hidden={hidden} className="msger-input" id="apikeyInput" placeholder="Scrivi qui la tua ApiKey..." onChange={handleApiKeyChange}/>
            <CustomButton text={"SALVA API-KEY"}  hidden={hidden} isDisabled={(apikey) === "" ? true : false} onSubmit={()=>{saveApiKey()}} className={"msger-send-btn"}/>  

            <input type="text" hidden={!hidden} className="msger-input" id="textInput" value={message} placeholder="Scrivi qui il tuo messaggio..." onChange={handleMessageChange}/>          
            <CustomButton text={"INVIA MESSAGGIO"}  hidden={!hidden} isDisabled={(message) === "" ? true : false} onSubmit={()=>{onSubmit()}} className={"msger-send-btn"}/>
          </div>
          <AudioRecorder changeMessage={setMessage}/>
        </div>
    )
}

export default Home;