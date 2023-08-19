import { useEffect, useState } from "react";
import Title from "./Title";
import axios from "axios";
import RecordMessage from "./RecordMessage";
import Next from "./Next";

const Convo = () => {
  // initial state
  const [isLoading, setIsLoading] = useState(false);
  const [messages, setMessages] = useState<any[]>([]);
  const [preamble, setPreamble] = useState<string>("");


  // create function called createBlobUrl to convert any audio to Blob
  function createBlobURL(data: any) {
    const blob = new Blob([data], { type: "audio/mpeg" });
    const url = window.URL.createObjectURL(blob);
    return url;
  }

  // need to create a function or method to display the inital question 

  

  
  
  useEffect(() => {
    const fetchData = async () => {
      try {
        setIsLoading(true);
        const response_text = await fetch('http://localhost:8000/start-question-text');
        const response_audio = await fetch('http://localhost:8000/start-question-voice');
        const preambleResponse = await fetch('http://localhost:8000/conversation-preamble');
        const preambleData = await preambleResponse.json();
        setPreamble(preambleData.text);
        const data = await response_text.json();
        const blob = await response_audio.blob();
        const audio = new Audio();
        audio.src = createBlobURL(blob);
        const initialMessage = { sender: "edubot", blobUrl: audio.src, text: data.text };
        const newMessageArr = [...messages, initialMessage];
        setMessages(newMessageArr);
        setIsLoading(false);
        audio.play();
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };
  
    fetchData();
  }, []);
 


  // when the recording stops, infomation will start processing here
  const handleStop = async (blobUrl: string) => {
    setIsLoading(true);

    // convert blob url to blob object
    fetch(blobUrl)
      .then((res) => res.blob())
      .then(async (blob) => {
        // Construct audio to send file
        const formData = new FormData();
        formData.append("file", blob, "myFile.wav");
        
        // Send audio file --> post-audio endpoint (to get audio text)
        const { data:text } = await axios.post<string>("http://localhost:8000/get-user-audio", formData, {
          headers: {
            "Content-Type": "audio/mpeg",
          },
        });
        // Append the received text to edubot message
        const myMessage = {sender: "me", blobUrl, text}
        const newMessageArr = [...messages,myMessage]
        setMessages(newMessageArr)

        //set the formdata for GPTResponse
        const formtext = new FormData();
        formtext.append("message_decode", text);

        // send the my text to get GPTresponse
        const { data:gpt } = await axios.post<string>("http://localhost:8000/post-audio", formtext, {
          headers: {
            "Content-Type": 'multipart/form-data',
          },
        });
        //Append gpt text to edubot message
        const formDat = new FormData();
        formDat.append("chat_response", gpt);


        // send form data to api endpoint
        await axios
          .post("http://localhost:8000/post-audio-2",formDat, {
            headers: {
              "Content-Type": 'multipart/form-data',
            },
            responseType: "arraybuffer", // Set the response type to handle binary data
          })
          .then((res: any) => {
            const blob = res.data;
            const audio = new Audio();
            audio.src = createBlobURL(blob);

            // Append to audio
            const eduMessage = { sender: "edubot", blobUrl: audio.src, text:gpt };
            newMessageArr.push(eduMessage);
            setMessages(newMessageArr);

            // Play audio
            setIsLoading(false);
            audio.play();
          })
          .catch((err: any) => {
            console.error(err);
            setIsLoading(false);
          });
      });
  };

  

  return (
    
    <div className="h-screen overflow-y-hidden">
      {/* Title */}
      <Title setMessages={setMessages} />
      <h1>{preamble}</h1>
      

      <div className="flex flex-col justify-between h-full overflow-y-scroll pb-96">
        {/* Conversation */}
        <div className="mt-5 px-5">
        
  
          {messages?.map((audio, index) => {
  return (
    <div
      key={index + audio.sender}
      className={
        "flex flex-col " +
        (audio.sender == "me" ? "flex items-end" : "")
      }
    >
      
      {/* Sender */}
      <div className="mt-4">
        
        <p
          className={
            audio.sender == "me"
              ? "text-left mr-2 italic text-green-500"
              : "ml-2 italic text-blue-500"
          }
        >
          {audio.sender}
        </p>

        {/* Message */}
        <audio
          src={audio.blobUrl}
          className="appearance-none"
          controls
        />
        <button className = "bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-full">More Infor</button>
      </div>
      

      {/* Text Message */}
      <div className="mt-4">
        <p>{audio.text}</p>
      </div>
    </div>
  );
})}
          {messages.length == 0 && !isLoading && (
            <div className="text-center font-light italic mt-10">
              Send Edubot a message...
            </div>
          )}

          {isLoading && (
            <div className="text-center font-light italic mt-10 animate-pulse">
              Gimme a few seconds...
            </div>
          )}
        </div>

        {/* Recorder */}
        <div className="fixed bottom-0 w-full py-6 border-t text-center bg-gradient-to-r from-sky-500 to-green-500">
          <div className="flex justify-center items-center w-full">
            <div>
              <RecordMessage handleStop={handleStop} />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Convo;