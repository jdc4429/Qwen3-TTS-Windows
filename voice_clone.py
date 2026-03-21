import torch
import soundfile as sf
from qwen_tts import Qwen3TTSModel
model = Qwen3TTSModel.from_pretrained(
    "Qwen/Qwen3-TTS-12Hz-1.7B-Base",
    device_map="cuda:0",
    dtype=torch.bfloat16,
    attn_implementation="sdpa",
)

ref_audio = "C:\GPT-SoVITS\Train\dell_r730_1.wav"
ref_text  = "Okay I want to do a quick video for installing a second video card in my R730 rack server I had problems here with the power cable for the second R As you can see there's not a lot of room and there was no way to route the power cable You can see here"

ref_audio = "C:\GPT-SoVITS\Train\dell_r730_2.wav"
ref_text  = "comes out of the device out of the card This is a Tesla P100 You can see it comes out of that There's no way to get it to come over here to the riser where you need it to plug in So what I wound up having to do I tried going through the air vent here and coming out this way and going over"

ref_audio = "C:\GPT-SoVITS\Train\dell_r730_3.wav"
ref_text  = "over this little like indentation here go down but then the cables not long enough so what i wound up doing was just in case you run into the same problem you can actually run this underneath here and have it come out the side let me see if i can get the light in there you can see it comes up"

ref_audio = "C:\GPT-SoVITS\Train\dell_r730_4.wav"
ref_text  = "the side doubles over and then goes into the riser I couldn't find any other way If anybody has any ideas for something better let me know and I'll be sure to update this and do a video for it The only downside is you see in here"

ref_audio = "C:\GPT-SoVITS\Train\dell_r730_5.wav"
ref_text  = "I don't think it'll be for what I'm doing and what most people are doing at home I don't think it'll be an issue So anyways that's how you install a second one in Also how I did it was I have this weird"

ref_audio = "C:\GPT-SoVITS\Train\dell_r730_6.wav"
ref_text  = "On the edge of the card there's this captive screw so you can't undo it"

ref_audio = "C:\GPT-SoVITS\Train\dell_r730_7.wav"
ref_text  = "proper way to I forget what the name of this is but it's like a holder to hold the video card in place This one worked fine on my P40 so it didn't have that device I tried to use a screwdriver and so forth to back that captive screw out but it does not want to come out"

ref_audio = "C:\GPT-SoVITS\Train\dell_r730_8.wav"
ref_text  = "So anyways what I did was I just decided just to put this over here and just let it it's not going anywhere And I'll reinstall it if I take the card out or if I sell the server But for right now that's installed"

ref_audio = "C:\GPT-SoVITS\Train\dell_r730_9.wav"
ref_text  = "Also the way that I did it there's a little button here you press and this whole riser actually pulls out I installed the riser on the card and then installed the card in the machine I found that easier Also beware there's a little tab here that goes over But I found that easier I tried it both"

ref_audio = "C:\GPT-SoVITS\Train\dell_r730_10.wav"
ref_text  = "and it was just too hard to get the angle correct to slide it into the riser being installed so anyways i had to take it out again anyways because i had to do that um but for me putting the riser on the card outside the machine and then installing it that's what we're"

wavs, sr = model.generate_voice_clone(
    text="Hey, this is Barth and welcome to my YouTube channel. You can find all sorts of cool self help videos on my channel. Do you know how to get raccoons out of a wall? Can you tell my voice was cloned?",
    language="English",
    ref_audio=ref_audio,
    ref_text=ref_text,
    instruct="Speak in a friendly, enthusiastic YouTube host style. Sound natural and conversational, like you're talking directly to a friend. Use a warm, engaging tone with slight excitement when asking questions and talk at a good slow speed for listeners.",
)
sf.write("output_voice_clone.wav", wavs[0], sr)
