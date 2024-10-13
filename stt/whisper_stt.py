import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
import time

def transcribe(audio_path, model_id):
    start_time = time.time()
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

    model = AutoModelForSpeechSeq2Seq.from_pretrained(
        model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True
    )
    model.to(device)

    processor = AutoProcessor.from_pretrained(model_id)

    pipe = pipeline(
        "automatic-speech-recognition",
        model=model,
        tokenizer=processor.tokenizer,
        feature_extractor=processor.feature_extractor,
        torch_dtype=torch_dtype,
        device=device,
        chunk_length_s=30,
    )

    result = pipe(audio_path, return_timestamps=True)

    end_time = time.time()
    duration = end_time - start_time
    return result["text"], duration