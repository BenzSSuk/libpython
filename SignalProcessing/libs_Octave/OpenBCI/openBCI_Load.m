function [structRaw,header] = openBCI_Load(filename)
  f = fopen(filename, 'r');

  cellHeader = textscan(f,'%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s',1,"HeaderLines",4,'delimiter',',');  
  header = cellstr(cellHeader);

  cellRawRead = textscan(f,'%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%s%f%s',"HeaderLines",5,'delimiter',',');  
  matRaw = cell2mat(cellRawRead(:,1:20));
  
  % Create struct, used as table 
  nCols = size(matRaw,2);
  for i = 1:nCols
    structRaw.(header{i}) = matRaw(:,i);
  endfor
  
endfunction