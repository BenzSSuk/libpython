import numpy as np
import cv2 as cv
import os
import sys

folderProject = os.getcwd()

# Initialize
downFrame = 30

sys.path.append(folderProject+'/ImageProcessing')
import wedoimage as wedoimg

pathVideo = folderProject + '/video/web/Oxford_Shoppers.mp4' 
cap = cv.VideoCapture(pathVideo)

folderSaveImg = folderProject + '/images/export_frame/OxfordShoppers'

w_frame = cap.get(cv.CAP_PROP_FRAME_WIDTH)
h_frame = cap.get(cv.CAP_PROP_FRAME_HEIGHT)
fs = cap.get(cv.CAP_PROP_FPS)

countFrame = 0
while cap.isOpened():
    countFrame = countFrame + 1
    ret, frame = cap.read()
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    
    if countFrame == 1 or ( (countFrame % downFrame) == 0 ):
    # gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        nameImg = 'Frame_' + str(countFrame) + '.jpg'
        wedoimg.imwrite(folderSaveImg,nameImg,frame)

    # cv.imshow('frame', frame)
    # if cv.waitKey(1) == ord('q'):
    #     break
    
cap.release()
cv.destroyAllWindows()