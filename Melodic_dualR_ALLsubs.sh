#!/bin/bash
#
#This script runs the fsl functions melodic and dual_regression
#

#Insert rootpath
rootpath=~/Documents/ABIDE_1/MRC_AIMS/rsfMRI/raw_data
#Insert Subject list where EPI will be read from
#subjects that have bad reg in latest tidy_data were removed
#22/10/2018
subjlist="12002 12004 12005 12006 12007 12008 12009 12010 12011 \
       12012 12013 12014 12015 12016 12017 12018 12022 12023 \
       12025 12027 12028 12029 12030 12031 12034 12036 12037 \
       12038 12040 22001 22002 22005 22006 22009 22012 22013 \
       22017 22019 22023 22026 22027 22030 22031 22034 \
       22039 22040 22044 22045 22046 22047 22049 22050 32001 \
       32002 32003 32004 32007 32008 32009 32010 32012 32013 \
       32014 32015 32017 32018 32020 32021 32022 32023 \
       32024 32025 32026 32027 32028 32029 32030 32031 32032 \
       32034 32035 32036 32038 42001 42002 42004 42005 \
       42006 42007 42009 42011 42013 42015 42016 42020 \
       42021 42022 42024 42025 42028 42031 42033 42034 42037 \
       42039 42040 42029"

#Insert name of group to process and make dir for it
Group_name="ALLsubjects"

# OVERALL Destination path
destpath=$rootpath/MELODIC
mkdir $destpath

# Group destination path
G_dest=$destpath/${Group_name}
mkdir $G_dest

#Insert preprocessed EPI of interest for Melodic list
EPI="LG_3DR_Erest_pp.nii.gz"

cd $rootpath

for subid in $subjlist
do
	subpath=$rootpath/$subid
	preprocpath=$subpath/preproc_2
	cd $preprocpath
	echo "I am in ${subid}"

	#for macs is greadlink -f after brew install coreutils
	#reads file link and sends it to a list
	readlink -f $EPI
	echo $(readlink -f $EPI) >> ${destpath}/${Group_name}.txt
	cd $rootpath
done #for

#Go to Destpath
cd $destpath

#change groupname.txt to .filelist
#cp ${Group_name}.txt ${Group_name}.filelist


# Format melodic args
INPUT=${Group_name}.txt
TR="1.302"
DIMS="30"
BGIMG=$rootpath/MNIs/LG_3DR_MNI152_T1_2mm_brain.nii.gz
ARGS="--dim=$DIMS --nobet --tr=$TR --bgimage=$BGIMG --Oall --report -v  -a concat --mmthresh=0.5"

# Call melodic
melodic -i ${Group_name}.txt -o $G_dest $ARGS
#**************
#Consider running AROMA in MELODIC output
#*********

cp ${Group_name}.txt $G_dest

#cd to group destination path
cd $G_dest

#dual_regressions args can be entered here but in my UBUNTU versions it works only hard coded
#ADD arguments such as 1=variance normalized -1=One sample t-test 100=permutations



# Running Dual Regression in Group ICA
echo "Dual Regression about to Start"
# run dual_regression 

dual_regression melodic_IC.nii.gz 1 -1 10 Dual_r `cat ${Group_name}.txt`

#echo done 10 times
printf "**  DONE - DONE - DONE **\n%.0s" {1..10}
