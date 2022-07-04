import cv2
import mediapipe as mp
import math


class handDetector:

    def __init__(self, mode=False, maxHands=1, detectionCon=0.5, TrackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.TrackCon = TrackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(static_image_mode=self.mode, max_num_hands=self.maxHands,
                                        min_detection_confidence=self.detectionCon,
                                        min_tracking_confidence=self.TrackCon)
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20]
        self.fingers = []
        self.lmList = []

    def findHands(self, img, draw=True, flipType=True):

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        h, w, c = img.shape
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:

                ## draw
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms,self.mpHands.HAND_CONNECTIONS)

        if draw:
            return img



    def fingersUp(self):
        fingers = []
        # Thumb
        if self.lmList[self.tipIds[0]][1] > self.lmList[self.tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # Fingers
        for id in range(1, 5):
            if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)


        return fingers

    def findPosition(self, img, handNo=0, draw=True):
            self.lmList = []
            if self.results.multi_hand_landmarks:
                myHand = self.results.multi_hand_landmarks[handNo]
                for id, lm in enumerate(myHand.landmark):
                    # print(id, lm)
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    #print(id,cx,cy)
                    self.lmList.append([id, cx, cy])
            return self.lmList



def main():
    cap = cv2.VideoCapture(0)
    detector = handDetector(detectionCon=0.8, maxHands=2)
    while True:
        # Get image frame
        success, img = cap.read()
        # Find the hand and its landmarks
        img = detector.findHands(img)
        # hands = detector.findHands(img, draw=False)  # without draw
        lmList = detector.findPosition(img)
        if len(lmList) != 0:
            print(lmList[4])
        # Display
        cv2.imshow("Image", img)
        cv2.waitKey(1)
if __name__ == "__main__":
    main()