#!/bin/bash
#
#This script strips the HCP into its different parcels
#and puts it into the sites dir.

#Uses each parcel to calculate LFF metrics with 3dRSFC
#on each individual EPI.
#
#Parcelwise LFF means are save into a csv for a every subject 

#For MRC AIMS. Heavily depends on AFNI programs.

#Stavros Trakoshis
#11/10/2018

#3dRSFC output prefix(es)
lff=LFF+tlrc.BRIK
alff=ALFF+tlrc.BRIK
falff=fALFF+tlrc.BRIK
malff=mALFF+tlrc.BRIK
rsfa=RSFA+tlrc.BRIK
frsfa=fRSFA+tlrc.BRIK
mrsfa=mRSFA+tlrc.BRIK

#EPI data
#I recommend using the LG_3DR*
restpp=LG_3DR_Erest_pp.nii.gz

#insert subs
subjlist="12005 12006 " #12004 12005 12006 12007 12008 12009 12010 12011 12012 12013 12014 12015 12016 12017 12018 12021 12022 12023 12025 12026 12027 12028 12029 12030 12031 12032 12034 12036 12037 12038 12040 22001 22002 22005 22006 22007 22009 22012 22013 22015 22017 22019 22021 22022 22023 22025 22026 22027 22030 22031 22034 22035 22037 22038 22039 22040 22041 22043 22044 22045 22046 22047 22049 22050 32001 32002 32003 32004 32005 32007 32008 32009 32010 32012 32013 32014 32015 32016 32017 32018 32020 32021 32022 32023 32024 32025 32026 32027 32028 32029 32030 32031 32032 32034 32035 32036 32037 32038 42001 42002 42003 42004 42005 42006 42007 42008 42009 42011 42013 42014 42015 42016 42017 42020 42021 42022 42024 42025 42026 42027 42028 42029 42030 42031 42033 42034 42035 42036 42037 42039 42040"

#N parcels
parcels=180

#insert paths
rootpath=~/Documents/ABIDE_1/MRC_AIMS/rsfMRI/raw_data
temppath=~/rsfmri/Templates/GlasserHCP/
tempfile=/home/stavros/rsfmri/Templates/GlasserHCP/MMP_in_MNI_symmetrical_1.nii.gz

parcelsout=$rootpath/HCP_parcels

#lets make this the wd
cd $temppath

#check if parcels are there.
echo "**+ Checking if parcels dir was made and proceeding +** "


#if it doesn't exist then make it
#otherwise print contents and continue
if [ ! -d $parcelsout ]
	then
	echo "**+ Making parcel dir and parcels from tamplate +**"


	mkdir $parcelsout
	#parcel loop
	for parc in $(seq 1 $parcels)
	do

		echo "**+ Working on Parcel $parc +**"


		#we are masking the mask with itself
		#where the mask is equal to parc, output it with the respective name
		#double quotes after the expr allow shell variables in expression
		#equals is a built in expression


		3dcalc -a "$tempfile" -expr "equals(a,$parc)" -prefix Parcel_${parc}.nii.gz
		
		mv Parcel_* $parcelsout
		
		ls $parcelsout/Parcel_* | wc -l


	done #parcel loop
else
	echo "**+ Parcel's in this site exists. Listing parcels and continue +**"
	ls  $parcelsout

fi
cd $parcelsout

#LFF loop
echo "**+ Processing of each subj begings +**"

for sub in $subjlist
do
	echo "**+Starting subject $sub"

	#subjpaths
	subpath=$rootpath/$sub
	preprocpath=$subpath/preproc_2
	restppfname=$preprocpath/$restpp


	#outdirs and file
	LFFout=$preprocpath/LFF
	mkdir $LFFout
	
	
	echo "**+ Starting reasmpling parcels to EPI"

	#parcel loop
	for tp in Parcel*
	do

		#resample template parc to LG
		3dresample -master $restppfname -input $tp -prefix TmP_$tp
		
		#after -F sets the field seperator to - or .
		#takes second instance $2
		#returns integer of parcel basically
		#do many dirs
		tmpnum=$(echo TmP_$tp | awk -F'[_.]' '{print $3}')
		
		
		mv TmP_$tp $LFFout


	done #parcel loop
	
	echo "**+ Resampling Finished"

	echo "**+ Starting the calculation of LFFs metrics with AFNI"
	
	cd $LFFout
	
	#get n of parcel files in LFF dir
	Nparc=$(ls | wc -l)

	#output file in LFF dir
	outuptfile=${sub}_LFF.csv

	#col names (or 1st row)
	printf '%s\n' "Parcel num" "LFF" "ALFF" "fALFF" "mALFF" "RSFA" "fRSFA" "mRSFA" | paste -sd ',' > $outuptfile
	
	#loop over all parcel LFF .BRIK
	for i in $(seq 1 $Nparc)
	do
		pwd

		#Call AFNI
		3dRSFC -prefix TmP_Parcel_$i -nodetrend -mask TmP_Parcel_$i.nii.gz 0 99999 $restppfname


		#from .BRIK to .csv
		#voxel wise
		#3dmaskdump -o ALFF_parcel${i}.csv -mask TmP_Parcel_${i}.nii.gz RSFC_ALFF+tlrc.BRIK


		#outputs ONE number and we sent it to csv
		lffval=$(3dBrickStat -mean -nonan TmP_Parcel_${i}_$lff)
		alffval=$(3dBrickStat -mean -nonan TmP_Parcel_${i}_$alff)
		falffval=$(3dBrickStat -mean -nonan TmP_Parcel_${i}_$falff)
		malffval=$(3dBrickStat -mean -nonan TmP_Parcel_${i}_$malff)
		rsfaval=$(3dBrickStat -mean -nonan TmP_Parcel_${i}_$rsfa)
		frsfaval=$(3dBrickStat -mean -nonan TmP_Parcel_${i}_$frsfa)
		mrsfaval=$(3dBrickStat -mean -nonan TmP_Parcel_${i}_$mrsfa)
		
		#sents it to outputfile
		printf '%s\n' Parcel_$i $lffval $alffval $falffval $malffval $rsfaval $frsfaval $mrsfaval | paste -sd ',' >> $outuptfile	
	done
	
	pwd
	
	cp $outuptfile $preprocpath/CSV
	
	echo "**+ Subject $sub is done"
	
	cd $rootpath

	pwd

done #LFF loop