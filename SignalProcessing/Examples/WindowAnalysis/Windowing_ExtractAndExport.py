from SignalProcessing.extractfeature import addFeatures
import pandas as pd
import numpy as np
from scipy.fft import fft, fftfreq
import os
import sys

# please add folder of Git in VS code 
folderProj = '/Users/pannawis/Projects/03_FallDetection/FallDetection_SW/SignalProcessing'

# add custom module
sys.path.append(folderProj)
import wedosignal as wedosig

# ----- User input -----
twin = 5
tslide = twin
fs = 20

# folder of raw signal
folderFile = os.path.join(folderProj,'Rawsignal','SimulateTest')
# folder of export feature
folderFeature = os.path.join(folderFile,'Export','IndividualFiles')
folderFeatureComb = os.path.join(folderFile,'Export','Combined')

nameTableFeature = 'tableFeature_allFiles.csv'

# ----- Preallocate (No need to edit) -----
# list all file in folder
listFil_dir, listFil_folder, listFil_name = wedosig.findFile(folderFile,'*.csv',0)
nFiles = len(listFil_name)

# create folder for save file 
if not os.path.exists(folderFeature):
    os.makedirs(folderFeature)
if not os.path.exists(folderFeatureComb):
    os.makedirs(folderFeatureComb)


for ifile in range(nFiles):

    # read .csv file by iteration
    print(f'Extracting file {ifile+1}/{nFiles}')
    pathFile = listFil_dir[ifile]
    nameFile = listFil_name[ifile]

    dfSignal = pd.read_csv(pathFile,sep=';')

    # Extract information from filename 
    splitNameBuff = nameFile.split('_')
    nameSubject = splitNameBuff[1]
    event = splitNameBuff[2]
    irecord = splitNameBuff[3] 

    # no. of divided window -> change to overlaping window??
    nPointSig = dfSignal.shape[0]

    if tslide == twin:
        nWinMax = int( np.floor(nPointSig / (twin*fs)) )
    else:
        ValueError('Now this script not support tslide!=twin !')
    # elif tslide < twin:
    #     nWinMax = int( np.floor(nPointSig / (twin*fs)) ) - twin - 1
    # else:
    #     ValueError('tslide should <= twin !')

    dictFeats = {}
    # dictA = {'a':stringBuff,'b':stringBuff,'c':zerosBuff,'d':zerosBuff}
    countWin = 0
    for iwin in range(nWinMax):
        # some time user not start loop from zero
        countWin = countWin + 1

        winSig = wedosig.chopWindowByTime(dfSignal,fs,twin,countWin)
        nPointSigInWin = winSig.shape[0]

        # ----- Log experiment info -----
        dictFeats = wedosig.addFeatures(dictFeats,'subject',nameSubject)
        dictFeats = wedosig.addFeatures(dictFeats,'event',event)
        dictFeats = wedosig.addFeatures(dictFeats,'iwin',countWin)

        # ----- Extract feature in time domain -----
        y1 = winSig['sig_ch1']
        # mean
        meanSig = np.sum(y1)/nPointSigInWin
        dictFeats = wedosig.addFeatures(dictFeats,'mean',meanSig)

        # SD
        stdSig = np.std(y1)
        dictFeats = wedosig.addFeatures(dictFeats,'SD',stdSig)
        
        # ----- Extract feature in frequency domain -----
        y1 = winSig['sig_ch1']
        


    dfFeats = pd.DataFrame(dictFeats)