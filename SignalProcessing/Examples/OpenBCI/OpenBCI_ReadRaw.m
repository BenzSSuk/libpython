clear all;

folderProj = '/Users/pannawis/Projects/05_OpenBCI_Relax/DetectingRelaxedSection_SW'
filename = fullfile(folderProj,'rawdata','OpenBCI_Relax_Tem.txt');

# dir of folderpath
folderScript = fileparts(mfilename('fullpath'));

addpath(folderScript);

disp("Loading .txt");
[structRaw,header] = openBCI_Load(filename);

