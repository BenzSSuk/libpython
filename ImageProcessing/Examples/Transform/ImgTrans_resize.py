import cv2
import matplotlib.pyplot as plt
import numpy as np
import glob 
import os 

folderIm = '/Users/pannawis/Projects/01_SmartMeter/images/RealEnviron'
folderSave = '/Users/pannawis/Projects/01_SmartMeter/images/RealEnviron_640'


listPathImAll = getlist(folderIm,'.jpg',0)

if not os.path.exists(folderSave):
    os.makedirs(folderSave)

flagRead = 1
countFile=0
nFound=len(listPathImAll)
for ipath in listPathImAll:
    countFile=countFile+1
    print(f'i:{countFile}/{nFound}')
    img = cv2.imread(ipath,flagRead)

    imRatio = img.shape[1]/img.shape[0]
    ynew = 640
    # xnew = int(np.floor(ynew * imRatio))
    xnew = 640
    imgResized=cv2.resize(img,(xnew,ynew),cv2.INTER_AREA)

    fileName=ipath.split('/')[-1]
    cv2.imwrite(folderSave+'/'+fileName,imgResized)

print('#---- Finish ----#')