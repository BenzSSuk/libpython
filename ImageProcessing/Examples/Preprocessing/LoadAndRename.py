import cv2
import glob
import os

# %%
## -- User input
flagRead=1 
folderImg='/Users/pannawis/Projects/01_SmartMeter/SmartPowerMeter_SW/images/BoxMeter_Mitsu_GoodBad/Bad'
folderSave = folderImg

listNewNameType = ['fromFolder','bySeq','custom']
print('Please select listNewNameType !')
for i, val in enumerate(listNewNameType):
    print(f'{i}: {val}')
newNameTypeSelect = int(input('>'))
newNameType = listNewNameType[newNameTypeSelect]

## -- Initialize
if not os.path.exists(folderSave):
    os.makedirs(folderSave)

listImg = glob.glob(folderImg + '/*.jpg')
nImgs = len(listImg)
countImg = 0

for ipathImg in listImg:
    countImg = countImg + 1
    print(f'img:{countImg}/{nImgs}')

    ## -- Extract name 
    splitBuff = ipathImg.split('/')
    
    # nameImg = splitBuff[-1]

    ## -- Load image
    img=cv2.imread(ipathImg,flagRead)

    # Set your new name
    if newNameType == 'fromFolder':
        folderName = splitBuff[len(splitBuff)-2] 
        nameExport = folderName + '_' + str(countImg) + '.jpg'

    elif newNameType == 'bySeq':
        nameExport = str(countImg) + '.jpg'

    elif newNameType == 'custom':
        # nameExport = ...
        pass
    else:
        ValueError(f'variable newNameType was not recognite !')

    cv2.imwrite(folderSave + '/' + nameExport,img)
