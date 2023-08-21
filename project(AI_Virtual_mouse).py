# pip install opencv-contrib-python
# pip install numpy
# pip install -U autopy


import cv2
import numpy as np
import HandTrackingModule as htm
import time
import autopy

frmaeR=100
smoothing=5 #used for remove shaking the mouse
plocx,plocy=0,0
clocx,plocy=0,0
pTime=0

cap=cv2.VideoCapture(0)
cap_w,cap_h=620,480
cap.set(3,cap_w)
cap.set(3,cap_h)

wscr,hscr=autopy.screen.size()
#print(wscr,hscr)

detector=htm.handDetector(detectionCon=0.7,maxHands=1)
while True:

    success,img=cap.read()
    img=cv2.flip(img,1)

    img=detector.findHands(img)
    lmlist,bbox=detector.findPosition(img)
   
    if len(lmlist)!=0:

        x1,y1=lmlist[8][1:]
        x2,y2=lmlist[12][1:]
        #print(x1.y1,x2,y2

        fingers=detector.fingersUp()
        #print(fingers)
        cv2.rectangle(img,(frmaeR,frmaeR),(cap_w-frmaeR,cap_h-frmaeR),(255,0,255)) 

        if fingers[1]==1 and fingers[2]==0:
  
            conv_x=int(np.interp(x1,(frmaeR,cap_w-frmaeR),(0,wscr)))
            conv_y=int(np.interp(y1,(frmaeR,cap_h-frmaeR),(0,hscr)))

            clocx=plocx+(conv_x-plocx)/smoothing
            clocy=plocy+(conv_y-plocy)/smoothing


            cv2.circle(img,(x1,y1),5,(0,255,255),10)
            autopy.mouse.move(clocx,clocy)
            plocx,plocy=clocx,clocy
        
        if fingers[1]==1 and fingers[2]==1: 

            length,img,lineinfo=detector.findDistance(8,12,img)  #we need to find distence between index and middle finger
            #print(length)
            
            if length<=40:                                         #click thte mouse  if the distence is short
                cv2.circle(img,(lineinfo[4],lineinfo[5]),15,(0,255,0),cv2.FILLED)
                autopy.mouse.click()
     
    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime
    cv2.putText(img,str(int(fps)),(20,50),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)
    
    cv2.imshow('webcam',img)
    if cv2.waitKey(1) & 0xFF==27:
        break
cap.release()
cv2.destroyAllWindows()
 

    