import MicRecorder from "mic-recorder-to-mp3";
import { useEffect, useState, useRef } from "react";
import axios from "axios";
import CustomButton from "./CustomButton";
import LoadingSpinner from "./LoadingSpinner";

// Set AssemblyAI Axios Header
const assemblyAI = axios.create({
  baseURL: "https://api.assemblyai.com/v2",
  headers: {
    authorization: "d558677a79ad45ccaf2204170bf00e16",
    "content-type": "application/json",
  },
});

const AudioRecorder = ({ changeMessage, hidden }) => {
  // Mic-Recorder-To-MP3
  const recorder = useRef(null); //Recorder
  const [blobURL, setBlobUrl] = useState(null);
  const [audioFile, setAudioFile] = useState(null);
  const [isRecording, setIsRecording] = useState(null);

  useEffect(() => {
    //Declares the recorder object and stores it inside of ref
    recorder.current = new MicRecorder({ bitRate: 128 });
  }, []);

  const startRecording = () => {
    /*
      ---
      Function Name :  startRecording
      ---
      - Args → 
      - Description → funzione che si occupa dell'avvio della registrazione del messaggio vocale, richiedendo l'autorizzazione per l'utilizzo del microfono e iniziando la registrtazione. 
      - Returns → 
    */
    changeMessage("Sto registrando ...");
    // Check if recording isn't blocked by browser
    if (recorder.current) {
      recorder.current.stop();
      recorder.current.start().then(() => {
        setIsRecording(true);
      });
    }
  };

  const stopRecording = () => {
    /*
      ---
      Function Name :  stopRecording
      ---
      - Args → 
      - Description → funzione che si occupa della gestione della fine della registrazione del messaggio vocale e successiva creazione del file audio in formato mp3. 
      - Returns → 
    */
    changeMessage("Sto traducendo il tuo messaggio ...");
    recorder.current
      .stop()
      .getMp3()
      .then(([buffer, blob]) => {
        const file = new File(buffer, "audio.mp3", {
          type: blob.type,
          lastModified: Date.now(),
        });
        const newBlobUrl = URL.createObjectURL(blob);
        setBlobUrl(newBlobUrl);
        setIsRecording(false);
        setAudioFile(file);
        if (audioFile) {
          setIsLoading(true);
        }
      })
      .catch((e) => console.log(e));
  };

  const resetAudio = () => {
    setAudioFile(null);
    setBlobUrl(null);
    setTranscriptID("");
    setTranscriptData("");
    setUploadURL("");
  };

  // AssemblyAI

  // States
  const [uploadURL, setUploadURL] = useState("");
  const [transcriptID, setTranscriptID] = useState("");
  const [transcriptData, setTranscriptData] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  // Upload the Audio File and retrieve the Upload URL
  useEffect(() => {
    /*
      ---
      Function Name :  useEffect
      ---
      - Args → 
      - Description → funzione innescata in seguito ad un cambiamento avvenuto alla variabile audioFile, effettua l'upload del file stesso presso il servizio esterno AssemblyAI.
      - Returns → 
    */
    if (audioFile) {
      assemblyAI
        .post("/upload", audioFile)
        .then((res) => setUploadURL(res.data.upload_url))
        .catch((err) => console.error(err));
    }
  }, [audioFile]);

  const submitTranscriptionHandler = () => {
    /*
      ---
      Function Name :  submitTranscriptionHandler
      ---
      - Args → 
      - Description → funzione che richiede l'effettuazione della trascrizione sul file audio precedentemente caricato, ottendo l'id della trascrizione nella variabile transcriptID.
      - Returns → 
    */
    if (audioFile && uploadURL !== "") {
      assemblyAI
        .post("/transcript", {
          audio_url: uploadURL,
          language_code: "it",
        })
        .then((res) => {
          setTranscriptID(res.data.id);
          checkStatusHandler();
        });
    }
  };

  const checkStatusHandler = async () => {
    /*
      ---
      Function Name :  checkStatusHandler
      ---
      - Args → 
      - Description → funzione asincrona che attende che il servizio esterno completi la trascrizione del file audio inviato. 
      - Returns → 
    */
    setIsLoading(true);
    try {
      if (transcriptID !== "") {
        await assemblyAI.get(`/transcript/${transcriptID}`).then((res) => {
          if (res.data.text !== null) {
            setTranscriptData(res.data);
            changeMessage(res.data.text);
            setIsLoading(false);
            resetAudio();
          }
        });
      }
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    const interval = setInterval(() => {
      if (transcriptData.status !== "completed" && isLoading) {
        checkStatusHandler();
      } else if (audioFile && uploadURL !== "") {
        submitTranscriptionHandler();
        clearInterval(interval);
      }
    }, 1000);
    return () => clearInterval(interval);
  });

  return (
    <div className="audio-form">
      {isLoading ? (
        <LoadingSpinner />
      ) : (
        <CustomButton
          text={!isRecording ? "Registra" : "Ferma"}
          onSubmit={() => (isRecording ? stopRecording() : startRecording())}
          className={!isRecording ? "msger-rec-start" : "msger-rec-stop"}
          hidden={hidden}
          icon="Rec"
        />
      )}
    </div>
  );
};

export default AudioRecorder;
