import cv2
import numpy as np
framewidth = 640
framehight = 480
cap = cv2.VideoCapture(0)
cap.set(3,framewidth)
cap.set(4,framehight)
cap.set(10,150)
#[90, 48, 0, 118, 255, 255]

myColors = [[0,115,133,17,194,255], # those numbers are the filter we use to detect a certain color for example the first vector is for red and the second is for blue 
            [90,151,135,179,255,255]] # you should use the color detect code to get the right filter for the color you want to use 

myColorValues = [[0,0,255],   #BGR
                 [255,0,0]]
myPoints = []  ## [x , y , colorId ]


def findColor(img,myColors, myColorValues):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    count = 0
    newPoints =[]
    for color in myColors:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imgHSV,lower,upper)
        x, y = getContours(mask)
        cv2.circle(imgResult, (x, y), 10, myColorValues[count], cv2.FILLED)
        if x != 0 and y != 0:
            newPoints.append([x, y, count])
        count += 1
            # cv2.imshow(str(color[0]),mask)
    return newPoints

def getContours(img):
    contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    x,y,w,h = 0,0,0,0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area>500:
            #cv2.drawContours(imgResult, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt,True)
            approx = cv2.approxPolyDP(cnt,0.02*peri,True)
            x, y, w, h = cv2.boundingRect(approx)
    return x+w//2,y

def drawOnCanvas(mypoints,myColorValues):
    for point in mypoints:
        cv2.circle(imgResult,(point[0], point[1]), 2, myColorValues[point[2]], cv2.FILLED)





while True :
    success,img = cap.read()
    img = cv2.flip(img, 1)
    imgResult = img.copy()
    newPoints = findColor(img ,myColors,myColorValues)
    if len(newPoints) != 0:
        for newP in newPoints:
            myPoints.append(newP)
    if len(myPoints) != 0:
        drawOnCanvas(myPoints, myColorValues)
    cv2.imshow('imgresults', imgResult)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
