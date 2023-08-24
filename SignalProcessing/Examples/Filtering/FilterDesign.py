import scipy.signal as spsig
import numpy as np
import matplotlib.pyplot as plt
import os
import sys

'''
    scipy.signal.firwin(numtaps, cutoff, width=None, window='hamming', pass_zero=True, scale=True, nyq=None, fs=None)
    
    Parameters
    numtapsint
        Length of the filter (number of coefficients, i.e. the filter order + 1). numtaps must be odd if a passband includes the Nyquist frequency.
    cutofff:loat or 1-D array_like
        Cutoff frequency of filter (expressed in the same units as fs) OR an array of cutoff frequencies (that is, band edges). In the latter case, the frequencies in cutoff should be positive and monotonically increasing between 0 and fs/2. The values 0 and fs/2 must not be included in cutoff.
    width:float or None, optional
        If width is not None, then assume it is the approximate width of the transition region (expressed in the same units as fs) for use in Kaiser FIR filter design. In this case, the window argument is ignored.
    window:string or tuple of string and parameter values, optional
        Desired window to use. See scipy.signal.get_window for a list of windows and required parameters.
    pass_zero: {True, False, ‘bandpass’, ‘lowpass’, ‘highpass’, ‘bandstop’}, optional
        If True, the gain at the frequency 0 (i.e., the “DC gain”) is 1. If False, the DC gain is 0. Can also be a string argument for the desired filter type 
        (equivalent to btype in IIR design functions).
        New in version 1.3.0: Support for string arguments.
    
    scale:bool, optional
        Set to True to scale the coefficients so that the frequency response is exactly unity at a certain frequency. That frequency is either:
        0 (DC) if the first passband starts at 0 (i.e. pass_zero is True)
        fs/2 (the Nyquist frequency) if the first passband ends at fs/2 (i.e the filter is a single band highpass filter); center of first passband otherwise
    nyq:float, optional
        Deprecated. Use `fs` instead. This is the Nyquist frequency. Each frequency in cutoff must be between 0 and nyq. Default is 1.
        fsfloat, optional
        The sampling frequency of the signal. Each frequency in cutoff must be between 0 and fs/2. Default is 2.
    Returns
        h(numtaps,): ndarray
        Coefficients of length numtaps FIR filter.
    Raises
        ValueError
        If any value in cutoff is less than or equal to 0 or greater than or equal to fs/2, if the values in cutoff are not strictly monotonically increasing, or if numtaps is even but a passband includes the Nyquist frequency.


f1, f2 = 0.1, 0.2
>>> signal.firwin(numtaps, [f1, f2], pass_zero=False)

'''

os.chdir('../../')
folderSignalProcessing = os.getcwd()

folderSaveCoeff = os.path.join(folderSignalProcessing, 'FilterCoefficient')

def generateSinWithNoise(ampl, offset, lenSig, f, fs, amplNoise = 0.15):
    Ts = 1/fs
    t = np.arange(0, lenSig, Ts)
    nPoints = len(t)
    y_noise = amplNoise * np.random.rand(nPoints)
    y = ampl * np.sin((2 * np.pi * f) * t) + offset
    y_meas = y + y_noise

    return y_meas, t

# ----- Test signal -----
fs = 5

fsignal = 0.4
lenSignal = 5 # sec
amplSignal = 1.5
amplNoise = 0.5
offSetSignal = 2

# ----- Filter coefficient -----
nameCoeff = 'bp_hamming_0f05-1Hz_5Hz_15.npy'
cutoff = [0.05, 1] # ppg 0.05 - 6 Hz
numtaps = 15 # normaly set as odd
window = 'hamming'
filterType = 'bandpass'

# test signal
y_low, t = generateSinWithNoise(0.5, 0, lenSignal, amplNoise, fs, 0)
y, t = generateSinWithNoise(ampl=amplSignal, offset=offSetSignal, lenSig=lenSignal, f=fsignal, fs=fs, amplNoise=0.5)
y = y + y_low

# generate coeff
filterCoeff = spsig.firwin(numtaps, cutoff, width=None, window=window, pass_zero=filterType, scale=True, nyq=None, fs=fs)
# save coeff
pathSaveCoeff = os.path.join(folderSaveCoeff, nameCoeff)
np.save(pathSaveCoeff, filterCoeff)

# filter signal
filterCoeff = np.load(pathSaveCoeff)
yFiltered = spsig.convolve(y, filterCoeff, method='direct', mode='same')

yFilteredBuff = yFiltered[~np.isnan(yFiltered)]
yFiltered = yFiltered - np.average(yFilteredBuff)

# plot
plt.plot(t, y, t, yFiltered)
# plt.plot(yFiltered)
plt.legend(['original', 'filtered'])
plt.xlabel('time(s)')
plt.show()


