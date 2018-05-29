%ombining parellate.m and bfn_mfin_ml.m in MR subjets
%Assuming 3dresample with rest as -master was run and result was saved in a
%HURSTS dir, in subjets repo as {'subjetsID_MMP_in_MNI_symmetrial_1.nii.gz'}
%and its the only one in the dir

%Paths
rootpath = '/Users/stavrostrakoshis/Documents/MRC_AIMS/rsfMRI/raw_data/TEST';

%atlasfile = '/Users/stavrostrakoshis/rsfmri/Templates/GlasserHP/MMP_in_MNI_symmetrial_1.nii.gz';

%Parellate args
MEANCENTER = 1;

%Non-fractal-master/m/bfn_mfin_ml.m args
lb = [-0.5,0];
ub = [1.5,10];

%Get subdir list - every subjets has a 0 in their id
d = dir(fullfile(rootpath, '*0*'));

%Loop

for i=1:length(d)
    subname = d(i).name;
    subpath = fullfile(rootpath, subname);
    disp(subpath);
    
    %parcellate args
    atlasfile = fullfile(subpath,'HURSTS','Erest_TEMP.nii.gz');
    datafile = fullfile(subpath, 'preproc_2', 'Erest_pp.nii.gz');
    fname2save = strcat(subname,'_MMP_in_MNI_symmetrical_1.csv');
    
    
    %calls parcellate.m
    result = parcellate(atlasfile,datafile,fname2save,MEANCENTER);
    
   
   %import csv make it an array
    table = readtable(fname2save);
    disp(size(table));
    ArrayTable = table2array(table);

    % Identify if there are any regions that the atlas is not covering  
   
    colswnan = find(sum(isnan(ArrayTable),1)~=0);

   
    %feed array into bfn_mfin_ml.m
    [H, nfcor, fcor] = bfn_mfin_ml(ArrayTable, 'filter', 'Haar', 'lb', lb, 'ub', ub);

    % there are any columns with NAN replace them in ArrayTable with NAN
	if !isempty(colswnan)
		H(colswnan) = NaN;
	end   

    %write everything into csv for each subject
    H_name = strcat(subname, '_H.csv');
    fcor_name = strcat(subname, '_fcor.csv');
    nfcor_name = strcat(subname, '_nfcor.csv');
    
   
    csvwrite(H_name, H);
    csvwrite(fcor_name, fcor);
    csvwrite(nfcor_name, nfcor);
    
   
    clear H fcor nfcor datafile atlasfile fname2save H_name fcor_name nfcor_name att 
   
end