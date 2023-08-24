import numpy as np
import cv2 as cv

vdo_capture = cv.VideoCapture(0)
if not vdo_capture.isOpened():
    print("Cannot open camera")
    exit()

# sucess open camera
# get camera properties
w_frame = vdo_capture.get(cv.CAP_PROP_FRAME_WIDTH)
h_frame = vdo_capture.get(cv.CAP_PROP_FRAME_HEIGHT)
fs = vdo_capture.get(cv.CAP_PROP_FPS)

while True:
    # Capture frame-by-frame
    ret, frame = vdo_capture.read()
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    # Our operations on the frame come here
    frame_processed = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # Display the resulting frame
    cv.imshow('frame', frame_processed)

    # type 'q' to exit program
    if cv.waitKey(1) == ord('q'):
        break

# When everything done, release the capture
vdo_capture.release()
cv.destroyAllWindows()