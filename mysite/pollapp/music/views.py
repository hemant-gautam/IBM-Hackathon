#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import json
from os.path import join, dirname
import subprocess
from subprocess import PIPE, Popen

from django.conf import settings
from dotenv import load_dotenv
from watson_developer_cloud import SpeechToTextV1 as SpeechToText
from pydub import AudioSegment

# from speech_sentiment_python.recorder import Recorder

from watson_developer_cloud import ToneAnalyzerV1Experimental as ToneAnalyser
import requests
from googletrans import Translator

from django.core.files.storage import FileSystemStorage


from django.shortcuts import render, redirect
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from .models import Document, mediau
from .forms import DocumentForm

def home(request):

    return render(request, 'base.html')

def convert_file(request):
    print("entered")
    file = request.POST.get('abc', False)
    # uploading the file is required
    print("entered2")
    # form = DocumentForm(request.POST, request.FILES)
    #
    # newdoc = Document(docfile = request.FILES.get('file'))
    # newdoc.save()
    if request.method == 'POST' and request.FILES['abc']:
        myfile = request.FILES['abc']
        # a, file_extension = os.path.splitext(request.FILES['abc'].name)
        # print("a","ASDADA",file_extension)
        # cmd="mkdir "+settings.MEDIA_ROOT +'\\'+a
        # print(cmd)
        # result = Popen(cmd, shell=True, stdout=PIPE).stdout.read()
        # if len(result)>0:
        #     raise Exception(result)

        location=settings.MEDIA_ROOT+"\\documents"
        base_url=settings.MEDIA_URL+"/documents"
        print(myfile)
        fs = FileSystemStorage(location,base_url)
        file_name = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(file_name)
        fileurl=mediau(url=uploaded_file_url,name="a")
        fileurl.save()
        print("success")

    # Load documents for the list page
    # documents = Document.objects.all()
    # print("entered4")

    # Render list page with the documents and the form
    # return render(
    #     request, 'home.html',
    #     {'documents': documents, 'form': form},
    # )

    # after uploading the file
    result = transcribe_audio(settings.MEDIA_ROOT+"\\documents\\audio-file.flac")

    print("entered5")

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
    return render(request, 'home.html', context)


def transcribe_audio(path_to_audio_file):
    username = "b6edc1f8-d2c3-4aaf-97d3-d16dd0ad1d61"
    password = "Ypj577gNJvPi"
    speech_to_text = SpeechToText(username=username,password=password)

    with open(join(dirname(__file__), path_to_audio_file), 'rb') as audio_file:
        return speech_to_text.recognize(audio_file,content_type='audio/flac')

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
    print(translated_text)
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

