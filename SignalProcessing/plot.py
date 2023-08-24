# import matplotlib.pyplot as plt
# import numpy as np
#
# def plotPeakValley(figNum, signal, peakInfo, valleyInfo=[], input='peak'):
#
#     plt.figure(figNum)
#     x = np.arange(0, len(signal))
#
#     plt.plot(x, signal)
#     if input == 'peak':
#         plt.scatter(peakInfo['pos'], peakInfo['val'], c='red')
#         plt.scatter(valleyInfo['pos'], valleyInfo['val'], c='blue')
#
#     elif input == 'pulse':
#         # peakInfo = pulseInfo
#         plt.scatter(peakInfo['peak_pos'], peakInfo['peak_val'], c='red')
#         plt.scatter(peakInfo['valley1_pos'], peakInfo['valley1_val'], c='blue')
#         plt.scatter(peakInfo['valley2_pos'], peakInfo['valley2_val'], c='blue')
#
# def plotBlandAltman(ref, out):
#     mean = (ref + out)/2
#     diff = ref - out               # Difference between data1 and data2
#     md = np.mean(diff)           # Mean of the difference
#     sd = np.std(diff)            # Standard deviation of the difference
#
#     plt.scatter(mean, diff)
#     plt.axhline(md,           color='gray', linestyle='--')
#     plt.axhline(md + 1.96*sd, color='gray', linestyle='--')
#     plt.axhline(md - 1.96*sd, color='gray', linestyle='--')
#
#     plt.xlabel('mean(ref, output)')
#     plt.ylabel('error = ref - output')
#
# def plotBlandAltmanDF(df, headerRef, headerOut):
#
#     ref = df[headerRef]
#     out = df[headerOut]
#
#     plotBlandAltman(ref, out)
