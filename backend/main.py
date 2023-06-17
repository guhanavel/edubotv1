#uvicorn main:app
#uvicorn main:app --reload

# Main imports
from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from decouple import config
import openai

# Custom function imports
from functions.text_to_speech import convert_text_to_speech
from functions.openai_requests import convert_audio_to_text, get_chat_response
from functions.database import store_messages, reset_messages


response = ""

# Initiate
app = FastAPI()


# CORS - Origins
origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:4173",
    "http://localhost:3000",
]


# CORS - Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Check health (API)
@app.get("/health")
async def check_health():
    return {"response": "healthy"}

#Reset Message
@app.get("/reset")
async def reset_conversation():
    reset_messages()
    return {"response": "conversation reset", "text":"안녕하세요 이름이 뭐예요? (Annyeonghaseyo, ireumi mwoyeyo?)" }

# convert audio to text for user input
@app.post("/get-user-audio/")
async def get_audio(file: UploadFile = File(...)):
    
    #Get saved audio
    #audio_input = open("myFile.mp3", "rb")

    #Save file from frontend
    with open(file.filename, "wb") as buffer:
        buffer.write(file.file.read())
    audio_input = open(file.filename, "rb")

    #Decode audio
    message_decode = convert_audio_to_text(audio_input)

    # Guard: Ensure decoded
    if not message_decode:
        return HTTPException(status_code=400, detail="Failed to decode audio")
    return message_decode

# get chatgpt response
@app.post("/post-audio/")
async def get_audio(request: Request):
    
    form = await request.form()
    message_decode = form.get("message_decode")
    
    #Get ChatGPT Response
    chat_reponse = get_chat_response(message_decode)
    
    #Guard: Ensure message decoded
    if not chat_reponse:
        return HTTPException(status_code=400, detail="Failed to get chat response")
    
    #Store Messages
    store_messages(message_decode, chat_reponse)
    

    return chat_reponse


##file: UploadFile = File(...)

# get chatgpt audio response
@app.post("/post-audio-2/")
async def get_audio2(request: Request):
    
    form = await request.form()
    chat_response = form.get("chat_response")
    
    #convert chat response to audio
    audio_output = convert_text_to_speech(chat_response.split("(")[0])
    print(type(chat_response))

    #Guard: Ensure message decoded
    if not audio_output:
        return HTTPException(status_code=400, detail="Failed to get chat response")

    # Create a generator that yields chunks of data
    def iterfile():
        yield audio_output

    # Return output audio
    return StreamingResponse(iterfile(), media_type="application/octet-stream")
#application/octet-stream
#audio/mpeg

#initalize text
@app.get("/start-question-text/")
async def send_starter_text():
    return {"text":"안녕하세요 이름이 뭐예요? (Annyeonghaseyo, ireumi mwoyeyo?)"}

#initalize voice
@app.get("/start-question-voice/")
async def send_starter_voice():
    text = "안녕하세요 이름이 뭐예요?"
    audio_output = convert_text_to_speech(text)
    #Guard: Ensure message decoded
    if not audio_output:
        return HTTPException(status_code=400, detail="Failed to get chat response")

    # Create a generator that yields chunks of data
    def iterfile():
        yield audio_output

    # Return output audio
    return StreamingResponse(iterfile(), media_type="application/octet-stream")
    