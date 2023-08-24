import numpy as np
# import scipy.signal as spsig
import pandas as pd


def movemean(sig,nMean):
    '''
        i                 0 1 2 3 4 5 6 7  
        sig               1 1 1 1 1 1 1 1 1 1 1 1 
        winMean (5)       1 1 1 1 1
        out                       1
    '''

    sigOut = np.copy(sig)

    nLoop = len(sig) - (nMean - 1)
    for i in range(nLoop):
        indexStart = i 
        indexEnd = i + nMean - 1

        sigOut[indexEnd] = np.mean(sig[indexStart:indexEnd])        

    return sigOut

# def convolution(y, kernel, cutTransient=False):
#     '''
#     y        =  [1,2,3,4,5,6,7,8,9,10]
#     kernel   =  [1,2,3]
#
#     y        =    [0,0,1,2,3,4,5,6,7,8,9,10]
#     kernel   =    [3,2,1]
#                     [3,2,1]
#                       [3,2,1]
#     out      =         1,
#     '''
#     numtabs = kernel.size
#     y_size = y.size
#     y_padding = np.concatenate((np.zeros(numtabs-1), y))
#     for ik in range(ysize):
#         (y_padding[])
#         # imgOut[ir,ic]=np.dot(winImg,kernel)
#         imgOut[ir, ic] = np.tensordot(winImg, kernel, axes=2)

def deleteFirstNRow(df, nTransient):
    # delete first half
    dfOut = df.copy()
    dfOut.reset_index(inplace=True, drop=True)
    dfOut.drop(np.arange(0, nTransient), inplace=True)
    dfOut.reset_index(inplace=True, drop=True)

    return dfOut

def filter(y, filterCoeff, cutTransient = False, setZeroToTransient=False, subwindowProcess = False, bufferRawInit=[],
           fullOverlap = False):
    # if cutTransient:
    #     mode = 'valid'
    # else:
    #     mode = 'full'

    numtaps = len(filterCoeff)
    nTransient = numtaps - 1

    if subwindowProcess:
        y2 = np.concatenate((bufferRawInit, y))

    if fullOverlap:
        # only full overlap signal and kernel
        yFiltered = np.convolve(y, filterCoeff, mode='valid')

    else:
        #
        yFiltered = np.convolve(y, filterCoeff, mode='full')

        # cut transient at back
        yFiltered = yFiltered[0:-nTransient]

        if cutTransient:
            # cut transient at front
            yFiltered = yFiltered[nTransient:]

        elif setZeroToTransient:
            # yFiltered[0:nTransient] = 0
            yFiltered[0:nTransient] = yFiltered[nTransient]

    if subwindowProcess:
        nBuffers = numtaps - 1
        # select the last n element
        bufferForNextFilter = y[-nBuffers:]

        return yFiltered, bufferForNextFilter

    else:
        return yFiltered

def filterByHeader(df, listHeader, filterCoeff, newHeader = True, cutTransient = True, setZeroToTransient = False,
                   removeOffset = False, subwindowFilter = False, bufferPrevRaw = [], bufferPrevRawOnFile = False,
                   removeOffsetIn = True, fullOverlap = False):
    '''
        input:
            cutTransient: remove raw signal equal to size of filter coefficient
    '''

    # nRows = df.shape[0]
    numtaps = filterCoeff.size
    nTransient = numtaps - 1

    if subwindowFilter:
        # concat
        df = pd.concat((bufferPrevRaw, df))

    dfOut = df.copy()

    if cutTransient or fullOverlap:
        # output signal from filter is less than input
        # ,cut transient before log output

        # delete transient
        dfOut = deleteFirstNRow(dfOut, nTransient)

    for ih in range(len(listHeader)):
        header = listHeader[ih]
        y = df[header].to_numpy()

        if removeOffsetIn:
            y = y - np.mean(y)

        # filter signal
        if subwindowFilter:
            # add prev raw
            y = np.concatenate((bufferPrevRaw, y))

            yFiltered, bufferForNextFilter = filter(y, filterCoeff, cutTransient=cutTransient, setZeroToTransient=setZeroToTransient,
                                                    subwindowFilter=subwindowFilter,
                                                    fullOverlap=fullOverlap)

        else:
            yFiltered = filter(y, filterCoeff, cutTransient=cutTransient, setZeroToTransient=setZeroToTransient,
                               fullOverlap=fullOverlap)

        # remove offset
        if removeOffset:
            # yFiltered = dfOut[headerLog].to_numpy()
            yFilteredBuff = yFiltered[~np.isnan(yFiltered)]
            yFiltered = yFiltered - np.average(yFilteredBuff)

        # add new column name
        if newHeader:
            headerLog = header + '_filtered'

        else:
            headerLog = header

        dfOut[headerLog] = np.around(yFiltered, 4)

    # if cutTransient and not fullOverlap:
    #     dfOut = deleteFirstNRow(dfOut, nTransient)

    if subwindowFilter:
        return dfOut, bufferPrevRaw
    else:
        return dfOut
