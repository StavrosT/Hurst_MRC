#!/bin/bash
#This script reads from the subject txt file used in fsl's melodic
#to re-arrange individual data drom Dual R only. not hurst.
#
#Revised: 23/10/2018
#Stavros Trakoshis

#Insert path where data are stored
rootpath=$HOME/Documents/ABIDE_1/MRC_AIMS/rsfMRI/raw_data/MELODIC/ALLsubjects
#Datafile, epi txt file
Datafile=$rootpath/ALLsubjects.txt
#Dual regression
DRH_dir=$rootpath/Dual_r

#DR links txt path
#DRlinks=$DRH_dir/DRlinks.txt

#Drlinks fname
DRlinks_stage1=DRlinks_stage1.txt
DRlinks_stage2=DRlinks_stage2.txt



#Get N of subjects
#Reads lines in a  txt
SubjN=$(wc -l < ${Datafile})



#Specify wd
cd $DRH_dir


#Make a txt file with all Dr links of stage 1
for dir in *stage1*
do
	echo $(readlink -f $dir)
	echo $(readlink -f $dir) >> $DRlinks_stage1
done

#Make a txt file with all Dr links of stage 2
#not the Z-standardized images
#I dont want those.
for dir in *stage2*[0-9].nii.gz
do
	echo $(readlink -f $dir)
	echo $(readlink -f $dir) >> $DRlinks_stage2
done




#Loop ISubjN times
for i in $(seq 1 $SubjN)
do
	echo ${i}


	#Index the list of the EPI paths
	#sed -n #linenum indexes txt files by line num
	TmpEPIpath=$(sed -n ${i}p $Datafile)

	#We want to manipulate this line and get the path up
	#to preproc_2!
	#
	#This deletes whatever(*), is last (%) after /	
	#if TmpEPIpath#*/ it would delete first instance (#) of whatever is before (*) /
	#
	#!whats left is the path to preproc_2!
	#
	echo ${TmpEPIpath%/*}
	Tmppreproc=$(echo ${TmpEPIpath%/*})

	#General ICA dir
	ICA_ALL_subs=$Tmppreproc/ICA_ALL_subs
	mkdir $ICA_ALL_subs

	#Stage specific dirs
	S1=$ICA_ALL_subs/stage_1_out
	mkdir $S1
	S2=$ICA_ALL_subs/stage_2_out
	mkdir $S2



	#
	#Stage 1 process

	#takes the ith DRlink of stage1 link files
	tmpDRlink=$(sed -n ${i}p $DRlinks_stage1)
	echo $tmpDRlink

	#moves it
	cp $tmpDRlink $S1
	ls $S1


	#Stage 2 process

	#takes the ith DRlink of stage2 link files
	tmpDRlink=$(sed -n ${i}p $DRlinks_stage2)
	echo $tmpDRlink

	#moves it
	cp $tmpDRlink $S2
	ls $S2





done


