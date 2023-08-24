import numpy as np

def interpAndResample(y, t, fs_resamp):
    # resampling for HRV
    Ts_resamp = 1 / fs_resamp
    x_resamp = np.arange(t[0], t[-1], Ts_resamp)
    y_resamp = np.interp(x_resamp, t, y)

    return y_resamp

def resampling(y, fs_old, fs_new):
    lenSig = y.size/fs_old
    Ts_old = 1/fs_old
    t = np.arange(0, lenSig, Ts_old)

    if fs_new > fs_old:
        # upsampling
        y_resamp = interpAndResample(y, t, fs_new)

    elif fs_new < fs_old:
        # downsampling
        print('not support')

    return y_resamp
