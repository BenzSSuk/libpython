'''
Objective: 
    list filename of image into table, use for log other ref.
'''
import sys
import pandas as pd 
import os

folderProj = '/Users/pannawis/Projects/01_SmartMeter/SmartPowerMeter_SW'

sys.path.append(folderProj)

# pathCustom = ['/Users/pannawis/Projects/01_SmartMeter/SmartPowerMeter_SW']
# for ipath in pathCustom:
#     if not(ipath in sys.path):
#         print(f'Adding path:{ipath}')
#         sys.path.append(ipath)

# import wedoimage as wedoimg
# from wedoimage import*
import ImageProcessing as wedoimg
import SignalProcessing as wedosig

pathBrand = os.path.join(folderProj,'images','BoxMeter','ArtHome_TestApp01')
pathReport = os.path.join(folderProj,'Report','Ref')
nameReport = 'tableRef_ArtHome_TestApp01_listName.csv'

print('Listing file...')
listFil_dir, listFil_folder, listFil_name = wedoimg.findFile(pathBrand,'*.jpg',-1)

nFiles = len(listFil_name)
ibox = []
nameID_log = []
nameFull_log = []
dictRef = {'nameFull':[], 'nameImg':[], 'brand':[], 'condition':[], 'ibox':[], 'serial':[], 'digit_1':[],'digit_2':[],'digit_3':[],'digit_4':[],'digit_5':[], 'digit':[]}

print('Logging...')
for ifile in range(nFiles):
    nameFull = listFil_name[ifile]

    nameSplitBuff = listFil_dir[ifile].split('/')
    nSplits = len(nameSplitBuff)

    nameFullSplitBuff = nameFull.split('_')
    # nameImg = nameFullSplitBuff[]

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
    dictRef['serial'].append('')
    dictRef['digit_1'].append('')
    dictRef['digit_2'].append('')
    dictRef['digit_3'].append('')
    dictRef['digit_4'].append('')
    dictRef['digit_5'].append('')
    dictRef['digit'].append('')

# dictName = {'name':nameID_log, 'nameFull':nameFull_log, 'brand':listFil_folder, 'ibox':ibox}

print('Exporting...')
dfName = pd.DataFrame(dictRef)
# dfName.to_csv('/Users/pannawis/Projects/01_SmartMeter/SmartPowerMeter_SW/Report/Ref/tableName_brand.csv')
dfName.to_csv(pathReport + '/' + nameReport)

print('#---- Finished ! ----#')

