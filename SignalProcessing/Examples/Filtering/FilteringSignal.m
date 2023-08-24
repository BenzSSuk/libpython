clear all;
# ----- Start App -----
##[filename, folderFile, fltidx] = uigetfile()

# select file 
folderProj = '/Users/pannawis/Projects/Git/SignalProcessing';
filename = 'test-tag-40cm.csv';
folderFile = fullfile(folderProj,'Rawsignal','DistanceTag');

pathFile = fullfile(folderFile,filename);
rawFile = csvread(pathFile);
y_raw = rawFile(:,1);

# load coeffient
nameCoeff = 'lp_hm_5Hz_49.mat';
##nameCoeff = 'bp_hm_0f05-40Hz_301.mat';
folderCoeff = fullfile(folderProj,'FilterCoefficient');
pathCoeff = fullfile(folderCoeff,nameCoeff);
##load 'pathCoeff'
structLoad = load(pathCoeff);
filterCoef = structLoad.filterCoef;

# filtering 
# lowpass
y_filtered = filter(filterCoef,1,y_raw);

# moving avg


# plot 
# Length of signal
fs = 125;
Ts = 1/fs;
intervalPlot = [0,3]; % seconds range
N = length(y_raw);
tsig = N*Ts;
t = 0:Ts:tsig-Ts;

% index interval 
indexInterval = (t >= intervalPlot(1) & t <= intervalPlot(2));
tinterval = t(indexInterval);

figure(1);
clf;
subplot(2,1,1)
plot(tinterval,y_raw(indexInterval),'-b');
title('raw signal');
xlabel('seconds');

subplot(2,1,2);
plot(tinterval,y_filtered(indexInterval));
title('filtered signal');
xlabel('seconds');
### use for visualize low sampling signal 
##N_raw = size(y_raw,1);
##indexDown = 1:timesDown:N_raw;
##t_down = tinterval(indexDown);
##y_raw_down = y_raw(indexDown);
##plot(t_down,y_raw_down,'-or');
##title('Down sampling to 128 Hz');
