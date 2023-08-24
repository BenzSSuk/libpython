function [yFFT_abs,f] = getFFT(y,fs)
    yFFT = fft(y);
    N = size(y,'*');
    //s is real so the fft response is conjugate symmetric and we retain only the first N/2 points
    f = ( (fs/N)*(0:(N/2)) ); //associated frequency vector
    n = size(f,'*'); // product of dimensions
    yFFT_abs = abs(yFFT(1:n));
    
endfunction

function [areaBand] = areaFreqBand(yFFT,f,f1,f2)
    
    indexBand = ( f >= f1 & f < f2 );
    
    if or(indexBand) 
//        disp('Found range')
        yFFT_band = yFFT(indexBand);
        x_band = 1:size(yFFT_band,'*');
        areaBand = inttrap(x_band, yFFT_band);
    else
//        disp('Not found range')
        areaBand = 0;
    end
    
endfunction

function [areaMultiBand] = areaFreqMultiBand(yFFT,f,freqBand)
    nBands = length(freqBand);
    areaMultiBand = zeros(1,nBands);
    
    for iband = 1:nBands
        f1 = freqBand(iband).range(1);
        f2 = freqBand(iband).range(2);
        areaMultiBand(iband) = areaFreqBand(yFFT,f,f1,f2);
    end
    
endfunction

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

function [areaMultiBand] = areaFreqEEG(yFFT,f)
    freqBandEEG = getFreqBandEEG()
    
    [areaMultiBand] = areaFreqMultiBand(yFFT,f,freqBandEEG)
    
endfunction
