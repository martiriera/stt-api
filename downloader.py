import requests
from pydub import AudioSegment
from io import BytesIO
import os

def download_mp3(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        audio = AudioSegment.from_mp3(BytesIO(response.content))
        print(f"Audio length: {len(audio)} milliseconds")
        print(f"Channels: {audio.channels}, Frame rate: {audio.frame_rate}")

        half_point = len(audio) // 2
        second_half_audio = audio[half_point:]

        # Create directory if it does not exist
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        second_half_audio.export(filename, format="mp3")

    else:
        print("Failed to download the audio file.")

def getIdFromUrl(url):
    try:
        id = url.split('/')[-2]
        return id
    except Exception as e:
        print(f"An error occurred for url {url}: {e}")
        return "unknown_id"
