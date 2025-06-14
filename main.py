import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math
import subprocess

## Volume Funcitons
def set_mac_volume(volume_level):
    volume_level = max(0, min(100, int(volume_level)))
    script = f"set volume output volume {volume_level}"
    subprocess.run(["osascript", "-e", script])


wCam, hCam = 1280, 720

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0
vol=0
volBar=400
volPer=0

detector = htm.handDetector(detectionCon=0.7)




while True:
    success, img = cap.read()

    img = detector.findHands(img)
    lmList, x= detector.findPosition(img, draw=False)
    if len(lmList)!=0:

        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]

        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        cv2.circle(img, (x1, y1), 15, (255, 0, 0), cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (255, 0, 0), cv2.FILLED)

        cv2.line(img, (x1,y1),(x2,y2),(255,0,0), 3)
        cv2.circle(img, (cx, cy), 15, (255, 0, 0), cv2.FILLED)

        length = math.hypot(x2 - x1, y2 -y1)

        vol = np.interp(length, [50,300],[0, 100])
        volBar = np.interp(length, [50, 300], [400, 150])
        volPer = np.interp(length, [50, 300], [0, 100])
        set_mac_volume(vol)


        if length < 50:
            cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)
        if length > 300:
            cv2.circle(img, (cx, cy), 15, (0, 0, 255), cv2.FILLED)


    cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 3)
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (255, 0, 0), cv2.FILLED)
    cv2.putText(img, f'{int(volPer)} %', (40, 450),
                cv2.FONT_HERSHEY_COMPLEX,
                1, (255, 0, 0), 3)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, f'FPS:{int(fps)}', (40,50),
                cv2.FONT_HERSHEY_COMPLEX,
                1, (255, 0, 0), 3)

    cv2.imshow("Img", img)
    if cv2.waitKey(1) & 0xFF==ord('d'):
        break

cap.realease()
cv2.destroyAllWindows
