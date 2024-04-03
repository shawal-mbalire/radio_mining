import requests
import os

# Define file paths and URL
audio_url = "https://storage.googleapis.com/radiofilez/english/sunday/cp_91_3-2022-11-27_T06.00.01.mp3"
audio_file_path = "downloaded_audio.mp3"


# Download the audio file
response = requests.get(audio_url, allow_redirects=True)

if response.status_code == 200:
    with open(audio_file_path, 'wb') as f:
        f.write(response.content)
    print(f"Audio file downloaded successfully: {audio_file_path}")
else:
    print(f"Failed to download audio file: {response.status_code}")