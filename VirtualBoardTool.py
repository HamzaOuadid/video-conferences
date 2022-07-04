import cv2
import numpy as np
import time
import os
import HandTrackingModule as htm1

#######################
brushThickness = 8
eraserThickness = 100
#######################
folderPath = "Header"
myList = os.listdir(folderPath)
print(myList)
overlayList = []

for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)
print(len(overlayList))
header = overlayList[0]
drawColor = (255,0,0)
cap = cv2.VideoCapture(0)
cap.set(3, 1920)
cap.set(4, 1080)

detector = htm1.handDetector(detectionCon=0.85, maxHands=1)
xp, yp = 0, 0
imgCanvas = np.zeros((1080, 1920, 3), np.uint8)

while True:
    #importation d'image
    sucess, img = cap.read()
    img = cv2.flip(img, 1)
    #2.find hand landmarks
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:

        #tip of the index finger
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]
        #check which fingers are up
        fingers = detector.fingersUp()
        print(fingers)
        #4. id selection mode - two fingers are up
        if fingers[1] and fingers[2]:
            xp, yp = 0, 0
            # xp, yp = 0, 0
            print("Selection Mode")
            # # Checking for the click
            if y1 < 100:
                if 0 < x1 < 480:
                    header = overlayList[0]
                    drawColor = (0, 0, 255)
                elif 480 < x1 < 960:
                    header = overlayList[1]
                    drawColor = (0, 100, 0)
                elif 960 < x1 < 1440:
                    header = overlayList[2]
                    drawColor = (255, 255, 255)
                elif 1440 < x1 < 1920:
                    header = overlayList[3]
                    drawColor = (0, 0, 0)
            cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), drawColor, cv2.FILLED)

         #5. if drawing mode - inder finger is up
        if fingers[1] and fingers[2] == False:
            cv2.circle(img, (x1, y1), 15, drawColor, cv2.FILLED)
            print("Drawing Mode")
            if xp == 0 and yp == 0:
                xp, yp = x1, y1

            cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)
            cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)
            if drawColor == (0, 0, 0):
                 cv2.line(img, (xp, yp), (x1, y1), drawColor, eraserThickness)
                 cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, eraserThickness)

            else:
                 cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)
                 cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)
            xp, yp = x1, y1
         # Clear Canvas when all fingers are up
        if all (x >= 1 for x in fingers):
            imgCanvas = np.zeros((1080, 1920, 3), np.uint8)
D

    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img, imgInv)
    img = cv2.bitwise_or(img, imgCanvas)


    #setting the header image
    img[0:100, 0:1920] = header
    cv2.imshow("Image",img)
    cv2.waitKey(1)