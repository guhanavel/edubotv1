#uvicorn main:app
#uvicorn main:app --reload

# Main imports

import anvil.server
import anvil.tables as tables

anvil.server.connect("server_QSDZAW25TAFF6KM4NISXHLS4-FQM4NI4B5WTJ4ZS7")
import anvil.files
from anvil.files import data_files
import anvil.secrets
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from decouple import config


# Custom function imports
from functions.text_to_speech import convert_text_to_speech
from functions.openai_requests import convert_audio_to_text, get_chat_response
from functions.database import store_messages, reset_messages
from functions.translate import translator
from functions.pronounciation import prounce
from functions.speechnew import new_speech_to_text
from functions.prompt import PROMPT,QNS_1,VOICE


##############################################################
#                                                            #
#                                                            #
#                       LEVEL 0                              #
#                                                            #
#                                                            #
##############################################################
# Summary 
# In level 0, the user will repeat after the user to practice their pronouncation

# text of what you want to say
@anvil.server.callable
def send_pronoun_text():
    return {"text":"안녕하세요"}

# convert audio to text for user input
@anvil.server.callable
def get_audio_1():
    
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
#                                                            #
#                                                            #
#                       LEVEL 1                              #
#                                                            #
#                                                            #
##############################################################
# Summary
# Level 1 is a level where users will practise their listening skills by listening to a scenario and then answer questions based on that by speaking to the bot.
#initalize scence
@anvil.server.callable
def send_starter_text():
    text = QNS_1 + " " + translator(QNS_1)
    return {"text":"Scene: Jack and Lisa are planning for their friend Minji's birthday party."}


#LEVEL = [{"role":"Seo-Yeon","content":"리사야, 우리 민지의 생일파티를 준비하자"},{"role":"Min-Ho","content":"좋아, 우리 뭐 할까?"}]
#initalize voice

# Set the different level Questions

# question voice
@anvil.server.callable
def send_question_voice():
    # Get the question 
    # For testing, the question will be here
    #QUESTION_COUNT += 1
    QUESTION = "잭과 리사는 무엇을 계획하고 있나요?"
    # Audio for question 
    audio_output = convert_text_to_speech(VOICE,QUESTION)

    #Guard: Ensure message decoded
    if not audio_output:
        return HTTPException(status_code=400, detail="Failed to get chat response")

    # Create a generator that yields chunks of data
    def iterfile():
        yield audio_output

    # Return output audio
    return StreamingResponse(iterfile(), media_type="application/octet-stream")

# question in text
@anvil.server.callable
def send_question_text():
    QUESTION = "잭과 리사는 무엇을 계획하고 있나요?"
    return QUESTION



##############################################################
#                                                            #
#                                                            #
#                       LEVEL 2                              #
#                                                            #
#                                                            #
##############################################################
# Level 2 is a an example driven level where the user is required to transalte something based in the example we give him




##############################################################
#                                                            #
#                                                            #
#                       LEVEL 3                              #
#                                                            #
#                                                            #
##############################################################
# Level 3 is a simulated conversation 
# convert audio to text for user input



# get chatgpt response
@anvil.server.callable
def get_audio_3(message_decode):

    
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
@anvil.server.callable
def get_audio2(chat_response):
    
    
    #convert chat response to audio
    audio_output = convert_text_to_speech(VOICE,chat_response.split("(")[0])
    print(type(chat_response))

    #Guard: Ensure message decoded
    if not audio_output:
        return HTTPException(status_code=400, detail="Failed to get chat response")

    # Create a generator that yields chunks of data
    def iterfile():
        yield audio_output

    # Return output audio
    return StreamingResponse(iterfile(), media_type="application/octet-stream")

#initalize text
@anvil.server.callable
def send_starter_text():
    return {"text":QNS_1}

#initalize voice
@anvil.server.callable
def send_stater_voice():
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


##############################################################
#                                                            #
#                                                            #
#                 ANVIL FUNCTIONS                            #
#                                                            #
#                                                            #
##############################################################



@anvil.server.callable
def get_audio(audio):
    
    #Get saved audio
    #audio_input = open("myFile.mp3", "rb")

    #Save file from frontend
    with open("tempo.wav", "wb") as buffer:
        buffer.write(audio.get_bytes())
    audio_input = open("tempo.wav", "rb")

    #Decode audio
    message_decode = new_speech_to_text(audio_input)
    print(message_decode)
    

    # Guard: Ensure decoded
    if not message_decode:
        return "Error"
    # HTTPException(status_code=400, detail="Failed to decode audio")
    return message_decode 

@anvil.server.callable
def send_starter_voice():
   # text = LEVEL
    #convert_text_to_speech_level2(text)
    audio_output = open('text_to_speech.wav', 'rb')
    # Set chunk size
    CHUNK_SIZE = 1024 * 1024  # 1MB
    
    #Guard: Ensure message decoded
    if not audio_output:
        return HTTPException(status_code=400, detail="Failed to get chat response")

    # Create a generator that yields chunks of data
    with audio_output as f:
        data = f.read()

    tts_blob = anvil.BlobMedia('audio/mpeg', data, name = 'audio.mp3')
    

    # Return output audio
    return tts_blob

COUNTER = 1
CACHED = []

@anvil.server.callable
def send_pronoun_voice(CACHED):
    # words for question
    words = app_tables.pronoun.get(id=len(CACHED)+1)
    audio_output = convert_text_to_speech(VOICE,words['text'])

    #Guard: Ensure message decoded
    #with open(audio_output,"wb") as f:
    #    data = f.read()

    words['pronoun'] = anvil.BlobMedia('audio/mpeg', audio_output, name = 'audio.mp3')

    CACHED.append({'bot':True,'user':False,'vis':False,'direction':'left','text': words['text'],'url':words['pronoun'].get_url()})
    #COUNTER += 1
    # Return output audio
    return CACHED

@anvil.server.callable
def user_pronoun(audio,CACHED):
    with open("tempo.wav", "wb") as buffer:
        buffer.write(audio.get_bytes())
    audio_input = open("tempo.wav", "rb")

    #Decode audio
    message_decode = new_speech_to_text(audio_input)
    words = app_tables.pronoun.get(id=COUNTER)
    words['user'] = audio
    CACHED.append({'bot':False,'user':True,'vis':True,'direction':'right','text': message_decode,'url':words['user'].get_url()})
    return CACHED










if __name__ == "__main__":
    try:
        anvil.server.wait_forever()
    except KeyboardInterrupt:
        print("...exiting...")
