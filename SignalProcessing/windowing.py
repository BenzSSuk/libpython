import math
import pandas as pd
import numpy as np

def findNumWindowMax(nPoints, fs, winSize, roundType='floor'):
    nPointsLastWin = 0
    if winSize > 0:
        lenSigSec = nPoints/fs
        if (lenSigSec % winSize) == 0:
            nWinMax = lenSigSec/winSize

        else:
            nWinMaxRaw = lenSigSec/winSize
            if roundType == 'floor':
                nWinMax = math.floor(nWinMaxRaw)

            elif roundType == 'up':
                nWinMax = math.ceil(nWinMaxRaw)
                nPointsLastWin = nPoints - (nWinMax - 1) * (winSize * fs)

    elif winSize == -1:
        # run all data not split window
        nWinMax = 1

    else:
        ValueError("winSize must > 0 or == -1")

    return nWinMax, nPointsLastWin

def isLastWindow(dfSignal, fs, winSize, iwin, roundType = 'floor'):
    nPoints = dfSignal.shape[0]

    nWinMax = findNumWindowMax(nPoints, fs, winSize, roundType=roundType)

    if iwin == nWinMax:
        return True

    else:
        return False

def checkIndexWindow(iwin):
    if iwin <= 0:
        raise ValueError(f'index window must >=1, input index:{iwin}')

def getIndexStartEndWindow(winSize, fs, iwin):
    checkIndexWindow(iwin)

    istart = (iwin - 1) * winSize * fs + 1
    istart = istart - 1

    iend = iwin * winSize * fs

    return istart, iend

def chopWindowByTime(dfSignal, fs, winSize, iwin, nWinMax = 0, paddingLastWindow = False,
                     nPointsLastWin=0, getIndex=False):
    '''
    iwin     sec                      range                   python range
    1       0 - winSize                 1 - winSize*fs               0 - winSize*fs
    2       winSize - 2*winSize    winSize*fs+1 - 2*winSize*fs       winSize*fs - 2*winSize*fs    

    Input:
        dfSignal: dataframe of raw signal
        fs: sampling rate (Hz)
        winSize: window size for chop signal (sec)
        iwin: index window and range in 1 to nWinMax    
    '''
    checkIndexWindow(iwin)

    if paddingLastWindow:
        roundType = 'up'
    else:
        roundType = 'floor'

    if winSize == -1:
        winSig = dfSignal

    elif winSize > 0:

        # istart = (iwin - 1) * winSize * fs + 1
        # istart = istart - 1
        # iend = iwin * winSize * fs
        istart, iend = getIndexStartEndWindow(winSize, fs, iwin)

        # isLastWin = isLastWindow(dfSignal, fs, winSize, iwin, roundType=roundType)
        isLastWin = (iwin == nWinMax)
        if not paddingLastWindow or (paddingLastWindow and not isLastWin):
            # python index start with 0
            winSig = dfSignal.iloc[istart:iend]

        elif paddingLastWindow and isLastWin:
            nPointsWindow = winSize*fs
            # select the last to the last elements
            if nPointsLastWin == 0:
                winSig = dfSignal.iloc[istart:iend]

            elif nPointsLastWin > 1:
                winSig = dfSignal.iloc[istart:-1]

            elif nPointsLastWin == 1:
                winSig = dfSignal.iloc[istart:istart+1]

            nrow, ncol = winSig.shape
            nPointsFil = nPointsWindow - nrow
            dfZero = pd.DataFrame(np.zeros((nPointsFil, ncol), dtype=int), columns=dfSignal.columns)
            winSig = pd.concat([winSig, dfZero])
            winSig.reset_index(inplace=True)

    if not getIndex:
        return winSig

    else:
        return winSig, istart, iend

def chopWindowByBackward(dfSignal, fs, winSize, indexLastPointInWindow):
    '''
    chop raw data "winSize" sec from the input "indexLastPoints" backward
    '''

    winSizePoints = winSize*fs

    iend = indexLastPointInWindow
    istart = iend - winSizePoints

    if istart < 0:
        raise ValueError(f'index start window < 0, istart:{istart}')

    winSig = dfSignal[istart:iend]

    return winSig

def slidingWindowByTime(dfSignal,fs,winSize,iwin,tslide):

    checkIndexWindow(iwin)

    istart = int((iwin-1)*tslide*fs+1)
    iend   = int(istart + winSize*fs -1)
        
    # python index start with 0
    winSig = dfSignal.iloc[istart-1:iend]

    return winSig

def concatWindow(dfConcat, df, nConcat, indexWindow):
    isReachedWindow = False
    if indexWindow % nConcat == 1:
        dfConcat = df

    else:
        dfConcat = pd.concat([dfConcat, df])

    if indexWindow % nConcat == 0:
        isReachedWindow = True

    return dfConcat, isReachedWindow
