#uvicorn main:app
#uvicorn main:app --reload

# Main imports
from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from decouple import config
from functions.prompt import PROMPT,QNS_1,VOICE
from pydantic import BaseModel



# Custom function imports
from functions.text_to_speech import convert_text_to_speech
from functions.openai_requests import convert_audio_to_text, get_chat_response, get_chat_evaluation
from functions.database import store_messages, reset_messages
from functions.speechnew import new_speech_to_text

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


##############################################################
#                                                            #
#                                                            #
#                       DONT TOUCH                           #
#                                                            #
#                                                            #
##############################################################

# Check health (API)
@app.get("/health")
async def check_health():
    return {"response": "healthy"}

#Reset Message
@app.get("/reset")
async def reset_conversation():
    reset_messages()
    return {"response": "conversation reset", "text":QNS_1}

#application/octet-stream
#audio/mpeg

##############################################################
#                                                            #
#                                                            #
#                       Jeadok Method                        #
#                                                            #
#                                                            #
##############################################################
# Summary 
# In level 0, the user will repeat after the user to practice their pronouncation


prouncation_list =  [{'id':1,'text':'안녕하세요'},{'id':2,'text':'이것은 뭐예요'},{'id':3,'text':'안녕히'}]

class Pronounciation(BaseModel):
    id : int
    word : str

# text of what you want to say
@app.get("/level-0-text/")
async def send_pronoun_text(request: Pronounciation):
    return {'id':1,'text':'안녕하세요'}

# audio of the right pronouncation 
@app.get("/level-0-voice/")
async def send_pronoun_voice():
    # Audio for question 
    audio_output = convert_text_to_speech(VOICE,'안녕하세요')

    #Guard: Ensure message decoded
    if not audio_output:
        return HTTPException(status_code=400, detail="Failed to get response")

    # Create a generator that yields chunks of data
    def iterfile():
        yield audio_output

    # Return output audio
    return StreamingResponse(iterfile(), media_type="application/octet-stream")

# text of what you want to say
@app.get("/level-0-text1/")
async def send_pronoun_text(request: Request):
    return {'id':1,'text':'이것은 뭐예요'}

# audio of the right pronouncation 
@app.get("/level-0-voice1/")
async def send_pronoun_voice():
    # Audio for question 
    audio_output = convert_text_to_speech(VOICE,'이것은 뭐예요')

    #Guard: Ensure message decoded
    if not audio_output:   
        return HTTPException(status_code=400, detail="Failed to get response")

    # Create a generator that yields chunks of data
    def iterfile():
        yield audio_output

    # Return output audio
    return StreamingResponse(iterfile(), media_type="application/octet-stream")

# convert audio to text for user input
@app.post("/get-user-pronoun/")
async def get_audio(file: UploadFile = File(...)):
    
    #Get saved audio
    #audio_input = open("myFile.mp3", "rb")

    #Save file from frontend
    with open(file.filename, "wb") as buffer:
        buffer.write(file.file.read())
    #audio_input = open(file.filename, "rb")

    #Decode audio
    #message_decode = prounce("안녕하세요",file.filename)
    message_decode = new_speech_to_text(file.filename)

    # Guard: Ensure decoded
    if not message_decode:
        return "Error"
    # HTTPException(status_code=400, detail="Failed to decode audio")
    return message_decode 

##############################################################
##############################################################
##############################################################
#####################Simulated Conversation###################
##############################################################
##############################################################
##############################################################
# Level 3 is a simulated conversation 
# convert audio to text for user input

#conversation preamble
@app.get("/conversation-preamble")
async def send_preamble():
    return {"text": "You are having an simulated conversation where your job is testing"}

#conversation starter by edubot
@app.get("/start-question-text/")
async def send_starter_text():
    return {"text":QNS_1}

#initalize voice
@app.get("/start-question-voice/")
async def send_starter_voice():
    text = QNS_1
    audio_output = convert_text_to_speech(VOICE,text)
    #Guard: Ensure message decoded
    if not audio_output:
        return HTTPException(status_code=400, detail="Failed to get chat response")

    # Create a generator that yields chunks of data
    def iterfile():
        yield audio_output

    # Return output audio
    return StreamingResponse(iterfile(), media_type="application/octet-stream")




#Getting user input 
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
        return "Error"
    # HTTPException(status_code=400, detail="Failed to decode audio")
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

    print("GPT:" + get_chat_evaluation(message_decode))
    

    return chat_reponse 


##file: UploadFile = File(...)

# get chatgpt audio response
@app.post("/post-audio-2/")
async def get_audio2(request: Request):
    
    form = await request.form()
    chat_response = form.get("chat_response")
    
    #convert chat response to audio
    audio_output = convert_text_to_speech(VOICE,chat_response.split("###")[0])
    print(chat_response.split("###"))

    #Guard: Ensure message decoded
    if not audio_output:
        return HTTPException(status_code=400, detail="Failed to get chat response")

    # Create a generator that yields chunks of data
    def iterfile():
        yield audio_output

    # Return output audio
    return StreamingResponse(iterfile(), media_type="application/octet-stream")

