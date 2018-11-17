#!bin/bash

#this scirpt masks the Hmaps with Glasser ROIs and computes mean

#depends on Afni

#15/11/2018
#ST
#####

#paths

#root
rootpath=~/Documents/ABIDE_1/MRC_AIMS/rsfMRI/raw_data

#parcel's dir path
parcelpath=$rootpath/HCP_parcels

#LG binary mask nifti to resample all parcels path
LG_BN=$rootpath/32037/preproc_2/3dAutomask_Erest_pp.nii.gz

#resample parcels
LG_parcs=$parcelpath/LG_BN_parcels
mkdir $LG_parcs

#final destination
outpath=$rootpath/Hmap_H_means
mkdir $outpath

#each sub csv name
out_csvs=Hmaps_means.csv

#Nifti to use
Hmap=DWT_BNLG_Erest_Hmap.nii

#LG binary mask nifti to resample all parcels path
LG_BN=$rootpath/32037/preproc_2/3dAutomask_Erest_pp.nii.gz

#make counter
Count=0

#get subjects
cd $rootpath
subjlist=$(printf '%s\n' [0-9]* | paste -sd " ")

#get parcels
cd $parcelpath
parcellist=$(printf '%s\n' Parcel_*[0-9]* | paste -sd " ")



#######

#parcel_loop
cd $LG_parcs

#parcel loop
for parc in $parcellist
do

	echo $parc
	tmp_p=$parcelpath/$parc
	#call AFNI
	3dresample -master $LG_BN -prefix BN_${parc}.nii.gz -input $tmp_p

done


echo "**++ Parcel's have been resampled to the LG binary mask"

echo "**++A list of the resampled ROIs is created"

#NEW parcel list :)
LG_parcellist=$(echo printf '%s\n' *[0-9]* | paste -sd " ")

#
cd $rootpath
pwd



#sub loop
for sub in $subjlist
do
	#subpaths
	preprocpath=$rootpath/$sub/preproc_2
	fname=$preprocpath/$Hmap
	csvpath=$preprocpath/CSV


	#180 times for each subject
	for bnparc in $LG_parcellist
	do

		parcelII=$LG_parcs/$bnparc

		tmp_mean=$(3dBrickStat -mean -slow -nonan -mask $parcelII $fname)

		printf '%s\n' $tmp_mean | paste -sd "," >> $out_csvs

		echo "$bnparc for $sub done"
	done

	#mv it to each subj CSV dir
	mv $out_csvs $csvpath
	ls $csvpath/$out_csvs
	pwd

	echo "**++ $sub done!"
done

echo "**++We'll move each csv to a general dir in sites dir"

for sub in $subjlist
do
	preprocpath=$rootpath/$sub/preproc_2
	csvpath=$preprocpath/CSV
	Hmeans_csv_path=$csvpath/$out_csvs

	cp $Hmeans_csv_path $outpath/${sub}_Hmap_means.csv

done