% Copyright (C) 2016, 2016 Carlos R. Lacerda
%
% $Id: kalmanfilter.m 2016-04-04 12:09:23Z carlosrl $
%
% This software is distributed under the GNU General Public 
% Licence (version 2 or later); please refer to the file 
% Licence.txt, included with the software, for details.

% % subscribe to node
% if ismember('/camera/image_raw', rostopic('list'))
%     imsub = rossubscriber('/camera/image_raw');
% end
% fig = 'D:\IoT\Robot_Project\CAbot\fig\test';
% k = 0;
% tic;
% while toc < 60
%     img = receive(imsub);
%     I = readImage(img);
%     imshow(I);
%     imwrite(I, [fig,num2str(k),'.png']);
% end

path=[.1 .05; .13 .24; .18 .24; .23 .24; .28 .24; .28 .40; .28 .56; .33 .56; .33 .72; .33 .88; .33 1.04; .28 1.04; .23 1.04; .23 1.2;.20 1.4];
filename = 'D:\IoT\Robot_Project\bag\teste.dat';
filetxt = 'D:\IoT\Robot_Project\bag\out-2016-09-28-23-37-02.txt';
filecsv = 'D:\IoT\Robot_Project\bag\out-22-20-12.csv';

fid = fopen(filetxt);
res={};
while ~feof(fid)
  res{end+1,1} =fgetl(fid);
end
fclose(fid);
N=numel(res)

%m = csvread(filename);
%txt = textread(filetxt);
fileID = fopen(filetxt);
formatSpec = '%s';
%N=183;
%C_head = textscan(fileID, formatSpec, N, 'Delimiter', ',');
% now read data
%frewind(fileID);
formatSpec = '%.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f';
C_data = textscan(fileID, formatSpec, N, 'HeaderLines',0, 'Delimiter',',', 'CollectOutput', 0, ...
    'MultipleDelimsAsOne',0);
fclose(fileID);
%csv = csvread(filecsv);


plot(path(:,1), path(:,2),'k--d')
hold on
ylim([0 1.45])
xlim([0 .35])

for i = 1:N
    title([num2str(i) ', ' 'time: ' num2str(C_data{1,1}(i)) ', x: ' num2str(C_data{1,5}(i)) ...
        ', y: ' num2str(C_data{1,6}(i)) ', w: ' num2str(C_data{1,4}(i))])
    plot(C_data{1,5}(i), C_data{1,6}(i),'ro');
    pause(.5);
end

plot(.12,.2,'ro')
