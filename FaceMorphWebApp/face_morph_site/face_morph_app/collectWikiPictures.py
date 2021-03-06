import requests
import random
from io import BytesIO
import urllib
import numpy as np
import cv2
import os
import string


S = requests.Session()

URL = "https://en.wikipedia.org/w/api.php"

file_path = os.path.join(os.path.dirname(__file__), "oldCelebs.txt")
file_path1 = os.path.join(os.path.dirname(__file__), "newCelebs.txt")

namesFile = open(file_path,"r", encoding="utf-8")
newFile = open(file_path1, "w", encoding="utf-8")


output = []

lowert = string.ascii_lowercase
lower = {}
for i in range (0, len(lowert)):
    lower[lowert[i]] = None
for i in range (0,10):
    lower[str(i)] = None
lower[')'] = None
lower['"'] = None
lower["'"] = None
upper = string.ascii_uppercase
upper = ["." + x for x in upper]

celebSet = set()

for line in namesFile:
    """
    PARAMS = {
    "action": "query",
    "format": "json",
    "titles": line.strip("\n"),
    "prop": "pageimages",
    "piprop": "original"
    }
    """
    if len(line) > 2 and (line.split(":::",1))[0].strip("\n") not in celebSet :
        adjust = False
        PARAMS = {
        "action": "query",
        "format": "json",
        "titles": (line.split(":::",1))[0].strip("\n"),
        "prop": "extracts",
        "exintro": "true",
        "explaintext": "true"
        }
        celebSet.add((line.split(":::",1))[0].strip("\n"))
        R = S.get(url=URL, params=PARAMS)

        DATA = R.json()

        x = DATA["query"]["pages"]
        newLine = ""
        for a in x:

            desc = ((x[a]["extract"]).split("\n", 1))[0]

            newDesc = ""
            index = 0

            indexList = []
            for i in range (0,len(upper)):
                index = desc.find(upper[i])
                if index != -1: indexList.append(index)
            if len(indexList) > 0:
                index = min(indexList)


            if index != -1:
                if desc[index -1] in lower:
                    adjust = True
                    for i in range (0, index+1):
                        newDesc = newDesc + desc[i]

                    newLine = line.strip("\n") + ":::" + newDesc
                    break

            if adjust:
                break
            else:
                newDesc = desc

            newLine = line.strip("\n") + ":::" + newDesc


        newFile.write(newLine)
        newFile.write("\n")




"""


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


