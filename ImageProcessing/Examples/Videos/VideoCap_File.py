import numpy as np
import cv2 as cv
import os

folderProject = os.getcwd()

pathVideo = folderProject + '/video/web/walking_airport.mp4' 
cap = cv.VideoCapture(pathVideo)

w_frame = cap.get(cv.CAP_PROP_FRAME_WIDTH)
h_frame = cap.get(cv.CAP_PROP_FRAME_HEIGHT)
fs = cap.get(cv.CAP_PROP_FPS)

while cap.isOpened():
    ret, frame = cap.read()
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    cv.imshow('frame', gray)
    if cv.waitKey(1) == ord('q'):
        break
    
cap.release()
cv.destroyAllWindows()