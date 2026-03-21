import torch
import soundfile as sf
from qwen_tts import Qwen3TTSModel
# Load the CustomVoice model (1.7B recommended for best quality)
model = Qwen3TTSModel.from_pretrained(
    "Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice",
    device_map="cuda:0",  # Use "cpu" if no GPU available
    dtype=torch.bfloat16,
    attn_implementation="sdpa",  # Change to 'flash_attention_2' if you have GPU that supports.
)
# Available speakers: Vivian, Serena, Uncle_Fu, Dylan, Eric, Ryan, Aiden, Ono_anna, Sohee
wavs, sr = model.generate_custom_voice(
    text="Welcome to the future of text-to-speech technology!",
    language="English",
    speaker="Ryan",  # Dynamic male voice with strong rhythm
    instruct="Very happy and energetic, with enthusiasm",  # Optional style instruction
)
# Save the audio
sf.write("custom_voice_output.wav", wavs[0], sr)
print(f"Generated audio saved to custom_voice_output.wav (Sample rate: {sr} Hz)")