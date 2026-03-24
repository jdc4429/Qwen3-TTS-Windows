
import torch
import soundfile as sf
from qwen_tts import Qwen3TTSModel
model = Qwen3TTSModel.from_pretrained(
    "Qwen/Qwen3-TTS-12Hz-1.7B-Base",
    device_map="cuda:0",
    dtype=torch.bfloat16,
    attn_implementation="sdpa", # change to 'flash_attention_2' if supported by your GPU
)
ref_audio = "combined_reference.wav"
with open("combined_reference.txt", 'r', encoding='utf-8') as f:
    ref_text = f.read()
print("Generating voice clone...")
print(f"Using reference audio: {ref_audio}")
print(f"Reference text length: {len(ref_text)} characters")
print(f"Reference text preview: {ref_text[:100]}...")
wavs, sr = model.generate_voice_clone(
    text="""...欢迎来到语音合成技术的未来！""",
    language="Chinese",
    ref_audio=ref_audio,
    ref_text=ref_text,
    instruct="""Speak in a friendly, enthusiastic YouTube host style. Sound natural and conversational, like you're talking directly to a friend. Use a warm, engaging tone with slight excitement when asking questions and talk at a good slow speed for listeners.""",
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
    "-filter:a", f"atempo=1.05",
    "-vn",
    "output_voice_clone-1.05.wav"
])
