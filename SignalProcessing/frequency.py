import numpy as np
# from scipy.fft import fft, fftfreq
import scipy.fft as spfft
from .peakdetection import findAllPeakValley

# dubug only turn off when not use
import matplotlib.pyplot as plt

# -----------------------------------
# ---------- Preprocessing ----------
# -----------------------------------
def nextpow2(x):
    '''
    shift_bit_length(x)
    ref: https://stackoverflow.com/questions/14267555/find-the-smallest-power-of-2-greater-than-or-equal-to-n-in-python
        find the next power of 2
        in = 6
        out = 8

        in = 50
        out = 64

        in = 500
        out = 512
    '''

    return int(1<<(x-1).bit_length())

def BPMtoFrequency(rangeFreqBPM):
    rangeFreq = [0, 0]
    rangeFreq[0] = rangeFreqBPM[0] / 60
    rangeFreq[1] = rangeFreqBPM[1] / 60

    return rangeFreq

def padding(y, n=None, method='nextpow2', val=0):
    '''
    padding zero to the end of signal to length n
    '''

    signal_size = y.size

    if n is None:
        if method == 'nextpow2':
            n = nextpow2(signal_size)

    if n > signal_size:
        nPads = n - signal_size
        y_padded = np.concatenate([y, np.ones((nPads))*val])

        return y_padded

    elif n == signal_size:
        return y

    else:
        raise ValueError("n must > signal_size")

def findMaxFreq(y_freq_abs, x_freq):
    # --- Maximum frequency
    if y_freq_abs.size > 0:
        index_freqMax = np.argmax(y_freq_abs)
        fmax = x_freq[index_freqMax]
    else:
        fmax = np.nan

    return fmax

def getFreqAxis(signal_size, fs, method='scipy'):
    '''
    get only half side axis
    '''

    if method == 'scipy':
        x_freq = spfft.rfftfreq(signal_size, 1/fs)

    elif method == 'manual': 
        N_half = signal_size//2 + 1 # A//B = floor(A/B)
        stepFreq = fs/signal_size
        x_freq = np.arange(0, N_half) * stepFreq

    return x_freq

def getIndexInRange(x_freq, rangeFreq=[], rangeFreqIsBPM=False):
    '''
    Input:
        x_freq: frequency axis like created by fft.rfftfreq
    '''
    if isinstance(rangeFreq, list) and len(rangeFreq) == 2:
        if rangeFreqIsBPM:
            rangeFreq = BPMtoFrequency(rangeFreq)

        indexFreqRange = np.logical_and(x_freq >= rangeFreq[0], x_freq <= rangeFreq[1])

    else:
        raise ValueError("rangeFreq must be list, rangeFreq = [f1, f2]")

    return indexFreqRange

# -----------------------------------
# -------- Fourier transform --------
# -----------------------------------
def dft_eq(in_real, in_imag, signal_size, i_out, i_in):
    angle_rad = ( 2 * np.pi * i_out * i_in ) / signal_size

    e_real = np.cos(angle_rad)
    e_imag = np.sin(angle_rad)

    # ----- output real -----
    out_freq_real = in_real*e_real + in_imag*e_imag

    # ----- output imagine -----
    out_freq_imag = -in_real*e_imag + in_imag*e_real

    return out_freq_real, out_freq_imag

def rdft(y, fs, rangeFreq = [], rangeFreqIsBPM=False, n=None, removeOffset=True):
    '''
    Real discrete fourier transform, half size spectrum
    Input:
        Signal with time domain that conatin only real data
    Output:
        out_freq_real: 
        out_freq_imag:
        out_freq_power: 
    '''

    if removeOffset:
        y_nonoffset = y - np.mean(y)

    else:
        y_nonoffset = y.copy()

    # y_nonoffset = y_nonoffset / 10000

    if not n is None:
        y_nonoffset = padding(y_nonoffset, n)

    N = y_nonoffset.size
    N_half = N//2 + 1
    out_freq_real = np.zeros((N_half))
    out_freq_imag = np.zeros((N_half))
    out_freq_power = np.zeros((N_half))
    for i_freq in range(N_half):
        # loop in all data y_freq
        out_freq_real_sum = 0
        out_freq_imag_sum = 0
 
        # theta_rad_0 = ( 2 * math.pi * i_freq * 0 ) / N
        # theta_rad_1 = ( 2 * math.pi * i_freq * (N-1) ) / N
        # print(f'k:{i_freq} theta_rad[0]:{theta_rad_0} theta_rad[N-1]:{theta_rad_1}')
        for i_time in range(N):
            out_freq_real_buff, out_freq_imag_buff = dft_eq(y_nonoffset[i_time], 0, N, i_freq, i_time)

            out_freq_real_sum = out_freq_real_sum + out_freq_real_buff
            out_freq_imag_sum = out_freq_imag_sum + out_freq_imag_buff

        out_freq_real[i_freq] = out_freq_real_sum
        out_freq_imag[i_freq] = out_freq_imag_sum
        
        # ----- abs -----
        out_freq_power[i_freq] = np.sqrt( out_freq_real[i_freq]**2 + out_freq_imag[i_freq]**2 )
        # out_freq_power[i_freq] = out_freq_real[i_freq] ** 2 + out_freq_imag[i_freq] ** 2

    x_freq = getFreqAxis(N, fs)

    if rangeFreq:
        indexFreqInRange = getIndexInRange(x_freq, rangeFreq, rangeFreqIsBPM)
        
        return out_freq_real[indexFreqInRange], out_freq_imag[indexFreqInRange], out_freq_power[indexFreqInRange], x_freq[indexFreqInRange]

    return out_freq_real, out_freq_imag, out_freq_power, x_freq

def rfft(y, fs, rangeFreq = [], rangeFreqIsBPM=False, n=None, removeOffset=True, devMode=False):
    # signal_size = y.size
    if n is None:
        n = nextpow2(y.size)

    if removeOffset:
        y_nonoffset = y - np.mean(y)

    else:
        y_nonoffset = y.copy()

    # calculate Half side fft
    y_freq_complex = spfft.rfft(y_nonoffset, n)
    y_freq = np.abs(y_freq_complex)

    # create frequency axis
    x_freq = spfft.rfftfreq(n, 1/fs)

    if rangeFreq:
        indexFreqInRange = getIndexInRange(x_freq, rangeFreq, rangeFreqIsBPM)

        return y_freq[indexFreqInRange], x_freq[indexFreqInRange]

    return y_freq, x_freq

def fft(y, fs, rangeFreq = [], rangeFreqIsBPM=False, n=None, removeOffset=True, devMode=False):
    if rangeFreqIsBPM:
        rangeFreq = BPMtoFrequency(rangeFreq)

    Ts = 1/fs

    # 1. remove offset
    if removeOffset:
        y_nonoffset = y - np.mean(y)

    else:
        y_nonoffset = y.copy()

    # 2. Calculate FFT
    y_freq = spfft.fft(y_nonoffset, n=n)
    nPointSig = y_freq.size
    nPointSigHalf = int(nPointSig//2 + 1)

    # 3. Create frequency axis
    x_freq = spfft.fftfreq(nPointSig, Ts)

    # 4. Select only half side of spectrum
    y_freq_half = y_freq[0:nPointSigHalf]
    x_freq_half = x_freq[0:nPointSigHalf]

    # 5. Normaly output of fft contain real and imagine number
    # abs() for take magnitude
    y_freq_half_abs = np.abs(y_freq_half)

    if isinstance(rangeFreq, list):
        if len(rangeFreq) > 0:
            indexFreqRange = np.logical_and(x_freq_half >= rangeFreq[0], x_freq_half <= rangeFreq[1])
            x_freq_half_filtered = x_freq_half[indexFreqRange]
            y_freq_half_abs_filtered = y_freq_half_abs[indexFreqRange]

        else:
            x_freq_half_filtered = x_freq_half
            y_freq_half_abs_filtered = y_freq_half_abs
    else:
        raise ValueError("rangeFreq must be list, rangeFreq = [f1, f2]")

    fmax = findMaxFreq(y_freq_half_abs_filtered, x_freq_half_filtered)

    if devMode:
        logRawFreq = {}
        logRawFreq['y_freq_complex_half'] = y_freq_half
        logRawFreq['y_freq_abs_half'] = y_freq_half_abs
        logRawFreq['x_freq_half'] = x_freq_half
        logRawFreq['y_freq_abs_filtered'] = y_freq_half_abs_filtered
        logRawFreq['x_freq_filtered'] = x_freq_half_filtered

        return y_freq_half_abs_filtered, x_freq_half_filtered, fmax, logRawFreq

    else:
        return y_freq_half_abs_filtered, x_freq_half_filtered, fmax

# -----------------------------------
# ------------ Application ----------
# -----------------------------------

def areaFreqInRange(y_freq, x_freq, rangeFreq):
    # area under frequency
    # select range freq
    rangeFreq_LF = [0.04, 0.15]
    rangeFreq_HF = [0.15, 0.4]

    # f_win_HR = 0::fs_
    indexFreq = np.logical_and(x_freq >= rangeFreq[0], x_freq <= rangeFreq[1])
    areaInRange = np.trapz(y_freq[indexFreq], x_freq[indexFreq])

    return areaInRange

def findPeakFreq(y, fs, rangeFreq = [], rangeFreqIsBPM=False, n=None, devMode=False,
                methodFFT='rfft'):
    if rangeFreqIsBPM:
        rangeFreq = BPMtoFrequency(rangeFreq)

    if methodFFT == 'fft':
        if devMode:
            y_freq_abs, x_freq, fmax, logRawFreq = fft(y, fs=fs, rangeFreq=rangeFreq, n=n, devMode=devMode)

        else:
            y_freq_abs, x_freq, fmax = fft(y, fs=fs, rangeFreq=rangeFreq, n=n)
    
    elif methodFFT == 'rdft':
        real, imag, y_freq_abs, x_freq = rdft(y, fs, rangeFreq, n=n)

    elif methodFFT == 'rfft':
        y_freq_abs, x_freq = rfft(y, fs, rangeFreq=rangeFreq, n=n)

    # peak and find max peak
    peak_pos, peak_val, valley_pos, valley_val = findAllPeakValley(y_freq_abs, returnDict=False)

    # plt.figure(1)
    # plt.plot(x_freq, y_freq_abs)
    # plt.show()

    if len(peak_val) > 0:
        posMaxInPeak = np.argmax(peak_val)
        posMax = peak_pos[posMaxInPeak]

        fpeak_max = x_freq[posMax]

    else:
        # plt.figure(2)
        # plt.clf()
        # plt.subplot(211)
        # plt.plot(y, '-o')
        # plt.subplot(212)
        # plt.plot(x_freq, y_freq_abs, '-o')
        # plt.show()
        fpeak_max = np.nan


    if devMode:
        logRaw = {}
        logFeat = {}
        logFeat['peak_freq_pos'] = peak_pos
        logFeat['peak_freq_val'] = peak_val
        logFeat['peak_freq_pos_max'] = posMax
        logFeat['x_freq_peakMax'] = fpeak_max

        logRaw.update(logRawFreq)

        return fpeak_max, logRaw, logFeat

    else:
        return fpeak_max