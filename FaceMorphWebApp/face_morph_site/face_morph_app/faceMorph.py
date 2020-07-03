from imutils import face_utils
import dlib
import cv2
import numpy as np
import math
import os
import requests
import random
import urllib

# I took this straight from GitHub, not very familar with heavy math based transformations
# inPoints and outPoints are sets of two points > aka the coordinates of the eyes
# Returns tform[0] which has two coordinates post affine transformation
def similarityTransform(inPoints, outPoints) :
    s60 = math.sin(60*math.pi/180)
    c60 = math.cos(60*math.pi/180)

    inPts = np.copy(inPoints).tolist()
    outPts = np.copy(outPoints).tolist()

    xin = c60*(inPts[0][0] - inPts[1][0]) - s60*(inPts[0][1] - inPts[1][1]) + inPts[1][0]
    yin = s60*(inPts[0][0] - inPts[1][0]) + c60*(inPts[0][1] - inPts[1][1]) + inPts[1][1]

    inPts.append([np.int(xin), np.int(yin)])

    xout = c60*(outPts[0][0] - outPts[1][0]) - s60*(outPts[0][1] - outPts[1][1]) + outPts[1][0]
    yout = s60*(outPts[0][0] - outPts[1][0]) + c60*(outPts[0][1] - outPts[1][1]) + outPts[1][1]

    outPts.append([np.int(xout), np.int(yout)])

    # Affine transformation is a method to maintain your old coordinates relative to each other
    # Perfect for changing size of image while maintaing coordinates relative to each other
    tform = cv2.estimateAffinePartial2D(np.array([inPts]), np.array([outPts]))

    return tform[0]


def readPictures(path, name):
    fileNames = os.listdir(path = path)
    images = []

    for file in fileNames:
        if file == name:
            imagePath = path + file

            # read the image
            image = cv2.imread(imagePath)
            images.append(image)


    return images

# Find the landmark of faces using dlib and return an array containing the landmark coordinates of all detected faces & individial faces
def landmarkOfImages(images):
    # p = our pre-treined model directory
    file_path = os.path.join(os.path.dirname(__file__), "shape_predictor_68_face_landmarks.dat")
    #p = "shape_predictor_68_face_landmarks.dat"
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(file_path)

    rectImages = []
    returnImages = []
    npImages = []

    # this list will hold npImages[] and images[]
    containerList = []

    # Go through the images
    # 1) Convert and save in grey scale
    # 2) Make a rectangle around the faces and save those rectangles coordinates
    for image in images:

        rectImages.append(detector(image,0)) # if multiple faces are detected, detctor() returns multiply lists

        if ((len(rectImages[len(rectImages) -1])) == 1): # if only one face is detected in the picture, add the image directly to the list
            returnImages.append(image)
        else: # if more than one face is detected, we have to 'cut' to save n number of images, where n is the number of faces in the image
            # take the rectangle out of a the 2D list, ensure rectImages stays a 1D list
            tempList = rectImages[len(rectImages) - 1]
            for i in range(len(tempList)):

                # crop out individal faces and save them
                x1 = tempList[i].tl_corner().x
                x2 = tempList[i].br_corner().x
                y1 = tempList[i].tl_corner().y
                y2 = tempList[i].br_corner().y
                face = image[y1:y2, x1:x2]

                returnImages.append(face)

                # have to use detector again so we save coordinates as a dlib.rectangles() object
                # I somehow like to be able to create dlib.rectangles() objects, haven't seen a way to
                # if I can create those objects, I won't have to use detector() again, which saves on processing power
                if i == 0:
                    rectImages[len(rectImages) -1] = detector(returnImages[len(returnImages)-1], 0)
                else:
                    rectImages.append(detector(returnImages[len(returnImages)-1], 0))

    counter = 0 # used to keep track of what image we are on, used with greyImages[]
    # For each detected face, find the landmark.
    # for (i, rect) in enumerate(rects):
    # Make the prediction of landmarks and transfom it to numpy array
    for rectImg in rectImages:
        for (i, rect) in enumerate(rectImg):
            npImages.append(face_utils.shape_to_np(predictor(returnImages[counter], rect)))
            counter = counter + 1

    containerList.append(npImages)
    containerList.append(returnImages)

    return containerList
def rectContains(rect, point):

    # if the x values are out of range
    if point[0] < rect[0]: return False
    if point[0] > rect[2]: return False

    # if the y values are out of range

    if point[1] < rect[1]: return False
    if point[1] > rect[3]: return False

    return True

# returns triangle indices of all the triangles. the indices are the landmark NUMBERS, not pixel coordinates
def calculateDelaunayTriangles(rect, points):
    subDivRect = cv2.Subdiv2D(rect)

    for p in points:
        subDivRect.insert((p[0], p[1]))

    detTrianglesList = subDivRect.getTriangleList() # if you draw the triangles, some of them will be out of the box, need to remove those indices
    delTri = []

    for t in detTrianglesList:
        singleTriangle = [] # stores the indices of t
        singleTriangle.append((t[0],t[1]))
        singleTriangle.append((t[2],t[3]))
        singleTriangle.append((t[4],t[5]))

        # check if the points are within the rectangle
        if (rectContains(rect, singleTriangle[0]) and rectContains(rect, singleTriangle[1]) and rectContains(rect,singleTriangle[2])):
            indices = []

            # we compare the single triangle indices with the the average landmark points
            # when the indice coordinate matches a landmark coordinate, we store that landmarks number (total of 76 landmarks)
            for a in range(0,3):
                for b in range (0,len(points)):
                    if (abs(singleTriangle[a][0] - points[b][0]) <1.0 and abs(singleTriangle[a][1] - points[b][1]) < 1.0): # check why comparing the values doesnt work here? it works when faceMorph.py is stand alone
                        indices.append(b)
            delTri.append(indices)

    return delTri

# Apply affine transform calculated using srcTri and dstTri to src and
# output an image of size.
def applyAffineTransform(src, srcTri, dstTri, size) :

    # Given a pair of triangles, find the affine transform.
    warpMat = cv2.getAffineTransform( np.float32(srcTri), np.float32(dstTri) )

    # Apply the Affine Transform just found to the src image
    dst = cv2.warpAffine( src, warpMat, (size[0], size[1]), None, flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT_101 )

    return dst

def constrainPoint(p, w, h) :
    p =  ( min( max( p[0], 0 ) , w - 1 ) , min( max( p[1], 0 ) , h - 1 ) )
    return p

# Warps and alpha blends triangular regions from img1 and img2 to img
def warpTriangle(img1, img2, t1, t2) :

    # Find bounding rectangle for each triangle
    r1 = cv2.boundingRect(np.float32([t1]))
    r2 = cv2.boundingRect(np.float32([t2]))

    # Offset points by left top corner of the respective rectangles
    t1Rect = []
    t2Rect = []
    t2RectInt = []

    for i in range(0, 3):
        t1Rect.append(((t1[i][0] - r1[0]),(t1[i][1] - r1[1])))
        t2Rect.append(((t2[i][0] - r2[0]),(t2[i][1] - r2[1])))
        t2RectInt.append(((t2[i][0] - r2[0]),(t2[i][1] - r2[1])))


    # Get mask by filling triangle
    mask = np.zeros((r2[3], r2[2], 3), dtype = np.float32)
    cv2.fillConvexPoly(mask, np.int32(t2RectInt), (1.0, 1.0, 1.0), 16, 0)

    # Apply warpImage to small rectangular patches
    img1Rect = img1[r1[1]:r1[1] + r1[3], r1[0]:r1[0] + r1[2]]

    size = (r2[2], r2[3])

    img2Rect = applyAffineTransform(img1Rect, t1Rect, t2Rect, size)

    img2Rect = img2Rect * mask

    # Copy triangular region of the rectangular patch to the output image
    img2[r2[1]:r2[1]+r2[3], r2[0]:r2[0]+r2[2]] = img2[r2[1]:r2[1]+r2[3], r2[0]:r2[0]+r2[2]] * ( (1.0, 1.0, 1.0) - mask )

    img2[r2[1]:r2[1]+r2[3], r2[0]:r2[0]+r2[2]] = img2[r2[1]:r2[1]+r2[3], r2[0]:r2[0]+r2[2]] + img2Rect


def run(celebDict, userPictureName, userPicture):

    path = "face_morph_app/images/"

    images = []

    if userPicture:
        images = readPictures(path,userPictureName)

    file_path = os.path.join(os.path.dirname(__file__), "celebs.txt")
    namesFile = open(file_path,"r",encoding="utf-8")


    # the path where the pictures are saved


    for name in celebDict:
        if name != "":
            url = celebDict[name]

            resp = urllib.request.urlopen(url)
            image = np.asarray(bytearray(resp.read()), dtype="uint8")
            image = cv2.imdecode(image, cv2.IMREAD_COLOR)
            images.append(image)


    containerList = landmarkOfImages(images)

    landMarks = containerList[0]
    images = containerList[1]


    for i in range (0, len(images)):
        images[i] = np.float32(images[i])/255.0

    # dimensions of output image, used to standardize input images to the same size
    h = 600
    w = 600

    # coordinates of the eye corners in a w * h adjusted image
    eyeDist = [(0.3 * w, h/3), (0.7 * w, h/3)]

    # landmark points added to corners of image and middle point of of them (excluding the center point)
    boundaryPts = np.array([(0,0), (w/2,0), (w-1,0), (w-1,h/2), ( w-1, h-1 ), ( w/2, h-1 ), (0, h-1), (0,h/2) ])

    # initialize average of all points array
    avgPoints = np.array([(0,0)] * ( len(landMarks[0]) + len(boundaryPts) ), np.float32())

    transformedPoints = []
    transformedImg = []
    for i in range(len(images)):
        singleImageLandmarks = landMarks[i]

        # formatting the coordinates of the eye corners: right eye x, right eye y, left eye x, left eye y
        oldEyePoints = [[landMarks[i][36][0], landMarks[i][36][1]], [landMarks[i][45][0], landMarks[i][45][1]]]

        tformPoints = similarityTransform(oldEyePoints, eyeDist) # check what this prints, tform needs to be a 2x3 matrix for .warpAffine(), but this returns tform[0] ????

        tformImage = cv2.warpAffine(images[i], tformPoints, (w,h)) # returns transformed image

        # transforming the landmarks
        newImageLandmarks = np.reshape(np.array(singleImageLandmarks), (68,1,2)) # changing the shape of the array
        newImageLandmarks = cv2.transform(newImageLandmarks, tformPoints) # returns the transformed landmarks
        newImageLandmarks = np.float32(np.reshape(newImageLandmarks, (68,2)))

        # add the boundary points into the array
        newImageLandmarks = np.append(newImageLandmarks, boundaryPts, axis = 0)

        # calculate the average value of the landmark points among all other images, add previous averages too
        avgPoints = avgPoints + newImageLandmarks / len(images)

        transformedPoints.append(newImageLandmarks)
        transformedImg.append(tformImage)

    # creating the Deluany triangles of the average face
    rect = (0,0,w,h) # rectangle bounding where the triangles will be

    # indices of triangles, indices = landmark #'s
    delTri = calculateDelaunayTriangles(rect, np.array(avgPoints))

    outputImg = np.zeros((h,w,3), np.float32())

    # now we have the average face landmarks
    # we transform all the images so that their Delauny triangles are warped to fit...
    # ...the Delauny triangles of the average face
    for i in range (len(transformedImg)):
        newImg = np.zeros((h,w,3), np.float32())

        # transform triangles
        for j in range (len(delTri)):
            triangleIn = []
            triangleOut = []
            for k in range (0,3):
                    pointsIn = transformedPoints[i][delTri[j][k]] # finding pixel values of the Delauny triangles, of the PRE warped image
                    pointsIn = constrainPoint(pointsIn,w,h)

                    pointsOut = avgPoints[delTri[j][k]] # finding the pixel value of the average landmarks, (aka what the POST warped image pixels will be)
                    pointsOut = constrainPoint(pointsOut,w,h)

                    # saving the pixel values of the landmarks of the average face & image
                    triangleIn.append(pointsIn)
                    triangleOut.append(pointsOut)

            # warping the images based on the delauny triangles of an average face
            warpTriangle(transformedImg[i], newImg, triangleIn, triangleOut)

        # Add image intensities for averaging
        outputImg = outputImg + newImg

    # Divide by numImages to get average
    outputImg = outputImg / len(images)
    outputImg = np.float32(outputImg) * 255.0

    path = "face_morph_app/static/face_morph_app/images"
    numberofimages = len(os.listdir(path = path)) # use this for naming convention

    morphName = "image" + str(numberofimages) + ".jpg"
    cv2.imwrite(os.path.join(path, morphName), outputImg)

    return morphName

