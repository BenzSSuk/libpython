import numpy as np
import cv2 
import os

folderImg = '/Users/pannawis/Projects/01_SmartMeter/SmartPowerMeter_SW/images/Digit/main_15A/preprocess_class_gen/7'
nameImg = '2_IMG_20210722_135642_Digit_3.jpg'

pathSave = folderImg + '/shift'

if not os.path.exists(pathSave):
    os.makedirs(pathSave)

nameImgWithoutExtend = nameImg.split('.')[0]

img = cv2.imread(folderImg + '/' + nameImg,0)
rows,cols = img.shape

# shift_x = 100
# shift_y = 50

for shift_x in np.arange(0,10,2):
    for shift_y in np.arange(-6,10,2):
        M = np.float32([[1,0,shift_x],[0,1,shift_y]])
        img_shifted = cv2.warpAffine(img,M,(cols,rows))

        nameSave = nameImgWithoutExtend + '_' + str(shift_x) + '_' + str(shift_y) + '.jpg'

        cv2.imwrite(pathSave + '/' + nameSave,img_shifted)







