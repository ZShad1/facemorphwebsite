import requests
import random
from io import BytesIO
import urllib
import numpy as np
import cv2
import os


S = requests.Session()

URL = "https://en.wikipedia.org/w/api.php"

file_path = os.path.join(os.path.dirname(__file__), "celebnames.txt")
file_path1 = os.path.join(os.path.dirname(__file__), "celebs.txt")

namesFile = open(file_path,"r")
newFile = open(file_path1, "w")


output = []


for line in namesFile:
    PARAMS = {
    "action": "query",
    "format": "json",
    "titles": line.strip("\n"),
    "prop": "pageimages",
    "piprop": "original"
    }


    R = S.get(url=URL, params=PARAMS)

    DATA = R.json()

    x = DATA["query"]["pages"]
    newLine = ""
    for a in x:
        try:
            url = (x[a]["original"]["source"])
            newLine = line.strip("\n") + ":" + url
        except:
            newLine =""
    if newLine != "":
        newFile.write(newLine)
        newFile.write("\n")



"""
namesLines = namesFile.readlines() # lots of memory is wasted here > find a way to read an individual line
randomNumber = random.randint(1, len(namesLines))

PARAMS = {
    "action": "query",
    "format": "json",
    "titles": namesLines[randomNumber].strip("\n"),
    #"titles": "Coldplay",
    "prop": "pageimages",
    "piprop": "original"
}


R = S.get(url=URL, params=PARAMS)

DATA = R.json()

#print(DATA["query"]["pages"]["80103"]["original"]["source"])

x = DATA["query"]["pages"]

for a in x:
    url = (x[a]["original"]["source"])

resp = urllib.request.urlopen(url)
image = np.asarray(bytearray(resp.read()), dtype="uint8")
image = cv2.imdecode(image, cv2.IMREAD_COLOR)
"""


