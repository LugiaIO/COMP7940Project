import google.cloud.texttospeech as tts
from google.oauth2 import service_account

import os
import json


with open("sample.json", "w") as outfile:
    json.dump(json.loads(os.environ["TTS"]), outfile)

credentials = service_account.Credentials.from_service_account_file("sample.json")


def textToWav(voice_name: str, text: str, movie_name: str, username: str):
    """
    Convert text to WAV audio using Google Cloud Text-to-Speech API.

    Args:
        voice_name (str): The name of the voice to use.
        text (str): The text to convert to speech.
        movie_name (str): The name of the movie associated with the text.
        username (str): The username associated with the text.

    Returns:
        None. The generated speech is saved to a WAV file.
    """
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

    filename = f"{movie_name}_{username}.wav"
    with open(filename, "wb") as out:
        out.write(response.audio_content)
        print(f'Generated speech saved to "{filename}"')
