#!/bin/bash
yt-dlp -o /tmp/audio.wav --extract-audio --audio-format wav $1 # https://www.youtube.com/watch?v=MXTPXJfWBxA
#youtube-dl -o /tmp/audio.wav --extract-audio --audio-format wav $1 # https://www.youtube.com/watch?v=MXTPXJfWBxA
[ $? -eq 0 ] && ffmpeg -i /tmp/audio.wav -ac 1 -ar 16000 /tmp/audiomono16khz.wav
[ $? -eq 0 ] && ukr-speech-to-text.py /tmp/audiomono16khz.wav | tee translated.txt
[ $? -eq 0 ] && ukrainian-word-stress --symbol combining translated.txt >translatedstressed.txt
rm /tmp/audio.wav /tmp/audiomono16khz.wav 
