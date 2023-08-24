import numpy as np

def norm_maxmin(y):
    y_norm = (y - np.max(y)) / (np.max(y) - np.min(y))

    return y_norm