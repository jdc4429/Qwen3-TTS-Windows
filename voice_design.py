import os
os.environ["TRANSFORMERS_NO_FLASH_ATTENTION"] = "1"
import torch
import soundfile as sf
from qwen_tts import Qwen3TTSModel
model = Qwen3TTSModel.from_pretrained(
    "Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign",
    device_map="cuda:0",
    dtype=torch.bfloat16,
    attn_implementation="sdpa",  # Use SDPA for your RTX 2070
)
# Force SDPA
underlying_model = model.model
underlying_model.config._attn_implementation = "sdpa"

wavs, sr = model.generate_voice_design(
    text="Hey, this is Garett and welcome to my YouTube channel. You can find all sorts of cool self help videos on my channel. Do you know how to get raccoons out of a wall? Can you tell my voice was cloned?",
    language="English",
    instruct="A very scratchy low male voice that is very unique and odd but speaks at a good pace",
)

sf.write("output_voice_design.wav", wavs[0], sr)


# Designed voices

#Speak in a friendly, enthusiastic YouTube host style. Sound natural and conversational, like you're talking directly to a friend. Use a warm, engaging tone with slight excitement when asking questions and talk at a good speed for listeners.

# A composed middle-aged male announcer with a deep, rich and magnetic voice, a steady speaking speed and clear articulation, suitable for news broadcasting or documentary commentary.  Speak in a friendly, enthusiastic YouTube host style. Sound natural and conversational, like you're talking directly to a friend. Use a warm, engaging tone with slight excitement when asking questions and talk at a good speed for listeners.

#A warm, engaging woman with a naturally rich and inviting voice, smooth and pleasant to listen to. She speaks with a steady, clear cadence and a genuine, friendly energy. Her tone is conversational and approachable, like chatting with a close friend over coffee. She brings warmth and a subtle enthusiasm to her words, with a natural lift of excitement when asking questions, and maintains a comfortable, easy-to-follow pace throughout.