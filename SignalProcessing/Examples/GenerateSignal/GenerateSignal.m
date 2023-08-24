
fs = 125
Ts = 1/fs
y = []

folderSignal = pwd()
folderSave = 


ampl = 1.5
lenSig = 60*5 # seconds
t = 0:Ts:lenSig - Ts
nPoints = length(t)
f = 10  # Hz
yi = ampl*sin(2*( %pi)*f*t) + rand(nPoints)/2
y = [y yi]

lenSig = 60*5 # seconds
t = 0:Ts:lenSig - Ts
f = 13  # Hz
yi = ampl*sin(2*( %pi)*f*t) + rand(nPoints)/2
y = [y yi]

lenSig = 60*5 # seconds
t = 0:Ts:lenSig - Ts
f = 10  # Hz
yi = ampl*sin(2*( %pi)*f*t) + rand(nPoints)/2
y = [y yi]

y = y'

figure(1);
clf;
plot(y)

 # write csv
 #header = ['EEG1','EEG2','EEG3']

tableOut = [y y y]
pathSave = '/Users/pannawis/Projects/05_OpenBCI_Relax/DetectingRelaxedSection_SW/sin_simulate.csv'
csvWrite(tableOut,pathSave)




 
