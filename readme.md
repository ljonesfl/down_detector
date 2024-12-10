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
    
The program will periodically check the internet connection and announce when it is unavailable. It will
also announce if the latency exceeds a specified threshold.

The pyttsx3 package proved to be unstable so I opted for gTTS. gTTS requires an internet connection
to generate the files so, the first time the program is ran, it will require an active connection
to generate the mp3 files. After that, it can speak its phrases whether connected or not.

State changes will only be announced during a scheduled window. The default schedule is 6am to 10pm.

### Phrases
The phrases are configurable in the config file. To change the phrase, simply update
the text, delete the mp3 files in the audio folder then re-run the program.

### Configuration

The configuration is stored in down_detector.yaml.
The program will automatically detect changes to the config file and reload it without having to restart.

#### Parameters
```
schedule:
    start_hour: 7
    end_hour: 22
```
start_hour and end_hour specify the start and end time of the notification window. Notifications
outside of this range will be ignored.

```
timeout:
  active: 10
  down: 5
  response: 5
```
active

The number of seconds to wait between polling when the internet is active.

down

The number of seconds to wait between polling when the internet is down.

response

The number of seconds to wait when checking latency before assuming failure.

```
phrase:
  active: the internet connection is active
  down: the internet is currently unreachable
  normal: the internet speed is normal
  slow: the internet speed is currently slow
```

active

The phrase to speak when the internet becomes active.

down

The phrase to speak when the internet is determined to be down.

normal

The phrase to speak when latency is determined to be normal.

slow

The phrase to speak when latency is determined to be high.

```
audio:
  active: audio/active.mp3
  down: audio/down.mp3
  slow: audio/slow.mp3
  normal: audio/normal.mp3
```

These are all relative paths/names of the mp3 files generated
from the phrases.

```
latency:
  min: 0.30
  count: 3
```

min

The minimum latency in seconds before determining that the internet is slow.

count

The number of polling cycles that latency must be high before triggering
an alert.

```
log:
  enabled: true
  file: log.csv
  active: true
  latency: true
```

enabled

Enable/disable file logging.

file

The name of the log file to write to.

active

Log active\down events.

latency

Log latency events.

```
notify:
  active:
    voice: true
    led: false
  latency:
    voice: true
    led: false
    beep: true
```

active

voice

Speak when changing between active/down.

latency

voice

Speak when changing between slow/normal.

beep

Beep when latency is determined to be slow on polling cycles 
before latency - count cycles are reached and a phrase is spoken.

## Installation
### Install Python Packages
#### Batch
    pip install -r requirements.txt

#### Manual
    pip install gTTS
    pip install pyyaml
    pip install ping3
    pip install simpleaudio
    pip install numpy
    pip install RPi.GPIO <-- only if using a Raspberry Pi

### Setup Config File
    cp down_detector.yaml.example down_detector.yaml
