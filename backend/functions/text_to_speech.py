import requests
from decouple import config

NARAKEET_KEY = config("NARAKEET")


#Convert Text to Speech

def convert_text_to_speech(message):
    voice = 'Seo-Yeon'
    
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