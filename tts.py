import google.cloud.texttospeech as tts
from google.oauth2 import service_account

import os
import json


with open("sample.json", "w") as outfile:
    json.dump(json.loads(os.environ["TTS"]), outfile)

credentials = service_account.Credentials.from_service_account_file('sample.json')

def textToWav(voice_name: str, text: str):
    language_code = "-".join(voice_name.split("-")[:2])
    text_input = tts.SynthesisInput(text=text)
    voice_params = tts.VoiceSelectionParams(
        language_code=language_code, name=voice_name
    )
    audio_config = tts.AudioConfig(audio_encoding=tts.AudioEncoding.LINEAR16)

    client = tts.TextToSpeechClient(credentials=credentials)
    response = client.synthesize_speech(
        input=text_input,
        voice=voice_params,
        audio_config=audio_config,
    )

    filename = f"{voice_name}.wav"
    with open(filename, "wb") as out:
        out.write(response.audio_content)
        print(f'Generated speech saved to "{filename}"')
        
textToWav("en-GB-Neural2-B", "What is the temperature in London?")