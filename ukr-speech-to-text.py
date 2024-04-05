#!/usr/bin/env python

import os
import sys
import time
import azure.cognitiveservices.speech as speechsdk


def speech_recognize_continuous_from_file(filename):
    """performs continuous speech recognition with input from an audio file"""
    speech_config = speechsdk.SpeechConfig(
        subscription=os.environ.get("TRANSLATOR_TEXT_RESOURCE_KEY"),
        region=os.environ.get("TRANSLATOR_TEXT_REGION"),
    )
    speech_config.speech_recognition_language = "uk-UA"
    audio_config = speechsdk.audio.AudioConfig(filename=filename)

    speech_recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config, audio_config=audio_config
    )

    done = False

    def stop_cb(evt):
        speech_recognizer.stop_continuous_recognition()
        nonlocal done
        done = True
    
    def text_recognized(evt):
        print(evt, file=sys.stderr)
        sys.stderr.flush()
        print(evt.result.text, file=sys.stdout)
        sys.stdout.flush()

    speech_recognizer.recognized.connect(text_recognized)

    # stop continuous recognition on either session stopped or canceled events
    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)

    # Start continuous speech recognition
    speech_recognizer.start_continuous_recognition()
    while not done:
        time.sleep(0.5)

print(sys.argv[0], sys.argv[1], file=sys.stderr)
speech_recognize_continuous_from_file(sys.argv[1])
