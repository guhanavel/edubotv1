from speechmatics.models import ConnectionSettings
from speechmatics.batch_client import BatchClient
from httpx import HTTPStatusError 
from pydub import AudioSegment

AUTH_TOKEN = "b7ENbt67bMnZ70C0qd9xge8SQdSL9IiV"
def new_speech_to_text(file):
    # Load the audio file
    
    audio = AudioSegment.from_file(file)

    # Specify the output filename with the .mp3 extension
    output_filename = "output.wav"

    # Export the audio as an MP3 file
    audio.export(output_filename, format="wav")




    PATH_TO_FILE = "output.wav"
    LANGUAGE = "ko"
    print("help")
    settings = ConnectionSettings(
        url="https://asr.api.speechmatics.com/v2",
        auth_token=AUTH_TOKEN,
    )

    # Define transcription parameters
    conf = {
        "type": "transcription",
        "transcription_config": { 
            "language": LANGUAGE,
            # Find out more about entity detection here:
            # https://docs.speechmatics.com/features/entities#enable-entity-metadata
            "enable_entities": True,
            "additional_vocab":[]
        },
    }

    # Open the client using a context manager
    with BatchClient(settings) as client:
        try:
            job_id = client.submit_job(
                audio=PATH_TO_FILE,
                transcription_config=conf,
            )
            print(f"job {job_id} submitted successfully, waiting for transcript")

            # Note that in production, you should set up notifications instead of polling. 
            # Notifications are described here: https://docs.speechmatics.com/features-other/notifications
            transcript = client.wait_for_completion(job_id, transcription_format="txt")
            # To see the full output, try setting transcription_format="json-v2".
            return transcript
        except HTTPStatusError:
            return "Invalid API key - Check your AUTH_TOKEN at the top of the code!"
  