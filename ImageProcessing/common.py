import cv2
import os
import numpy as np
import glob

# from numpy.core.fromnumeric import shape
def findFile(pathSearch, stringSearch, nSubFolderSearch=0):
    '''
        Example

        folderA
            |
            ---file01.csv     --\
            ---file02.csv        > nSubFolderSearch = 0  
            ---file03.csv     --/
            ---folderB
                |
                ---file04.csv   --\
                ---file05.csv      >  nSubFolderSearch = 1
                ---file06.csv   --/

        Input:
            pathSearch = ...\...\folderA
            stringSearch = '*.csv' >> all file that contain .csv
                         = '*' >> all folder or file in pathSearch
            nSubFolderSearch = 0

        output: file01.csv,file02.csv,file03.csv

        Input:
            pathSearch = ...\...\folderA
            stringSearch = '*.csv' >> all file that contain .csv
            nSubFolderSearch = 1

        output: file04.csv, file05.csv, file06.csv
    '''
    os.chdir(pathSearch)
    listFileAll = glob.glob('**/{}'.format(stringSearch), recursive=True)

    # nSubFolderSearch = nSubFolderSearch + 1
    nFileFound = len(listFileAll)
    listFil_folder = []

    listFil_name = []
    listFil_dir = []
    for ifile in range(nFileFound):
        listFileIn = listFileAll[ifile]
        if '/' in listFileIn:
            # dir from mac and linux
            listSplit = listFileIn.split('/')
            folderFile = listSplit[-2]
            fileName = listSplit[-1]
            nSplit = len(listSplit)
        elif '\\' in listFileIn:
            # dir from window
            listSplit = listFileIn.split('\\')
            folderFile = listSplit[-2]
            fileName = listSplit[-1]
            nSplit = len(listSplit)
        else:
            folderFile = listFileIn
            fileName = listFileIn
            nSplit = 1

        if nSubFolderSearch == -1 or (nSplit - 1) == nSubFolderSearch:
    
            listDirFile = os.path.join(pathSearch,listFileIn)
            #        print('loading...')

            listFil_dir.append(listDirFile)

            listFil_name.append(fileName)
            
            listFil_folder.append(folderFile)

    return listFil_dir, listFil_folder, listFil_name
    
def imwrite(folderSave,nameSave,img):
    if not os.path.exists(folderSave):
        os.makedirs(folderSave)
    if len(img) > 0:
        cv2.imwrite(os.path.join(folderSave,nameSave), img)
    else:
        print('Image is empty !')

def filterQuadrant(arrX,arrY,xcen,ycen,q):
    if q == 1:
        arrX_q = arrX[arrX >= xcen]
        arrY_q = arrY[arrY >= ycen]
    elif q == 2: 
        arrX_q = arrX[arrX < xcen]
        arrY_q = arrY[arrY >= ycen]
    elif q == 3:
        arrX_q = arrX[arrX < xcen]
        arrY_q = arrY[arrY < ycen]
    elif q == 4:
        arrX_q = arrX[arrX >= xcen]
        arrY_q = arrY[arrY < ycen]
    
    return arrX_q,arrY_q

def imreadFromPath(listImg):
    nImgs = len(listImg)

    imgInit = cv2.imread(listImg[0])
    nDims = len(imgInit.shape)
    if nDims == 3:
        flagColor = 1
        h,w,nCH = imgInit.shape
        imgAll = np.zeros((nImgs,h,w,nCH),dtype='uint8')
    elif nDims == 2:
        flagColor = 0
        h,w =imgInit.shape
        imgAll = np.zeros((nImgs,h,w,1),dtype='uint8')

    # print('Loading datasets...')
    countImg = -1
    for pathImg in listImg:
        countImg = countImg + 1

        img_read = cv2.imread(pathImg,flagColor)   
        nDims = len(img_read.shape)

        if countImg > 0 and nDims != nDimPrev:
            ValueError('Support only same type of image in folder, RGB or gray scale')

        if nDims == 3:
            imgAll[countImg,:,:,:] = img_read
        elif nDims == 2:
            imgAll[countImg,:,:,0] = img_read

        nDimPrev = nDims

    return imgAll

def imreadInFolder(pathFolder,imgExtension):
    listDir, listFolder, listName = findFile(pathFolder,imgExtension,0)

    imgAll = imreadFromPath(listDir)

    return imgAll
    
def distance(coorA,coorB,distType):
    '''
    coorA = matric of coordinate of point A
    coorB = matric of coordinate of point B
    coor format
    coor = [x1,y1,z1,
           x2,y2,z2,
                 ...]
    * dimension in column and instance in row
    '''
    shapeA = coorA.shape
    shapeB = coorB.shape

    if len(shapeA)==1:
        coorA = coorA.reshape(1,coorA.size)
        shapeA = coorA.shape
    if len(shapeB)==1:
        coorB = coorB.reshape(1,coorB.size)
        shapeB = coorB.shape

    if shapeA[1] != shapeB[1]:
        ValueError('Shape must match in column !')

    if distType == 'euclidean':
        # axis=1 >> concat by col
        # arrDiff = np.concatenate((arrX-xref,arrY-yref),axis=1)

        # axis=1 >> norm array in each row
        # calculate euclidean
        matDist = np.linalg.norm(coorA - coorB, ord=2, axis=1)
    
    return matDist

def minkowski(coorA,coorB,p):
    matDist = np.linalg.norm( (coorA - coorB) , ord=p, axis=1)

    return matDist

