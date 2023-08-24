%{
  Requirement package, run at the command window tab of Octave GUI respectively.
    > pkg install -forge control
    > pkg install -forge signal
%}
close all;
clear all;
##clf;

pkg load signal;

##folderProj = '/Users/pannawis/Projects/Git/SignalProcessing';
folderProj = pwd

# export to .mat and .txt

folderSave = 'FilterCoefficient';
Fs = 75; # sampling rate
N = 300; # no. of coefficient

%filterType = 'high';
filterType = 'bandpass';


if strcmp(filterType,'low')
  # Low pass
  cutoff_1 = 5;
  f_band =  cutoff_1 / (Fs/2);
 
elseif strcmp(filterType,'high')
  cutoff_1 = 0.1;
  f_band =  cutoff_1 / (Fs/2);
 
elseif strcmp(filterType,'bandpass')
  # band pass
  cutoff_1 = 0.1;
  cutoff_2 = 10;
  f_band = [cutoff_1 cutoff_2] / (Fs/2);
  
endif

%nameCoeff = 'hp_hm_0f1Hz_100Hz_501';
nameCoeff = 'bp_hm_0f1_10Hz_75Hz_301';

%{ 
  b = fir1 (n, w, type, window, noscale)
  Produce an order n FIR filter
  Input:
    n: order of FIT filter
    w: Normalized frequency (*pi rad/sample)
      0 - fs/2
      fs/2 >> 1
      fcutoff >> fcutoff/(fs/2)
    type: 'low'(default), 'high', 'stop', 'pass', 'bandpass'
    window: hamming(default)
    
  Output:
    b: filter coefficient size = n+1
%}
##N = dB*Fs/(22*delta_f);
filterCoef = fir1(N, f_band, filterType);

# export variable 
nameSave = [nameCoeff '.mat'];
pathSave = fullfile(folderProj,folderSave,nameSave);
save(pathSave, 'filterCoef',"-v7");

nameSave = [nameCoeff '.txt'];
pathSave = fullfile(folderProj,folderSave,nameSave);
save(pathSave, 'filterCoef');

figure(1);
freqz(filterCoef)
##plot((-0.5:1/4096:0.5-1/4096)*Fs,20*log10(abs(fftshift(fft(hc,4096)))));
##axis([0 50 -60 20]);
##title('Filter Frequency Response');
##grid on;

# ----- Generate signal -----
##f1 = 10000;
##f2 = 15000;
##delta_f = f2-f1;
##dB  = 40;

##x = sin(2*pi*[1:1000]*5000/Fs) +  sin(2*pi*[1:1000]*2000/Fs) + sin(2*pi*[1:1000]*13000/Fs)  + sin(2*pi*[1:1000]*18000/Fs);
##
##sig = 20*log10(abs(fftshift(fft(x,4096))));
##xf = filter(hc,1,x);
##
##figure;
##subplot(211);
##plot(x);
##title('Sinusoid with frequency components 2000, 5000, 13000, and 18000 Hz');
##
##
##subplot(212);
##plot(xf);
##title('Filtered Signal');
##xlabel('time');
##ylabel('amplitude');
##
##
##x= (x/sum(x))/20;
##sig = 20*log10(abs(fftshift(fft(x,4096))));
##xf = filter(hc,1,x);
##
##figure;
##subplot(211);
##plot((-0.5:1/4096:0.5-1/4096)*Fs,sig);
##hold on;
##plot((-0.5:1/4096:0.5-1/4096)*Fs,20*log10(abs(fftshift(fft(hc,4096)))),'color','r');
##hold off;
##axis([0 20000 -60 10]);
##title('Input to filter - 4 Sinusoids');
##grid on;
##subplot(212);
##plot((-0.5:1/4096:0.5-1/4096)*Fs,20*log10(abs(fftshift(fft(xf,4096)))));
##axis([0 20000 -60 10]);
##title('Output from filter');
##xlabel('Hz');
##ylabel('dB');
##grid on;