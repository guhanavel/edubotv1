import requests
from decouple import config
from functions.prompt import VOICE

from pydub import AudioSegment

NARAKEET_KEY = config("NARAKEET")


#Convert Text to Speech

def convert_text_to_speech(voice,message):

    voice = voice
    
    options = {
        'headers': {
            'Accept': 'application/octet-stream',
            'Content-Type': 'text/plain',
            'x-api-key': NARAKEET_KEY,
        },
        'data': message.encode('utf8')
    }

    url = f'https://api.narakeet.com/text-to-speech/m4a?voice={voice}'
    # Send request
    try:
        reponse = requests.post(url, **options)
    except Exception as e:
        return
    
    #Handle request
    if reponse.status_code == 200:
        return reponse.content
    else:
        return 

def convert_text_to_speech_level2(message):
    # create empty audio file as placeholder
    text_to_speech = AudioSegment.empty()
    # iterate through the message
    for mes in message:
        # save audio to a tempo.wav file
        with open('tempo.wav', 'wb') as f:
            f.write(convert_text_to_speech(mes["role"],mes["content"]))
        sound1 = AudioSegment.from_file("tempo.wav")
        text_to_speech += sound1
    text_to_speech.export("text_to_speech.wav")
    
    
    
            
 