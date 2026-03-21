# This python script will copy the training data from GPT-SoVITS's slicer_opt.list file and create a python file that 
# you can run in Qwen3-TTS to create the voice clone, combining all audio files and descriptions into one reference.
import re
import os
import numpy as np
import soundfile as sf
from scipy import signal
training_audio = 'Dell_r730'
pause_duration = 0.5
output_audio = "combined_reference.wav"
output_text = "combined_reference.txt"
train_list_path = "slicer_opt.list"
text_separator = " "

def clean_text(text):
    # text = text.replace('—', '-')  # Don't convert these symbols as they do emphasis shift
    text = text.replace('–', '-')
    # Preserve — by converting to placeholder, strip ascii, restore
    text = text.replace('—', 'EMDASH')
    text = text.encode('ascii', 'ignore').decode('ascii')
    text = text.replace('EMDASH', '—')
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def parse_train_list(train_list_path):
    entries = []
    with open(train_list_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) >= 4:
                audio_path = parts[0]
                text = parts[3]
                text = clean_text(text)
                if text:
                    entries.append((audio_path, text))
    return entries

def concatenate_audio_files(audio_files, output_file, pause_duration):
    if not audio_files:
        print("No audio files to concatenate")
        return False
    try:
        concatenated_audio = []
        target_sr = None
        files_processed = 0
        for i, file_path in enumerate(audio_files):
            if not os.path.exists(file_path):
                print(f"Warning: File not found - {file_path}")
                continue
            audio, sr = sf.read(file_path)
            files_processed += 1
            if target_sr is None:
                target_sr = sr
            if sr != target_sr:
                num_samples = int(len(audio) * target_sr / sr)
                audio = signal.resample(audio, num_samples)
            concatenated_audio.append(audio)
            if i < len(audio_files) - 1:
                pause_samples = int(target_sr * pause_duration)
                pause = np.zeros(pause_samples)
                concatenated_audio.append(pause)
        final_audio = np.concatenate(concatenated_audio)
        sf.write(output_file, final_audio, target_sr)
        print(f"Successfully created combined audio file: {output_file}")
        print(f"  - Combined {files_processed} audio files")
        print(f"  - Total duration: {len(final_audio)/target_sr:.2f} seconds")
        print(f"  - Sample rate: {target_sr} Hz")
        return True
    except Exception as e:
        print(f"Error concatenating audio files: {e}")
        return False

def combine_texts(entries, output_file, separator=" "):
    texts = [text for _, text in entries]
    combined_text = separator.join(texts)
    combined_text = re.sub(r'\s+', ' ', combined_text)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(combined_text)
    preview = combined_text[:200] + "..." if len(combined_text) > 200 else combined_text
    print(f"Successfully created combined text file: {output_file}")
    print(f"  - Combined {len(entries)} text entries")
    print(f"  - Separator used: '{separator}'")
    print(f"  - Total length: {len(combined_text)} characters")
    print(f"  - Preview: {preview}")
    return combined_text

def generate_python_file(audio_path, text_path, output_file="generated_tts.py"):
    text_content = """Another thing that is hard to imagine is how far away the planets and stars really are. The ancient Chinese built stone towers so they could have a closer look at the stars. It's natural to think the stars and planets are much closer than they really are,... — after all,... — in everyday life we have no experience of the huge distances of space. Those distances are so large that it doesn't even make sense to measure them in feet or miles, the way we measure most lengths. Instead we use the light-year, which is the distance light travels in a year. In one second, a beam of light will travel 186,000 miles, so a light-year is a very long distance. The nearest star, other than our sun, is called Proxima Centauri (also known as Alpha Centauri C), which is about four light-years away. That is so far that even with the fastest spaceship on the drawing boards today, a trip to it would take about ten thousand years."""
    
    instruct_content = "Speak in a friendly, enthusiastic YouTube host style. Sound natural and conversational, like you're talking directly to a friend. Use a warm, engaging tone with slight excitement when asking questions and talk at a good slow speed for listeners."
    
    cleaned_text = clean_text(text_content)
    cleaned_text = re.sub(r'(?<!\.)\.(?!\.)(?=\s)', '...', cleaned_text)
    cleaned_text = '...' + cleaned_text
    cleaned_instruct = clean_text(instruct_content)
    template = f'''
import torch
import soundfile as sf
from qwen_tts import Qwen3TTSModel
model = Qwen3TTSModel.from_pretrained(
    "Qwen/Qwen3-TTS-12Hz-1.7B-Base",
    device_map="cuda:0",
    dtype=torch.bfloat16,
    attn_implementation="sdpa", # change to 'flash_attention_2' if supported by your GPU
)
ref_audio = "{audio_path}"
with open("{text_path}", 'r', encoding='utf-8') as f:
    ref_text = f.read()
print("Generating voice clone...")
print(f"Using reference audio: {{ref_audio}}")
print(f"Reference text length: {{len(ref_text)}} characters")
print(f"Reference text preview: {{ref_text[:100]}}...")
wavs, sr = model.generate_voice_clone(
    text="""{cleaned_text}""",
    language="English",
    ref_audio=ref_audio,
    ref_text=ref_text,
    instruct="""{cleaned_instruct}""",
    # 🔥 ADD THESE ↓↓↓
    temperature=0.5,
    top_p=0.8,
    top_k=30,
    repetition_penalty=1.1,
    # 🔥 ALSO IMPORTANT (sub-speaker layer)
    subtalker_temperature=0.5,
    subtalker_top_p=0.8,
    subtalker_top_k=30,
)
sf.write("output_voice_clone.wav", wavs[0], sr)
print("Voice clone saved to: output_voice_clone.wav")
import subprocess
subprocess.run([
    "ffmpeg",
    "-i", "output_voice_clone.wav",
    "-filter:a", f"atempo=.95",
    "-vn",
    "output_voice_clone-.95.wav"
])
subprocess.run([
    "ffmpeg",
    "-i", "output_voice_clone.wav",
    "-filter:a", f"atempo=.90",
    "-vn",
    "output_voice_clone-.90.wav"
])
'''
# Instead of ffmpeg can use sox which it says is studio quality - command 'sox input.wav output.wav tempo 0.95'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(template)
    print(f"\nSuccessfully generated {output_file}")
    print(f"  - Using combined audio: {audio_path}")
    print(f"  - Using combined text: {text_path}")

def main():
    if not os.path.exists(train_list_path):
        print(f"Error: {train_list_path} not found in current directory")
        print("Please make sure train.list is in the same directory as this script")
        return
    try:
        entries = parse_train_list(train_list_path)
        if not entries:
            print("No valid entries found in train.list")
            return
        print(f"Found {len(entries)} entries in train.list")
        audio_files = [audio_path for audio_path, _ in entries]
        existing_files = [f for f in audio_files if os.path.exists(f)]
        missing_files = [f for f in audio_files if not os.path.exists(f)]
        if missing_files:
            print(f"Warning: {len(missing_files)} audio files not found:")
            for f in missing_files[:5]:
                print(f"  - {f}")
            if len(missing_files) > 5:
                print(f"  ... and {len(missing_files)-5} more")
        if not existing_files:
            print("Error: No audio files found!")
            return
        print(f"\nProceeding with {len(existing_files)} audio files")
        print("\n" + "="*50)
        print("Text cleaning example:")
        print("="*50)
        sample_text = entries[0][1] if entries else ""
        print(f"Cleaned text: {sample_text[:100]}...")
        print("\n" + "="*50)
        print("Combining audio files...")
        print("="*50)
        if not concatenate_audio_files(existing_files, output_audio, pause_duration):
            print("Failed to combine audio files. Exiting.")
            return
        print("\n" + "="*50)
        print("Combining text files...")
        print("="*50)
        combined_text = combine_texts(entries, output_text, separator=text_separator)
        print("\n" + "="*50)
        print("Text combination verification:")
        print("="*50)
        print(f"Number of texts: {len(entries)}")
        print(f"Separator used: '{text_separator}'")
        print("\n" + "="*50)
        print("Generating TTS Python file...")
        print("="*50)
        generate_python_file(output_audio, output_text)
        print("\n" + "="*50)
        print("SUCCESS! You can now run: python generated_tts.py")
        print("="*50)
    except Exception as e:
        print(f"Error processing: {e}")
        import traceback
        traceback.print_exc()
if __name__ == "__main__":
    main()
