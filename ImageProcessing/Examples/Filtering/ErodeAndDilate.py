from os import name
import cv2
import glob
import numpy as np
import sys

pathCustom = ['/Users/pannawis/Projects/01_SmartMeter/SmartPowerMeter_SW/ImageProcessing',
              '/Users/pannawis/Projects/01_SmartMeter/SmartPowerMeter_SW/SignalProcessing']
for ipath in pathCustom:
    if not(ipath in sys.path):
        print(f'Adding path:{ipath}')
        sys.path.append(ipath)

# import wedoimage as wedoimg
# from wedoimage import*
import wedoimage as wedoimg
import wedosignal as wedosig

for i in ['5','6','7','8','9']:
    folderImg = '/Users/pannawis/Projects/01_SmartMeter/SmartPowerMeter_SW/images/Digit/main_15A/train_shift_filter/' + str(i)
    folderSave = folderImg 

    print('list file...')
    # listImg = glob.glob(folderImg + '/*.jpg')
    listImg_abs, listImg_folder, listImg_name = wedoimg.findFile(folderImg,'*.jpg',0)
    nImgs = len(listImg_name)
    # writeImg = int(input('write image ?\n>'))
    writeImg =1

    countImg = -1
    for pathImg in listImg_abs:
        countImg = countImg + 1
        print(f'analying {countImg+1}/{nImgs}...')
        nameImg = listImg_name[countImg]
        nameImgWithoutExtend = nameImg.split('.')[0]
        
        img_read = cv2.imread(pathImg,0)

        # erode
        kernel = np.ones((3,3),dtype='uint8')
        img_erode = cv2.erode(img_read, kernel, iterations=1)
        nameErode = nameImgWithoutExtend + '_e1.jpg' 

        # dilate
        kernel = np.ones((3,3),dtype='uint8')
        img_dilate = cv2.dilate(img_read,kernel, iterations=1)
        nameDilate = nameImgWithoutExtend + '_d1.jpg'
        if writeImg == 1:
            wedoimg.imwrite(folderSave,nameErode,img_erode)
            wedoimg.imwrite(folderSave,nameDilate,img_dilate)
        