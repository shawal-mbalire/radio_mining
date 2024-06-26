import os
import io
import whisper
import requests
import numpy as np
import noisereduce as nr
from pydub import AudioSegment
from scipy.io.wavfile import read

OUTPUT_DIRECTORY  = "output_chunks"
AUDIO_PATH        = 'downloaded_audio.mp3'
NOISE_REDUCED_DIR = "noise_reduced_chunks"
AUDIO_URL         = "https://storage.googleapis.com/radiofilez/english/saturday/kfm_93_3-2022-11-26_T11.00.01.mp3"

if not os.path.exists(AUDIO_PATH):
    response = requests.get(AUDIO_URL, allow_redirects=True)
    if response.status_code == 200:
        with open(AUDIO_PATH, 'wb') as f:
            f.write(response.content)
        print(f"Audio file downloaded successfully: {AUDIO_PATH}")
    else:print(f"Failed to download audio file: {response.status_code}")

model = whisper.load_model("base")
os.makedirs(OUTPUT_DIRECTORY, exist_ok=True)
os.makedirs(NOISE_REDUCED_DIR, exist_ok=True)

def audiosegment_to_librosawav(segment):
    out_f = io.BytesIO()
    segment.export(out_f, format='wav')
    out_f.seek(0)
    rate, data = read(out_f)
    return rate, data

def transcribe_audio_segment(segment_file_path, model=model):
    result = model.transcribe(segment_file_path)
    return result["text"]

def split_audio_file(AUDIO_PATH, OUTPUT_DIRECTORY, segment_duration_s=150):
    audio = AudioSegment.from_mp3(AUDIO_PATH)
    num_segments = int(audio.duration_seconds / segment_duration_s) + 1
    for i in range(num_segments):
        start_time = i * segment_duration_s * 1000 
        end_time = min((i + 1) * segment_duration_s * 1000, audio.duration_seconds * 1000)
        segment = audio[start_time:end_time]
        segment_file_path = os.path.join(OUTPUT_DIRECTORY, f"segment_{i + 1}.mp3")
        segment.export(segment_file_path, format="mp3")
        rate, data = audiosegment_to_librosawav(segment)
        if segment.channels == 2:  
            data = np.mean(data, axis=1)
        reduced_noise = nr.reduce_noise(y=data, sr=rate,prop_decrease=0.8) 
        if reduced_noise.dtype != np.int16:
            reduced_noise = np.int16(reduced_noise / np.max(np.abs(reduced_noise)) * 32767)
        noise_reduced_segment = AudioSegment(reduced_noise.tobytes(), frame_rate=rate, sample_width=reduced_noise.dtype.itemsize, channels=1)
        noise_reduced_segment_path = os.path.join(NOISE_REDUCED_DIR, f"segment_{i + 1}_reduced_noise.mp3")
        noise_reduced_segment.export(noise_reduced_segment_path, format="mp3")
        yield segment_file_path,noise_reduced_segment_path

for segment_file_path, noise_reduced_segment_path in split_audio_file(AUDIO_PATH, OUTPUT_DIRECTORY):
    print()
    transcription = transcribe_audio_segment(noise_reduced_segment_path)
    print(transcription)