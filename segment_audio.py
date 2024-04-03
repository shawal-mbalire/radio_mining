from pydub import AudioSegment
import os

output_dir = "output_chunks" 
audio_file_path = 'downloaded_audio.mp3'

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

def split_audio_file(audio_file_path, output_dir, segment_duration_s=150):
    """Split audio file into segments and save them."""
    # Load audio file
    audio = AudioSegment.from_mp3(audio_file_path)

    # Calculate number of segments
    num_segments = int(audio.duration_seconds / segment_duration_s) + 1

    # Split then export the segments
    for i in range(num_segments):
        start_time = i * segment_duration_s * 1000  # Convert seconds to milliseconds
        end_time = min((i + 1) * segment_duration_s * 1000, audio.duration_seconds * 1000)

        segment = audio[start_time:end_time]
        segment_file_path = os.path.join(output_dir, f"segment_{i + 1}.mp3")
        segment.export(segment_file_path, format="mp3")
        yield segment_file_path

for segment_file_path in split_audio_file(audio_file_path, output_dir):
    print(f"Segment file saved: {segment_file_path}")