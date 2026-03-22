@echo off
REM Create environment
conda create -n TTS python=3.10.20 -y

REM Run all installation commands in the environment
conda run -n TTS pip install -U qwen-tts
conda run -n TTS pip install torch==2.10.0 torchvision==0.25.0 torchaudio==2.10.0 --index-url https://download.pytorch.org/whl/cu130
conda run -n TTS pip install https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/download/v0.7.13/flash_attn-2.8.3+cu130torch2.10-cp310-cp310-win_amd64.whl
conda run -n TTS pip install transformers==4.57.3

conda run -n TTS git clone https://github.com/jdc4429/Qwen3-TTS-Windows.git
cd Qwen3-TTS-Windows
conda run -n TTS pip install -e .
