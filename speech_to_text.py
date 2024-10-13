import wave
import sys
import os
import time

from vosk import Model, KaldiRecognizer, SetLogLevel

from trim_wav import trim_wav
from datetime import datetime
import json

# You can set log level to -1 to disable debug messages
SetLogLevel(0)

# Define the root directory of the project
root_dir = os.path.dirname(os.path.abspath(__file__))

# Define relative paths
input_wav_path = os.path.join(root_dir, "output.wav")
trimmed_wav_path = os.path.join(root_dir, "test_trimmed.wav")
model_path = os.path.join(root_dir, "models/vosk-model-small-ca-0.4")

# Start timing
start_time = time.time()

try:
  trim_wav(input_wav_path, trimmed_wav_path, 15, 16)
  wf = wave.open(trimmed_wav_path, "rb")
except FileNotFoundError:
  print("Audio file not found.")
  sys.exit(1)
except wave.Error as e:
  print(f"Error opening audio file: {e}")
  sys.exit(1)

if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
  print("Audio file must be WAV format mono PCM.")
  sys.exit(1)

model = Model(model_path)

wf = wave.open(trimmed_wav_path, "rb")
rec = KaldiRecognizer(model, wf.getframerate())
rec.SetWords(True)
rec.SetPartialWords(True)

output_text_path = os.path.join(root_dir, "transcription.txt")

# Generate a unique filename based on the current date and time
current_time = datetime.now().strftime("%Y%m%d%H%M%S")
output_text_path = os.path.join(root_dir, f"transcription_{current_time}.txt")

with open(output_text_path, "a") as f:
  while True:
    data = wf.readframes(4000)
    if len(data) == 0:
      break
    if rec.AcceptWaveform(data):
      result = json.loads(rec.Result())
      if "text" in result:
        f.write(result["text"] + "\n")

  final_result = json.loads(rec.FinalResult())
  if "text" in final_result:
    f.write(final_result["text"] + "\n")

# End timing
end_time = time.time()

# Print execution duration
execution_duration = end_time - start_time
print(f"Execution duration: {execution_duration:.2f} seconds")