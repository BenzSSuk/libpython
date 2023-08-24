function [yFFT_abs,f] = getFFT(y,fs)
    yFFT = fft(y);
    N = length(y);
    %s is real so the fft response is conjugate symmetric and we retain only the first N/2 points
    f = ( (fs/N)*(0:(N/2)) ); %associated frequency vector
    n = length(f); % product of dimensions
    yFFT_abs = abs(yFFT(1:n));
    
endfunction