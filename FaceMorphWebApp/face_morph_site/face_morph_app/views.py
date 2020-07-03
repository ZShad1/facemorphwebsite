from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
import cv2
import os
import json
from . import faceMorph
from PIL import Image


def home(request):
    context = {}

    # getting all the celebrity information
    file_path = os.path.join(os.path.dirname(__file__), "celebs.txt")
    namesFile = open(file_path,"r", encoding="utf-8")
    context['celebs'] = {} # stores the celeb names and urls
    context['celebsDesc'] = {} #stores the celeb names and desc

    allLines = namesFile.readlines()

    for i in range (0, (len(allLines))-1):

        lineSplit = allLines[i].split(":::")

        # if the current line is the first line with name, url, and desc, we need to save the url and name
        if len(lineSplit) == 3:
            name = lineSplit[0].strip("\n")
            url = lineSplit[1].strip("\n")
            context['celebs'][name] = url
            descList = []

            while True: # emulating a do-while loop > looking for the next occurance of ":::" to see when the celebs summary is over

                descList.append(lineSplit[2].strip("\n")) # append the first line of the summary

                if (i+1 != len(allLines) and len(allLines[i+1].split(":::")) == 1 ): # ensuring the new line we are on is not a new celeb
                    i = i+1
                    descList.append(allLines[i].strip("\n"))
                else: # if it is a new celebrity, we store the desc.
                    desc = ""
                    for summaryLine in descList:
                        desc = desc +  summaryLine

                    context['celebsDesc'][name] = desc
                    break
    context['celebs'] = json.dumps(context['celebs'])

    return render(request, "face_morph_app/home.html", context)

def result(request):
    context = {}

    userPicture = False # track if user submitted a picture or not
    fileName = ""

    if request.method == 'POST' and 'uploadPicture' in request.POST:

        # store user picture if they submitted one
        try:
            uploaded_file = request.FILES['document']
            fs = FileSystemStorage()
            fileName = fs.save(uploaded_file.name, uploaded_file)
            context['url'] = fs.url(fileName)
            userPicture = True
        except:
            userPicture = False
        celebDict = {request.POST["celebselect0"]: request.POST["celebURL0"],
                      request.POST["celebselect1"]: request.POST["celebURL1"],
                      request.POST["celebselect2"]: request.POST["celebURL2"],
                      request.POST["celebselect3"]: request.POST["celebURL3"],
                      request.POST["celebselect4"]: request.POST["celebURL4"]}


        context['morphimage'] = faceMorph.run(celebDict, fileName, userPicture) # get the morphed image
        context['celebs'] = celebDict

    return render(request,"face_morph_app/result.html", context)


#def test():
#    faceMorph.run()
