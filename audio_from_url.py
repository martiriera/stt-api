import requests
from pydub import AudioSegment
from io import BytesIO

# Function to download and play an MP3 file from a URL
def download_and_read_mp3(url, wav_convert=False):
    # Download the audio file
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Load the audio into an AudioSegment object
        audio = AudioSegment.from_mp3(BytesIO(response.content))

        # Get information about the audio
        print(f"Audio length: {len(audio)} milliseconds")
        print(f"Channels: {audio.channels}, Frame rate: {audio.frame_rate}")

        if wav_convert:
            # Convert the audio to WAV format with a sampling frequency of 16k
            audio = audio.set_frame_rate(16000)
            audio.export("output.wav", format="wav")

        return audio
    else:
        print("Failed to download the audio file.")
        return None

# Example usage
mp3_url = "https://traffic.omny.fm/d/clips/47dc05c7-7279-4c6f-9b31-ae74013297d9/e4e46f35-5cd4-49e0-b007-af030077c851/563da055-9bb2-46cd-aa1c-b1540104644e/audio.mp3?dist=RSS"  # Replace with your actual URL
download_and_read_mp3(mp3_url)
