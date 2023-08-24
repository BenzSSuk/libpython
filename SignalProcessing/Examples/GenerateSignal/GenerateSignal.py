import math
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import sys

import pandas as pd

print(os.getcwd())
nameSave = 'SimulateSignal_sin_noise.csv'
folderSave = os.path.join(os.getcwd(), 'output')

os.chdir("../../")
folderSignal = os.getcwd()
sys.path.append(folderSignal)
if not os.path.exists(folderSave):
    os.makedirs(folderSave)

import SignalProcessing as wedosig

# ----- Signal parameter -----
f_bpm = 80
f = f_bpm/60
lenSig = 5 # seconds
ampl = 0.4
offset = 2

# ----- Sampling parameter -----
fs = 100
Ts = 1/fs

# ----- Create signal -----
t = np.arange(0, lenSig - Ts, Ts)
nPoints = len(t)

# y_noise = np.random.randint(low=0, high=100, size=nPoints)
y_noise = 0.15*np.random.rand(nPoints)
y_sig = ampl*np.sin((2*math.pi*f)*t) + offset
y_meas = y_sig + y_noise

# ----- Analog to digital -----
'''
vref = 3.3
bitRes = 19 bits >> 2^19 >> 524288
analog      digital
 vref       524288
 x          524288(x)/vref
'''
vRef = 3
bitRes = 19
digitalMax = math.pow(2, bitRes) - 1

y_meas_digital = np.floor((digitalMax * y_meas) / vRef)
y_meas_digital = y_meas_digital.astype(int)

# ----- Plot -----
# plt.figure(1)
# plt.plot(y_meas)
#
# plt.figure(2)
# plt.plot(y_meas_digital)
# plt.show()

# ----- Save -----
dictFeat = {}

wedosig.addFeatureToDict(dictFeat, 'device', ['simulate']*nPoints, 'extenRow')
wedosig.addFeatureToDict(dictFeat, 't', t, 'extenRow')
wedosig.addFeatureToDict(dictFeat, 'y', y_meas_digital, 'extenRow')

df = pd.DataFrame(dictFeat)
pathSave = os.path.join(folderSave, nameSave)
df.to_csv(pathSave, index = False)



