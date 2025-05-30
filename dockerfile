FROM python:3.9-slim

WORKDIR /app

# Instale dependências do sistema para OpenCV, Whisper, Selenium e Chrome/Chromium
RUN apt-get update && \
    apt-get install -y libgl1-mesa-glx libglib2.0-0 ffmpeg \
    chromium-driver chromium && \
    rm -rf /var/lib/apt/lists/*

ENV PATH="/usr/lib/chromium:/usr/lib/chromium-browser:${PATH}"

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt