# Down Detector

## Purpose

Living in an RV with a lot of trees around, my Starlink loses connection occasionally.
As I have a lot of IOT devices connected to it, I wanted a way to know when the internet 
was currently unavailable and back online.

I created this program to run on a Raspberry Pi and check the internet connection periodically
then say something if it changes state to down and back up.

## Usage

    python3 down_detector.py
    
It is currently configured to poll the internet every 15 seconds while active and every 5 seconds
while down.

The pyttsx3 package proved to be unstable so I opted for gTTS. gTTS requires an internet connection
to generate the files so, the first time the program is ran, it will require an active connection
to generate the mp3 files. After that, it can speak its phrases whether connected or not.

### Phrases
The phrases are configurable via ACTIVE_TEXT and DOWN_TEXT. To change the phrase, simply update
the text, delete the mp3 files in the audio folder then re-run the program.

## Installation
    source venv/bin/activate
    pip install requests
    pip install gTTS

