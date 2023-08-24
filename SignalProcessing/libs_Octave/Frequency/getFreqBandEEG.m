function [freqBandEEG] = getFreqBandEEG()
    countRange = 1;
    freqBandEEG(countRange).name = 'delta';
    freqBandEEG(countRange).range = [0.5, 4];
    countRange = countRange + 1;
    freqBandEEG(countRange).name = 'theta';
    freqBandEEG(countRange).range = [4, 7];
    countRange = countRange + 1;
    freqBandEEG(countRange).name = 'alpha';
    freqBandEEG(countRange).range = [8, 12];
    countRange = countRange + 1;
    freqBandEEG(countRange).name = 'sigma';
    freqBandEEG(countRange).range = [12, 14];
    countRange = countRange + 1;
    freqBandEEG(countRange).name = 'beta';
    freqBandEEG(countRange).range = [14, 20];

endfunction