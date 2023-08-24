import math
import numpy as np
import scipy.signal as spsig

# def bandwidthFromQF(filter_type, Q, f_center):
#     bw = None
#     if filter_type == 'notch':
#         bw = Q*f_center

#     return bw 

# def notch_r(bw):
#     ''' 
#     bw = -ln(r)
#     r = e^(-bw)
#     '''
#     r = math.pow(math.e, -bw)

#     return r

def iirNotchCoeff(w0, r, fs):
    ''' 
    r similar to filter quality 
    0.1 - 0.99
    larger mean better
    '''
    a = np.zeros((3))
    b = np.zeros((3))

    b[0] = 1
    b[1] = -2*math.cos(2*math.pi*w0/fs)
    b[2] = 1

    a[0] = 1
    a[1] = -2*r*math.cos(2*math.pi*w0/fs)
    a[2] = r*r

    # bw = -math.log(r)

    return b, a

def filterSecondOrder(y_meas, b, a):
    '''
    w0 = fsignal
    y_fitered = y_meas - f_signal component
                = y_noise

    y_signal_clean = y_meas - y_noise
                    = y_meas - y_filtered
    '''

    y_filtered = np.zeros_like(y_meas)

    for i in range(y_meas.size):
        if i >= 2:
            # y_filtered[i] = b[0]*y_meas[i] + b[1]*y_meas[i-1] + b[2]*y_meas[i-2] + a[1]*y_filtered[i-1] + a[2]*y_filtered[i-2]
            y_filtered[i] = y_meas[i] + b[1]*y_meas[i-1] + y_meas[i-2] - a[1]*y_filtered[i-1] - a[2]*y_filtered[i-2]

    # y_out = y_meas - y_filtered

    return y_filtered

def iirNotch(y, f, r, fs, manual=False):

    if isinstance(f, list):
        y_filtered = y.copy()
        for f_notch in f:
            b, a = iirNotchCoeff(f_notch, r, fs)
            if manual:
                y_filtered = filterSecondOrder(y_filtered, b, a)

            else:
                y_filtered = spsig.filtfilt(b, a, y_filtered)

    elif isinstance(f, (int, float)):
        b, a = iirNotchCoeff(f, r, fs)
        if manual:
            y_filtered = filterSecondOrder(y, b, a)

        else:
            y_filtered = spsig.filtfilt(b, a, y)

    return y_filtered
