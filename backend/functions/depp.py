from deepgram import Deepgram


async def main():
    dg_client = Deepgram('b7b4fbb9f7787221b075cb6a1e232ed9df172f0d')
    with open(PATH_TO_FILE, 'rb') as audio:
        source = {'buffer': audio, 'mimetype': MIMETYPE_OF_FILE}
    response = await dg_client.transcription.prerecorded(source, {'punctuate': True})