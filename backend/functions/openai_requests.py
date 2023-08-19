import openai
from decouple import config
import whisper
from pydub import AudioSegment


from functions.database import get_recent_messages
from functions.prompt import LANGUAGE




# Retrieve Enviornment Variables
openai.organization = config("OPEN_AI_ORG")
openai.api_key = config("OPEN_AI_KEY")
model = whisper.load_model("base")

# Open AI - Whisper
# Convert audio to text
def convert_audio_to_text(audio_file):
  try:
    # Load the audio file
    
    audio = AudioSegment.from_file(audio_file)

    # Specify the output filename with the .mp3 extension
    output_filename = "output.mp3"

    # Export the audio as an MP3 file
    audio.export(output_filename, format="mp3")

    # load audio and pad/trim it to fit 30 seconds
    audio = whisper.load_audio("output.mp3")
    audio = whisper.pad_or_trim(audio)

    # make log-Mel spectrogram and move to the same device as the model
    mel = whisper.log_mel_spectrogram(audio).to(model.device)

    # decode the audio
    options = whisper.DecodingOptions(language = LANGUAGE, fp16 = False)
    # get the transcribe
    result = whisper.decode(model, mel, options)


    #transcript = openai.Audio.transcribe("whisper-1", audio_file)
    #message_text = transcript["text"]

    return result.text
  except Exception as e:
    return "Error"

# Open AI - Chat GPT
def get_chat_response(message_input):

  messages = get_recent_messages()
  user_message = {"role": "user", "content": message_input }
  messages.append(user_message)
  #print(messages)

  try:
    response = openai.ChatCompletion.create(
      model="gpt-4",
      messages=messages
    )
    #print(response)
    message_text = response["choices"][0]["message"]["content"]
    return message_text
  except Exception as e:
    print(e)
    return

def get_chat_evaluation(message_input):

  messages = get_recent_messages()
  user_message = {"role": "user", "content": message_input }
  messages.append(user_message)
  #print(messages)

  try:
    response = openai.ChatCompletion.create(
      model="gpt-4",
      messages=messages
    )
    #print(response)
    message_text = response["choices"][0]["message"]["content"]
    return message_text
  except Exception as e:
    print(e)
    return