import MicRecorder from "mic-recorder-to-mp3"
import { useEffect, useState, useRef } from "react"
import axios from "axios"
import CustomButton from "./CustomButton"
import LoadingSpinner from "./LoadingSpinner"

// Set AssemblyAI Axios Header
const assemblyAI = axios.create({
  baseURL: "https://api.assemblyai.com/v2",
  headers: {
    authorization: "d558677a79ad45ccaf2204170bf00e16",
    "content-type": "application/json",
    "transfer-encoding": "chunked",
  },
})

const AudioRecorder = ({changeMessage, hidden}) => {
  // Mic-Recorder-To-MP3
  const recorder = useRef(null) //Recorder
  const [blobURL, setBlobUrl] = useState(null)
  const [audioFile, setAudioFile] = useState(null)
  const [isRecording, setIsRecording] = useState(null)

  useEffect(() => {
    //Declares the recorder object and stores it inside of ref
    recorder.current = new MicRecorder({ bitRate: 128 })
  }, [])

  const startRecording = () => {
    changeMessage("Sto registrando ...")
    // Check if recording isn't blocked by browser
    recorder.current.stop()
    recorder.current.start().then(() => {
      setBlobUrl("")
      setAudioFile(null)
      setIsRecording(true)
    })
  }

  const stopRecording = () => {
    changeMessage("Sto traducendo il tuo messaggio ...")
    recorder.current
      .stop()
      .getMp3()
      .then(([buffer, blob]) => {
        const file = new File(buffer, "audio.mp3", {
          type: blob.type,
          lastModified: Date.now(),
        })
        const newBlobUrl = URL.createObjectURL(blob)
        setBlobUrl(newBlobUrl)
        setIsRecording(false)
        setAudioFile(file)
      })
      .catch((e) => console.log(e))
  }
  
  const resetAudio = () => {
    setAudioFile(null)
    setBlobUrl(null)
    setTranscriptID("")
    setTranscriptData("")
    setUploadURL("")
  }

  // AssemblyAI

  // States
  const [uploadURL, setUploadURL] = useState("")
  const [transcriptID, setTranscriptID] = useState("")
  const [transcriptData, setTranscriptData] = useState("")
  const [isLoading, setIsLoading] = useState(false)

  // Upload the Audio File and retrieve the Upload URL
  useEffect(() => {
    if (audioFile) {
      assemblyAI
        .post("/upload", audioFile)
        .then((res) => setUploadURL(res.data.upload_url))
        .catch((err) => console.error(err))
    }
    console.log(audioFile)
  }, [audioFile])

  // Submit the Upload URL to AssemblyAI and retrieve the Transcript ID
  const submitTranscriptionHandler = () => {
    if(audioFile){
      assemblyAI
        .post("/transcript", {
          audio_url: uploadURL,
          language_code: "it"
        })
        .then((res) => {
          setTranscriptID(res.data.id)
          checkStatusHandler()
        })
      }
  }

  // Check the status of the Transcript
  const checkStatusHandler = async () => {
    setIsLoading(true)
    try {
      if(transcriptID!==""){
        await assemblyAI.get(`/transcript/${transcriptID}`).then((res) => {
          if(res.data.text !== null){
            setTranscriptData(res.data)
            changeMessage(res.data.text)
            console.log("CIAO STO SCRIVENDO TRANSCRIPT"+res.data.text)
          }
        })
      }
    } catch (err) {
      console.error(err)
    }
  }

  //Periodically check the status of the Transcript
  useEffect(() => {
    const interval = setInterval(() => {
      if (transcriptData.status !== "completed" && isLoading) {
        checkStatusHandler()
      } else {
        submitTranscriptionHandler()
        resetAudio()        
        setIsLoading(false)
        clearInterval(interval)  
      }
    },1000)
    return () => clearInterval(interval)
  })

  return (
      <div className="audio-form">
       <CustomButton text={(!isRecording ? "Registra" : "Ferma")} 
       onSubmit={()=> isRecording ? stopRecording() : startRecording()} className={!isRecording? "msger-rec-start":"msger-rec-stop"} hidden={hidden} icon="Rec"/>

      <LoadingSpinner hidden={isLoading}/>
    </div>
  )
}

export default AudioRecorder