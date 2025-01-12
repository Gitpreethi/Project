import cv2
import os
import time
import HandtrackingModule as htm

Wcam,Hcam=640,480
cap=cv2.VideoCapture(0)

cap.set(3,Wcam)
cap.set(4,Hcam)

folderPath="Finger"
myList=os.listdir(folderPath)
print(myList)
overlayList=[]
for imPath in myList:
    image=cv2.imread(f'{folderPath}/{imPath}')
    print(f'{folderPath}/{imPath}')
    overlayList.append(image)

print(len(overlayList))

pTime=0

detector=htm.handDetector(detectionCon=0.75)

tipid=[4,8,12,16,20]
while True:
    success,img=cap.read()
    img=detector.findHands(img)
    lmList=detector.findPosition(img,draw=False)
    #print(lmList)

    if len(lmList)!=0:
        fingers=[]

        if lmList[tipid[0]][1]>lmList[tipid[0]-1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        for id in range(1,5):
           

           if lmList[tipid[id]][2]<lmList[tipid[id]-2][2]:
               fingers.append(1)
           else:
               fingers.append(0)
        
        #print(fingers)
        totalfingers=fingers.count(1)
        print(totalfingers)
        #h,w,c=overlayList[totalfingers-1].shape
        #img[0:h,0:w]=overlayList[totalfingers-1]

        cv2.rectangle(img,(20,325),(170,475),(0,255,0),cv2.FILLED)
        cv2.putText(img,str(totalfingers),(45,475),cv2.FONT_HERSHEY_PLAIN,10,(255,0,0),25)

    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime
    cv2.putText(img,f'FPS:{int(fps)}',(400,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)
    cv2.imshow("Image",img)
    cv2.waitKey(1)  
