import contextlib
import wave

def trim_wav(input_path, output_path, start_min, end_min):
  start_sec = start_min * 60
  end_sec = end_min * 60

  with contextlib.closing(wave.open(input_path, 'rb')) as infile:
    params = infile.getparams()
    framerate = params.framerate
    start_frame = int(framerate * start_sec)
    end_frame = int(framerate * end_sec)
    infile.setpos(start_frame)
    frames = end_frame - start_frame

    with wave.open(output_path, 'wb') as outfile:
      outfile.setparams(params)
      outfile.writeframes(infile.readframes(frames))
