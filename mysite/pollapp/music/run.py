#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import json
from os.path import join, dirname
from dotenv import load_dotenv
from watson_developer_cloud import SpeechToTextV1 as SpeechToText
from watson_developer_cloud import AlchemyLanguageV1 as AlchemyLanguage
from pydub import AudioSegment
from speech_sentiment_python.recorder import Recorder
from watson_developer_cloud import ToneAnalyzerV3 as ToneAnalyser
import requests
from googletrans import Translator

#stt = SpeechToText(username="0470aaca-c082-40b3-8497-9ea89cf0a0c0", password="2DaFdKgu3Wkl")
#sound = AudioSegment.from_file("test0.wav")
#halfway_point = len(sound) // 2
#first_half = sound[:halfway_point/2]
#second_half = sound[halfway_point/2:]


#first_half.export("clip0.wav", format="wav")
#second_half.export("clip1.wav", format="wav")

#for i in range(0,2):
#	file = "clip" + str(i) + ".wav"
#	audio_file = open(file, "rb")
#	text = json.dumps(stt.recognize(audio_file, content_type="audio/wav"), indent=2)
#	print (text)
def transcribe_audio(path_to_audio_file):
    username = "b6edc1f8-d2c3-4aaf-97d3-d16dd0ad1d61"
    password = "Ypj577gNJvPi"
    speech_to_text = SpeechToText(username=username,password=password)

    with open(join(dirname(__file__), path_to_audio_file), 'rb') as audio_file:
        return speech_to_text.recognize(audio_file,content_type='audio/wav')

def analyze_tone(text):
    username = '6de40222-d8a8-44be-8300-b9d5c022a6bb'
    password = 'AT7oh5YTq1aO'
    watsonUrl = 'https://gateway.watsonplatform.net/tone-analyzer/api/v3/tone?version=2016-05-18'
    headers = {"content-type": "text/plain"}
    data = text
    try:
        r = requests.post(watsonUrl, auth=(username,password),headers = headers,
         data=data)
        return r.text
    except:
        return False

def display_results(data):
    data = json.loads(str(data))
    print(data)
    for i in data['document_tone']['tone_categories']:
        print(i['category_name'])
        print("-" * len(i['category_name']))
        for j in i['tones']:
            print(j['tone_name'].ljust(20),(str(round(j['score'] * 100,1)) + "%").rjust(10))
        print()
    print()

def translate_to_japanese(text):
    translator = Translator()
    translated_text = translator.translate(text, dest='ja')
    print(translated_text)
    return translated_text

def translate_to_tamil(text):
    translator = Translator()
    translated_text = translator.translate(text, dest='ta')
    print(translated_text)
    return translated_text

def translate_to_telugu(text):
    translator = Translator()
    translated_text = translator.translate(text, dest='te')
    print(translated_text)
    return translated_text

def main():
    recorder = Recorder("speech.wav")

    print("Please say something nice into the microphone\n")
    recorder.record_to_file()
	
    print("Transcribing audio....\n")
    result = transcribe_audio('speech.wav')

    text = result['results'][0]['alternatives'][0]['transcript']
    print("Text: " + text + "\n")

    translated_text = translate_to_japanese(text)
    data = text
    if len(data) >= 1:
        results = analyze_tone(data)
        if results != False:
            display_results(results)
            exit
        else:
            print("Something went wrong")


if __name__ == '__main__':
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)
    try:
        main()
    except:
        print("IOError detected, restarting...")
        main()

