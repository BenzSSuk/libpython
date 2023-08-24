// Design filter coefficient

/*
ftype: 'lp', 'hp', 'bp', 'sb'
forder: no. coefficient
cfreq: cut off frequency 
     Low >> cfreq(1) = 3, 0 - 3 Hz
     High >> cfreq(1) = 5, 5 ++ Hz
wtype: 're', 'tr', 'hm', 'hn', 'kr', 'ch'
fpar: 
*/

//ftype = 'lp'
//forder = 51
//cfreq = 40
//wtype = 'hm'
//fpar = 0
//[wft,wfm,fr]=wfir(ftype,forder,cfreq,wtype,fpar)

fs = 125
cfreq = [0,0]

cutOffFreq = 0.05 // Hz
cfreq(1) = cutOffFreq / fs

cutOffFreq = 40 // Hz
cfreq(2) = cutOffFreq / fs


[filterCoef,hm,fr] = wfir("bp",101,cfreq,"hm",[0 0])

save('/Users/pannawis/Projects/05_OpenBCI_Relax/bp_hm_0f05-40Hz.dat',['filterCoef']);

//clear filterCoef
//load('/Users/pannawis/Projects/05_OpenBCI_Relax/lp_hm_40Hz.dat','filterCoef');

