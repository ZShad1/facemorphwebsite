from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
import cv2
import os
import json
from . import faceMorph

def home(request):
    context = {}

    file_path = os.path.join(os.path.dirname(__file__), "celebs.txt")
    namesFile = open(file_path,"r",encoding="utf-8")
    context['celebs'] = {}
    namesFile.readline()
    for line in namesFile:
        line = line.split(":", 1)
        name = line[0].strip("\n")
        url = line[1].strip("\n")
        context['celebs'][name] = url
    print(len(context['celebs']))
    context['celebs'] = json.dumps(context['celebs'])

    return render(request, "face_morph_app/home.html", context)

def result(request):
    context = {}

    if request.method == 'POST' and 'uploadPicture' in request.POST:

        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        fileName = fs.save(uploaded_file.name, uploaded_file)
        context['url'] = fs.url(fileName)

        celebNames = [request.POST["celebselect0"], request.POST["celebselect1"], request.POST["celebselect2"],
                      request.POST["celebselect3"], request.POST["celebselect4"]]

        context['morphimage'] = faceMorph.run(celebNames)
        context['celebs'] = celebNames

    return render(request,"face_morph_app/result.html", context)


#def test():
#    faceMorph.run()
