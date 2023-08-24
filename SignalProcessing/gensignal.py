import numpy as np

def generateSinWithNoise(ampl, offset, lenSig, f, fs, amplNoise = 0.15, offsetTime = 0):
    Ts = 1/fs
    t = np.arange(0, lenSig, Ts)

    # time shift
    if offsetTime > 0:
        t = t + offsetTime

    nPoints = len(t)
    y_noise = amplNoise * np.random.rand(nPoints)
    y = ampl * np.sin((2 * np.pi * f) * t) + offset
    y_meas = y + y_noise

    return y_meas, t