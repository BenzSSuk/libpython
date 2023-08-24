pkg load signal

# ---- load voice -----
# ui get file
folderFile = 'C:\Users\Panna\OneDrive - The Siam Cement Public Company Limited\Projects\_Wearable';
filename = 'Test1234_help2.wav';
pathFile = fullfile(folderFile,filename); 
[y, fs] = audioread(pathFile);

# ----- loop of down sampling -----
listDown = [2,3,4,6,8,10,12,14,20,40,80,160];
for nDown = listDown
##  nDown = 2;
  fs_new = round(fs/nDown);
  filename_down = ['Test1234_' num2str(fs_new) 'Hz.wav'];
  y_down = downsample(y, nDown);
  audiowrite(filename_down, y_down, fs/nDown)
end

