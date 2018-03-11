#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import os
from os.path import join, dirname
import sys
import requests
import subprocess

from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from googletrans import Translator
from django.conf import settings
from imp import reload

from .models import mediau
from .recorder import Recorder
from watson_developer_cloud import SpeechToTextV1 as SpeechToText


def home(request):

    return render(request, 'base.html')

def convert_file(request):
    reload(sys)
    sys.setdefaultencoding('utf-8')
    hide = request.POST['hide']
    print(type(hide))
    if int(hide) == 1:
        recorder = Recorder("speech.wav")
        recorder.record_to_file()
        print("Transcribing audio....\n")
        result = transcribe_audio('speech.wav')
    else:
        if request.method == 'POST' and request.FILES['abc']:
            myfile = request.FILES['abc']
            filename, file_extension = os.path.splitext(request.FILES['abc'].name)
            file_extension = file_extension[1:]
            location = settings.MEDIA_ROOT
            base_url = settings.MEDIA_URL
            print(myfile)
            fs = FileSystemStorage(location, base_url)
            file_name = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(file_name)
            fileurl = mediau(url=uploaded_file_url, name=filename)
            fileurl.save()

        result = transcribe_audio_file(settings.MEDIA_ROOT+"\\" + filename+"." + file_extension, file_extension)
        # print(result)
    # for k, v in result.items():
    #     print(v[0])
    text = result['results'][0]['alternatives'][0]['transcript']
    print("Text: " + text + "\n")

    translated_text_hi = translate_to_hindi(text)
    translated_text_ta = translate_to_tamil(text)
    translated_text_te = translate_to_telugu(text)
    translated_text_kn = translate_to_kannada(text)

    data = text
    if len(data) >= 1:
        results = analyze_tone(data)
        if results != False:
            sentiment = display_results(results)
            category_name = sentiment['category_name']
            tones = sentiment['tones']
            exit
        else:
            print("Something went wrong")

    context = {
         'text' : text,
         'translated_text_hi':translated_text_hi,
         'translated_text_ta':translated_text_ta,
         'translated_text_te':translated_text_te,
         'translated_text_kn':translated_text_kn,
         'results':results,
         'sentiment':sentiment,
         'tones':tones,
         'category_name':category_name
    }
    return render(request, 'base.html', context)


def transcribe_audio(path_to_audio_file):
    username = "b6edc1f8-d2c3-4aaf-97d3-d16dd0ad1d61"
    password = "Ypj577gNJvPi"
    speech_to_text = SpeechToText(username=username,password=password)

    with open(path_to_audio_file, 'rb') as audio_file:
        return speech_to_text.recognize(audio_file,content_type='audio/wav')


def transcribe_audio_file(path_to_audio_file, file_extension):
    username = "b6edc1f8-d2c3-4aaf-97d3-d16dd0ad1d61"
    password = "Ypj577gNJvPi"
    speech_to_text = SpeechToText(username=username,password=password)

    with open(path_to_audio_file, 'rb') as audio_file:
        return speech_to_text.recognize(audio_file,content_type='audio/'+file_extension)





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
    # for i in data['document_tone']['tone_categories']:
    #     print(i['category_name'])
    #     print("-" * len(i['category_name']))
    #     for j in i['tones']:
    #         print(j['tone_name'].ljust(20),(str(round(j['score'] * 100,1)) + "%").rjust(10))
    #     print()
    # print()
    return data['document_tone']['tone_categories'][0]

def translate_to_tamil(text):
    translator = Translator()
    translated_text = translator.translate(text, dest='ta')
    # print(translated_text)
    return translated_text

def translate_to_telugu(text):
    translator = Translator()
    translated_text = translator.translate(text, dest='te')
    print(translated_text)
    return translated_text

def translate_to_hindi(text):
    translator = Translator()
    translated_text = translator.translate(text, dest='hi')
    print(translated_text)
    return translated_text

def translate_to_kannada(text):
    translator = Translator()
    translated_text = translator.translate(text, dest='kn')
    print(translated_text)
    return translated_text

