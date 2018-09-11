%%
%This script loops over the output of fsl Dual regression
%reads in the txt file for every subject and calculates the Hurst exponenet
%for every component across time points.
%%
% Enter rootpath for MELODIC
rootpath = '/home/stavros/Documents/ABIDE_1/MRC_AIMS/rsfMRI/raw_data/MELODIC'


%Specific file-gorup
Groot = fullfile(rootpath, 'ALLmales-NOTMASK', 'Dual_r');

%Text files in Groot
TGroot = dir(fullfile(Groot, '*.txt'));
%%

%Fix parameters for bfn_mfin_ml
lb = [-0.5,0];
ub = [1.5,10];
%%

%Loop to take the specific name of each file 
for i = 1:length(TGroot)
    
    %Subpaths
    display(i)
    Subtxt = TGroot(i).name;
    display(Subtxt)
    
    %load txt
    Data = load(fullfile(Groot, Subtxt));
    %Call H function
    [H, nfcor, fcor] = bfn_mfin_ml(Data, 'filter', 'Haar', 'lb', lb, 'ub', ub);
    
    
    %Write everything into csv for each subject
    H_name = strcat(Subtxt, '_H.csv');
    fcor_name = strcat(Subtxt, '_fcor.csv');
    nfcor_name = strcat(Subtxt, '_nfcor.csv');
    
    csvwrite(H_name, H);
    csvwrite(fcor_name, fcor);
    csvwrite(nfcor_name, nfcor);
    

    %Make a dir for each Subtxt nameSplit txt in subtxt
    %Split Subtxt name, delimiter is the .
    NameVar = strsplit(Subtxt, '.');
    Subname = NameVar(1);
    %from cell 2 mat and then to str!
    StrName = mat2str(cell2mat(Subname));
    
    
    mkdir(Groot, StrName);
    tmp_dpath = fullfile(Groot, StrName);
    %Move csvs to that subject 
    movefile('*.csv', tmp_dpath)
    
    
end
%%
