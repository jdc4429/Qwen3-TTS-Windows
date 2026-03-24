<h1>GPT-SoVITS V4/V2Pro/V2ProPlus (BEST)</h1>
A Powerful Few-shot Voice Conversion and Text-to-Speech WebUI.<br>


## Install:<br>

Link to Qwen3-TTS package: https://github.com/jdc4429/Qwen3-TTS-Windows

Run the following commands to create an environment and install the neccessary files:

```bash
conda create -n GPT python=3.10.20 -y
conda activate GPT
```
then run:

```bash
git clone https://github.com/jdc4429/GPT-SoVITS-V2ProPlus-Windows.git
cd GPT-SoVITS-V2ProPlus-Windows
powershell -File install-FINAL-FIXES.ps1 -Device CU126 -Source HF
```
Powershell script: (Select from CU126, CU128, CU130) (Select from HF, HF-Mirror, ModelScope)<br>
<br>
The script takes quite a while to run as it has to download many GB's for the models.<br>

For help, see Usage Instructions.txt


## Features:<br>

1. **Zero-shot TTS:** Input a 5-second vocal sample and experience instant text-to-speech conversion.

2. **Few-shot TTS:** Fine-tune the model with just 1 minute of training data for improved voice similarity and realism.

3. **Cross-lingual Support:** Inference in languages different from the training dataset, currently supporting English, Japanese, Korean, Cantonese and Chinese.

4. **WebUI Tools:** Integrated tools include voice accompaniment separation, automatic training set segmentation, Chinese ASR, and text labeling, assisting beginners in creating training datasets and GPT/SoVITS models.


## Tested Environments:<br>

-----------------------------------------------------
| Python Version | PyTorch Version  | Device        |
| -------------- | ---------------- | ------------- |
| Python 3.10    | PyTorch 2.9.1    | CUDA 12.6     |
-----------------------------------------------------


#### Environment Variables:<br>

- `is_half`: Controls whether half-precision (fp16) is enabled. Set to `true` if your GPU supports it to reduce memory usage.


## Pretrained Models & other models (Only needed if not installing with Powershell script)<br>

Download pretrained models from [GPT-SoVITS Models](https://huggingface.co/lj1995/GPT-SoVITS) and place them in `GPT_SoVITS/pretrained_models`.

Download G2PW models from [G2PWModel.zip(HF)](https://huggingface.co/XXXXRT/GPT-SoVITS-Pretrained/resolve/main/G2PWModel.zip)| [G2PWModel.zip(ModelScope)](https://www.modelscope.cn/models/XXXXRT/GPT-SoVITS-Pretrained/resolve/master/G2PWModel.zip), unzip and rename to `G2PWModel`, and then place them in `GPT_SoVITS/text`.

For UVR5 (Vocals/Accompaniment Separation & Reverberation Removal, additionally), download models from [UVR5 Weights](https://huggingface.co/lj1995/VoiceConversionWebUI/tree/main/uvr5_weights) and place them in `tools/uvr5/uvr5_weights`.



## If you get the below error, run the pip command listed to fix it.<br>

ffmpeg.exe - Entry Point Not Found - The procedure entry point libintl_bind_textdomain_codeset could not be located in the dynamic link library C:\Users\jeffc\anaconda3\envs\SoVITS\Library\bin\gdk_pixbuf-2.0-0.dll.

Fix:<br>
conda activate GPT<br>
conda install libglib=2.78.4=*_0 gdk-pixbuf -c conda-forge --force-reinstall<br>
<br>