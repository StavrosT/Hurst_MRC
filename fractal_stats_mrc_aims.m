
rootpath = '/Users/stavrostrakoshis/Documents/MATLAB';

% grab all subjects with *H.csv

d = dir(fullfile(rootpath,'*H.csv'));
nregions = 180;

% pre-allocate empty matrix of zeros to store data in within the loop
% [subjects x regions]
Hdata = zeros(length(d),nregions);

for i = 1:length(d)
    % read in *H.csv
    fname = fullfile(rootpath,d(i).name);
    H = readtable(fname);
    Hdata(i,:) = table2array(H);
end


%% hypothesis tests
group = [zeros(5,1); ones(5,1)];
group1 = Hdata(group==0,:);
group2 = Hdata(group==1,:);

[H,P,CI,STATS] = ttest2(group1, group2);


