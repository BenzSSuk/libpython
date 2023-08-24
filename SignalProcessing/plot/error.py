import matplotlib.pyplot as plt
import numpy as np

def plotBlandAltman(ref, out):
    mean = (ref + out)/2
    diff = ref - out               # Difference between data1 and data2
    md = np.mean(diff)           # Mean of the difference
    sd = np.std(diff)            # Standard deviation of the difference

    plt.scatter(mean, diff)
    plt.axhline(md,           color='gray', linestyle='--')
    plt.axhline(md + 1.96*sd, color='gray', linestyle='--')
    plt.axhline(md - 1.96*sd, color='gray', linestyle='--')

    plt.xlabel('mean(ref, output)')
    plt.ylabel('error = ref - output')

def plotBlandAltmanDF(df, headerRef, headerOut):

    ref = df[headerRef]
    out = df[headerOut]

    plotBlandAltman(ref, out)
