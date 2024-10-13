import downloader
from stt.whisper_stt import transcribe
import os
from datetime import datetime

def execute():
  root_path = os.path.dirname(__file__)

  try:
    print("Downloading audio...")
    mp3_url = "https://traffic.omny.fm/d/clips/47dc05c7-7279-4c6f-9b31-ae74013297d9/e4e46f35-5cd4-49e0-b007-af030077c851/563da055-9bb2-46cd-aa1c-b1540104644e/audio.mp3?dist=RSS"
    id = downloader.getIdFromUrl(mp3_url)

    audio_path = os.path.join(root_path, 'tmp', f'audio_{id}.mp3')

    downloader.download_mp3(mp3_url, audio_path)
    print("Audio downloaded")

    print("Transcribing audio...")
    transcription, duration = transcribe(audio_path, "openai/whisper-large-v3-turbo")
    print(f"Transcription complete. Duration: {duration:.2f} seconds.")

    print("Storing transcription...")
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    output_path = os.path.join(os.path.dirname(__file__), 'transcriptions', f'transcription_{timestamp}.md')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as file:
      file.write(transcription)
    print(f"Transcription stored at {output_path}")

    if os.path.exists(audio_path):
      os.remove(audio_path)
      print(f"Deleted the source file: {audio_path}")
    else:
       print(f"The file does not exist: {audio_path}")

  except Exception as e:
    print(f"An error occurred: {e}")

if __name__ == "__main__":
  execute()