function [areaMultiBand] = areaFreqEEG(yFFT,f)
    freqBandEEG = getFreqBandEEG()
    
    [areaMultiBand] = areaFreqMultiBand(yFFT,f,freqBandEEG)
    
endfunction