function [areaBand] = areaFreqBand(yFFT,f,f1,f2)
    
    indexBand = ( f >= f1 & f < f2 );
    
    if any(indexBand) 
%        disp('Found range')
        yFFT_band = yFFT(indexBand);
        x_band = 1:length(yFFT_band);
        areaBand = trapz(x_band, yFFT_band);
    else
%        disp('Not found range')
        areaBand = 0;
    end
    
endfunction