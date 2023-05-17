# Down Detector

## Purpose

Living in an RV with a lot of trees around, my Starlink loses connection occasionally.
As I have a lot of IOT devices connected to it, I wanted a way to know when the internet 
was currently unavailable and back online.

I created this program to run on a Raspberry Pi and check the internet connection periodically
then say something if it changes state to down and back up.


## Requirements
### Should
* Poll the internet connection periodically
* Announce when the state of the internet connection changes
* Only announce state changes during a scheduled window

### Could
* Notify if latency exceeds a threshold
* Notify via email or text message


## Usage

    python3 down_detector.py
    
It is currently configured to poll the internet every 15 seconds while active and every 5 seconds
while down.

The pyttsx3 package proved to be unstable so I opted for gTTS. gTTS requires an internet connection
to generate the files so, the first time the program is ran, it will require an active connection
to generate the mp3 files. After that, it can speak its phrases whether connected or not.

State changes will only be announced during a scheduled window. The default schedule is 6am to 10pm.

### Phrases
The phrases are configurable in the config file. To change the phrase, simply update
the text, delete the mp3 files in the audio folder then re-run the program.

### Configuration

The configuration is stored in a down_detector.yaml file.
Be sure to restart the program after making changes to the config file.

## Installation
    source venv/bin/activate
    pip install gTTS
    pip install pyyaml
    pip install ping3

