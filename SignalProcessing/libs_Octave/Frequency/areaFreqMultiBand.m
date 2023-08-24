function [areaMultiBand] = areaFreqMultiBand(yFFT,f,freqBand)
    nBands = length(freqBand);
    areaMultiBand = zeros(1,nBands);
    
    for iband = 1:nBands
        f1 = freqBand(iband).range(1);
        f2 = freqBand(iband).range(2);
        areaMultiBand(iband) = areaFreqBand(yFFT,f,f1,f2);
    end
    
endfunction