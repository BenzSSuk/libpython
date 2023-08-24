'''
Objective: 
    Log size of image into table
'''
import sys
import pandas as pd 
import os
import cv2

folderProj = ['/Users/pannawis/Projects/01_SmartMeter/SmartPowerMeter_SW']
for ipath in folderProj:
    if not(ipath in sys.path):
        print(f'Adding path:{ipath}')
        sys.path.append(ipath)

# import wedoimage as wedoimg
# from wedoimage import*
import ImageProcessing as wedoimg
import SignalProcessing as wedosig

# folderImg = os.path.join(folderProj,'images','BoxMeter','ArtHome_TestApp01')
folderImg = input('path to folder img:')
pathReport = os.path.join(folderProj,'Report','Size')
if not os.path.exists(pathReport):
    os.makedirs(pathReport)
nameReport = 'tableSize_ArtHome_TestApp02.csv'

print('Listing file...')
listFil_dir, listFil_folder, listFil_name = wedoimg.findFile(folderImg,'*.jpg',-1)

nFiles = len(listFil_name)
ibox = []
nameID_log = []
nameFull_log = []
dictRef = {'nameFull':[], 'nameImg':[], 'brand':[], 'condition':[], 'ibox':[], 'row':[], 'col':[] }

print('Logging...')
for ifile in range(nFiles):
    print(f'ifile:{ifile+1}/{nFiles}')
    nameFull = listFil_name[ifile]

    nameSplitBuff = listFil_dir[ifile].split('/')
    nSplits = len(nameSplitBuff)

    nameFullSplitBuff = nameFull.split('_')
    # nameImg = nameFullSplitBuff[]

    imgRead = cv2.imread(listFil_dir[ifile])
    h,w,nCHs = imgRead.shape

    # nameImg = ''
    count = 0
    for nameBuff in nameFullSplitBuff:
        count = count + 1
        if count == 2:
            nameImg = nameBuff
        elif count > 2:
            nameImg = nameImg + '_' + nameBuff

    ibox = nameFullSplitBuff[0]

    folderCondition = nameSplitBuff[nSplits-2]
    folderBrand = nameSplitBuff[nSplits-3]

    # nameID = nameSplitBuff[1] + '_' + nameSplitBuff[2] + '_' + nameSplitBuff[3]
    # if not ('.jpg' in nameID):
    #     nameID = nameID + '.jpg'

    dictRef['nameFull'].append(nameFull)
    dictRef['nameImg'].append(nameImg)
    dictRef['brand'].append(folderBrand)
    dictRef['condition'].append(folderCondition)
    dictRef['ibox'].append(ibox)
    dictRef['row'].append(h)
    dictRef['col'].append(w)

# dictName = {'name':nameID_log, 'nameFull':nameFull_log, 'brand':listFil_folder, 'ibox':ibox}

print('Exporting...')
dfName = pd.DataFrame(dictRef)
# dfName.to_csv('/Users/pannawis/Projects/01_SmartMeter/SmartPowerMeter_SW/Report/Ref/tableName_brand.csv')
dfName.to_csv(pathReport + '/' + nameReport)

print('#---- Finished ! ----#')