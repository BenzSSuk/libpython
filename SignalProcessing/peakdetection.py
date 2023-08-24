import numpy as np

def peakdet(signal,fs,threshold,ampTH,distTH = [0.27,2]):
    '''
    This code start with finding peak and ignore all valley before it.
    signal      : input signal with fixed sampling rate
    threshold   : start find peak when signal[i] greater than threshold

    ampTH : After found peak and valley, find amp=abs(peak_y - valley_y),
            Then, keep only founded peak and valley that has amp greater than threshold
    distTH : dist_time = (valley_x - peak_x)/fs  and dist greater than distTH
            dist_time = Tpulse/2
            HR = [30 - 220 bpm], [0.5 - 3.667 Hz]
            Ts = [2 - 0.2727] sec
    '''
    peakInfo = {'pos':[], 'val':[]}
    valleyInfo = {'pos':[], 'val':[]}

    findPeakOrValley = 'init' # 0=not start finding, 1=find max, 2=find valley

    nPoints = len(signal)
    if nPoints >= 3:
        for i in np.arange(1,nPoints-1,1):
            currVal = signal[i]
            prevVal = signal[i-1]
            nextVal = signal[i+1]

            if findPeakOrValley == 'init' and (currVal > threshold):
                findPeakOrValley = 'peak'

            if findPeakOrValley == 'peak':
                #       1
                #    1     1
                isPeakType1 = (currVal > prevVal) and (currVal > nextVal) 
                #       1  1
                #    1
                isPeakType2 = (currVal > prevVal) and (currVal == nextVal) 

                if isPeakType1==True or isPeakType2==True:
                    # Found peak
                    currPeak_val = currVal
                    currPeak_pos = i 
                    
                    findPeakOrValley = 'valley' 

            elif findPeakOrValley=='valley':
                # 1   1
                #   1
                isValleyType1 = (currVal < prevVal) and (currVal < nextVal)
                # 1
                #   1 1
                isValleyType2 = (currVal < prevVal) and (currVal == nextVal)
                #     1
                # 1 1
                isValleyType3 = (currVal == prevVal) and (currVal < nextVal)

                if isValleyType1 or isValleyType2 or isValleyType3:
                    # Found valley
                    findPeakOrValley='peak'

                    currValley_val = currVal
                    currValley_pos = i

                    isAmpPass = (np.abs(currValley_val - currPeak_val) >= ampTH)

                    periodPulseHalf = (currValley_pos - currPeak_pos)/fs
                    periodPulse = periodPulseHalf * 2
                    isDistPass = (periodPulse >= distTH[0] and periodPulse <= distTH[1])
                    
                    if isAmpPass==True and isDistPass==True:
                        peakInfo['pos'].append(currPeak_pos)
                        peakInfo['val'].append(currPeak_val)

                        valleyInfo['pos'].append(currValley_pos)
                        valleyInfo['val'].append(currValley_val)

    else:
        print('Data is too short !')

    return peakInfo, valleyInfo

def findAllPeakValley(signal, returnDict = True):
    '''
    Find all peak and valley position using diff method
    *using numpy operation(vectorize) if 10x faster than loop and conditioning in each point

    sig
    i  1 2 3 4 5 6 7  8  9 11 12  13  14
           o       o           o
         o   o   o    o     o      o
       o       o         o            o

    peak/valley           p   v   p   v
    i_sig             1,2,3,4,5,6,7,8,9,10
    i_diff              1,2,3,4,5,6,7,8, 9
    diff                +,+,-,-,+,+,-,-, +
    diff_sign           1,1,0,0,1,1,0,0, 1
    diff(diff_sign)       0,-,0,1,0,-,0, 1

    add zero Str/End  0,0,-,0,1,0,-,0,1, 0

    peak == -1            p       p
    valley == 1               v       v

    #        o   o   o                         o
    #    o               o                o
    # o                      o   o   o
    #
    # diff         1,2,3,4,5,6,7,8,9,0,1
    #                1,2,3,4,5,6,7,8,9,0
    #                +,+,0,0,-,-,0,0,+,+
    #                1,1,1,1,0,0,1,1,1,1
    #
    # diff(diff)       1,2,3,4,5,6,7,8,9
    #                  0,0,0,-,0,1,0,0,0
    '''

    signal = signal.flatten()

    # ----- Detect all peak and valley -----
    sigDiff = np.diff(signal)
    indexRise = (sigDiff >= 0)

    sigDiffSign = np.zeros_like(sigDiff)
    sigDiffSign[indexRise] = 1
    # sigDiff[~indexRise] = 0

    sigDiffDiff = np.diff(sigDiffSign)

    # insert 0 at start and end for compensate indexSigDiffDiff same as index signal
    sigDiffDiff = np.append(0, sigDiffDiff)
    sigDiffDiff = np.append(sigDiffDiff, 0)

    # find index peak
    peak_pos = np.argwhere(sigDiffDiff == -1)
    peak_pos = peak_pos.flatten()
    peak_val = signal[peak_pos]
    # find index valley
    valley_pos = np.argwhere(sigDiffDiff == 1)
    valley_pos = valley_pos.flatten()
    valley_val = signal[valley_pos]

    if returnDict:
        peakInfo = {}
        peakInfo['pos'] = peak_pos
        peakInfo['val'] = peak_val
        valleyInfo = {}
        valleyInfo['pos'] = valley_pos
        valleyInfo['val'] = valley_val

        return peakInfo, valleyInfo

    else:
        return peak_pos, peak_val, valley_pos, valley_val

def trimStartEndValley(peak_pos, peak_val, valley_pos, valley_val):
    # make sure it start with valley
    if (peak_pos.size > 0) and (valley_pos.size > 0) and (peak_pos[0] < valley_pos[0]):
        peak_pos = np.delete(peak_pos, 0, axis=0)
        peak_val = np.delete(peak_val, 0, axis=0)

    # make sure it end with valley
    if (peak_pos.size > 0) and (valley_pos.size > 0) and (peak_pos[-1] > valley_pos[-1]):
        peak_pos = np.delete(peak_pos, -1, axis=0)
        peak_val = np.delete(peak_val, -1, axis=0)

    return peak_pos, peak_val, valley_pos, valley_val

def peakdet2(signal, fs=0, threshold=0, ampTH=0, distTH = [0, 0], checkAmpLeft = False):
    '''
    This code start with finding peak and ignore all valley before it.
    signal      : input signal with fixed sampling rate
    threshold   : start find peak when signal[i] greater than threshold

    ampTH : After found peak and valley, find amp=abs(peak_y - valley_y),
            Then, keep only founded peak and valley that has amp greater than threshold
    distTH : dist_time = (valley_x - peak_x)/fs  and dist greater than distTH
            dist_time = Tpulse/2
            HR = [30 - 220 bpm], [0.5 - 3.667 Hz]
            Ts = [2 - 0.2727] sec
    '''
    peakInfo = {'pos': np.array([]), 'val': np.array([])}
    valleyInfo = {'pos': np.array([]), 'val': np.array([])}

    # findPeakOrValley = 'init' # 0=not start finding, 1=find max, 2=find valley

    peak_pos, peak_val, valley_pos, valley_val = findAllPeakValley(signal, returnDict=False)

    # ----- Filter out -----
    # we assume signal must start with valley and end with valley
    # make sure it start with valley
    peak_pos, peak_val, valley_pos, valley_val = trimStartEndValley(peak_pos, peak_val, valley_pos, valley_val)

    # check amplitude (peak - valley)
    amplLeftValley = peak_val - valley_val[:-1]
    amplRightValley = peak_val - valley_val[1:]
    if checkAmpLeft:
        indexAmplPass = (amplLeftValley > ampTH)

    else:
        indexAmplPass = (amplLeftValley > ampTH) & (amplRightValley > ampTH)

    if np.any(indexAmplPass):
        peak_pos = peak_pos[indexAmplPass]
        peak_val = peak_val[indexAmplPass]
        # insert true at the last true peak
        idxLastTrue = np.flatnonzero(indexAmplPass)[-1]
        indexAmplPassValley = np.insert(indexAmplPass, idxLastTrue, True)
        valley_pos = valley_pos[indexAmplPassValley]
        valley_val = valley_val[indexAmplPassValley]

        peakInfo['pos'] = peak_pos
        peakInfo['val'] = peak_val
        valleyInfo['pos'] = valley_pos
        valleyInfo['val'] = valley_val

    # else:
    #     peakInfo['pos'] = np.array([])
    #     peakInfo['val'] = np.array([])
    #     valleyInfo['pos'] = np.array([])
    #     valleyInfo['val'] = np.array([])

    return peakInfo, valleyInfo

def convertPeakValleyToPulse(peak_pos, peak_val, valley_pos, valley_val):
    '''
        Convert Peak & valley array to table of pulse info, each row represent pulse
    '''
    peak_pos, peak_val, valley_pos, valley_val = trimStartEndValley(peak_pos, peak_val, valley_pos, valley_val)

    pulseInfo = {}

    if valley_pos.size >= 2 and peak_pos.size >= 1:
        pulseInfo['valley1_pos'] = np.delete(valley_pos, -1, axis=0)
        pulseInfo['valley1_val'] = np.delete(valley_val, -1, axis=0)

        pulseInfo['peak_pos'] = peak_pos
        pulseInfo['peak_val'] = peak_val

        pulseInfo['valley2_pos'] = np.delete(valley_pos, 0, axis=0)
        pulseInfo['valley2_val'] = np.delete(valley_val, 0, axis=0)

    else:
        pulseInfo['valley1_pos'] = np.array([])
        pulseInfo['valley1_val'] = np.array([])

        pulseInfo['peak_pos'] = np.array([])
        pulseInfo['peak_val'] = np.array([])

        pulseInfo['valley2_pos'] = np.array([])
        pulseInfo['valley2_val'] = np.array([])

    return pulseInfo

def findAllPulse(signal):
    '''
        Find all peak & valley before convert to pulse format
    '''

    peak_pos, peak_val, valley_pos, valley_val = findAllPeakValley(signal, returnDict=False)

    pulseInfo = convertPeakValleyToPulse(peak_pos, peak_val, valley_pos, valley_val)

    pulseInfo['nPulses'] = pulseInfo['peak_pos'].size

    return pulseInfo

def findPulseAmplitude(valley1_val, peak_val, valley2_val):
    """
    find amplitude of each pulse

    Parameters
    ----------
        pulseInfo : output from "findAllPulse()" or "convertPeakValleyToPulse()"

    """
    # leftAmpArr = pulseInfo['peak_val'] - pulseInfo['valley1_val']
    leftAmpArr = peak_val - valley1_val
    # rightAmpArr = pulseInfo['peak_val'] - pulseInfo['valley2_val']
    rightAmpArr = peak_val - valley2_val

    meanAmpArr = (leftAmpArr + rightAmpArr)/2

    return leftAmpArr, rightAmpArr, meanAmpArr

def findPulseWidth(valley1_pos, valley2_pos):
    """

    """
    # pulseWidth = pulseInfo['valley2_pos'] - pulseInfo['valley1_pos']
    pulseWidth = valley2_pos - valley1_pos

    meanPulseWidth = np.average(pulseWidth)

    return pulseWidth, meanPulseWidth

def pulseToMatrix(pulseInfo):
    """

    parameters:
        pulseInfo   : dict variable, output from findAllPulse()

    """
    pulseMatrixVal = np.stack((pulseInfo['valley1_val'], pulseInfo['peak_val'], pulseInfo['valley2_val']), axis=-1)

    pulseMatrixPos = np.stack((pulseInfo['valley1_pos'], pulseInfo['peak_pos'], pulseInfo['valley2_pos']), axis=-1)

    return pulseMatrixPos, pulseMatrixVal

def normalizePulse(pulseInfo, normalizeType = "MaxMin"):
    """
    Normalize by (x - min) / (max - min)

    Normalize in each pulse

    """

    _, pulseMatrixVal = pulseToMatrix(pulseInfo)

    if normalizeType == "MaxMin":
        pulseValMin = np.min(pulseMatrixVal, axis=1).reshape((-1, 1))
        pulseValMax = np.max(pulseMatrixVal, axis=1).reshape((-1, 1))
        pulseMatrixNorm = (pulseMatrixVal - pulseValMin) / (pulseValMax - pulseValMin)

    pulseInfoNorm = {}
    pulseInfoNorm['valley1_pos'] = pulseInfo['valley1_pos']
    pulseInfoNorm['valley1_val'] = pulseMatrixNorm[:, 0]
    pulseInfoNorm['peak_pos'] = pulseInfo['peak_pos']
    pulseInfoNorm['peak_val'] = pulseMatrixNorm[:, 1]
    pulseInfoNorm['valley2_pos'] = pulseInfo['valley2_pos']
    pulseInfoNorm['valley2_val'] = pulseMatrixNorm[:, 2]

    return pulseInfoNorm

def findPulseAmplitudeRatio(pulseInfo):
    """
    AmplitudeRatio meant to equalization of leftAmp and rightAmp

    maxAmp = max(left, rightAmp)
    AmplitudeRatio = ( leftAmp + rightAmp ) / (2*maxAmp)
           o
          o o
         o   o         ampRatio = 1
     o  o     o  o
       o       o

           o
          o o
         o   o  o      ampRatio = 0.8
     o  o     o
       o

           o   o
          o  o
         o             ampRatio = 0.3
     o  o
       o
    """
    # ----- normalize each pulse -----
    pulseInfoNorm = normalizePulse(pulseInfo)

    # ----- pulse amp -----
    leftAmpArr, rightAmpArr, meanAmpArr = findPulseAmplitude(pulseInfoNorm['valley1_val'], pulseInfoNorm['peak_val'], pulseInfoNorm['valley2_val'])

    # ----- pulse amp ratio -----
    arrAmpGreater = np.zeros_like(leftAmpArr)

    indexLeftGreater = (leftAmpArr >= rightAmpArr)
    arrAmpGreater[indexLeftGreater] = leftAmpArr[indexLeftGreater]

    indexRightGreater = ~indexLeftGreater
    arrAmpGreater[indexRightGreater] = leftAmpArr[indexRightGreater]

    diffAmpRatio = (leftAmpArr + rightAmpArr) / 2*arrAmpGreater


    return diffAmpRatio, indexLeftGreater, indexRightGreater

# def filterPulse(pulseInfo, meanAmpTH = 0, pulseWidth = 0):
#     """
#     remove pulse that
#
#     Parameters
#     ----------
#         pulseInfo  : output from "findAllPulse()" or "convertPeakValleyToPulse()"
#         pulseAmpTH : threshold for remove pulse that amplitude less than this threshold
#         pulseWidth : threshold for remove pulse that width(valley1_pos to valley2_pos) out this range
#
#     Return:
#     -------
#         indexPassTrue
#
#     """
#     # find pulse amplitude
#     leftAmpArr, rightAmpArr, meanAmpArr = findPulseAmplitude(pulseInfo['valley1_val'], pulseInfo['peak_val'], pulseInfo['valley2_val'])
#
#     # find pulse width
#     pulseWidth, meanPulseWidth = findPulseWidth(pulseInfo['valley1_pos'], pulseInfo['valley2_pos'])
#
#     if (rightAmpArr / leftAmpArr) < 0.3:
#         # remove i valley1, peak, valley2 and change i+1 valley1 to i-1 valley1
#     pulseInfoFiltered
#
#     return pulseInfoFiltered

# def findPPG_Pulse