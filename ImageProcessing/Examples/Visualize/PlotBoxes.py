import os
import sys
import numpy as np
import cv2 
import matplotlib.pyplot as plt

folderProj = os.getcwd()

sys.path.append(folderProj)
import wedoimage as wedoimg

folderImg = folderProj + '/images/person'

pathImg = folderImg + '/Store_7.jpg'

img = cv2.imread(pathImg,1)
boxes = np.array([ [0.1,0.2,0.2,0.3], [0.5,0.6,0.6,0.7] ])

# imgOut = img.copy()
# ibox = 0
# imgOut = cv2.rectangle(imgOut,( int(boxes[ibox,0]), int(boxes[ibox,1]) ),
#                                 ( int(boxes[ibox,2]), int(boxes[ibox,3]) ),
#                                 (0,255,0),1)
# cv2.rectangle(imgOut,( int(20), int(20) ),
#                      ( int(100), int(100) ),
#                      (0,255,0),1)
plt.figure(1)
img_box = wedoimg.plotMultiBox(img,boxes)
wedoimg.imshowCV(img_box)
