#!/bin/bash
#This script reads from the subject txt file used in fsl's melodic
#to re-arrange individual data drom Dual R and Hurst calculations


#Insert path where data are stored
rootpath=$HOME/Documents/ABIDE_1/MRC_AIMS/rsfMRI/raw_data/MELODIC/ALLmales-NOTMASK
#Datafile, epi txt file
Datafile=$rootpath/ALLmales-NOTMASK.txt
#Dual regression - hurst directory 
DRH_dir=$rootpath/Dual_r/HURST_stuff

#Hurst links txt path
Hlinks=$DRH_dir/hurstlinks.txt

#Get N of subjects
SubjN=$(wc -l < ${Datafile})

#Starts from zero!!
#expr performs numeric calculation in bash
#ISubjN=$(expr $SubjN - 1)



#Make a txt file with all H directories
cd $DRH_dir
for dir in *stage*
do
	echo $(readlink -f $dir)
	echo $(readlink -f $dir) >> hurstlinks.txt
done

cd rootpath


#Loop ISubjN times
for i in $(seq 1 $SubjN)
do
	echo ${i}


	#Index the list of the EPI paths
	#sed -n #linenum indexes txt files by line num
	TmpEPIpath=$(sed -n ${i}p $Datafile)

	#We want to manipulate this line and get the path up
	#to preproc_2!

	#This deletes whatever(*), is last (%) after /	
	#if TmpEPIpath#*/ it would delete first instance (#) of whatever is before (*) /

	echo ${TmpEPIpath%/*}
	Tmppreproc=$(echo ${TmpEPIpath%/*})


	#takes the ith Hlink to H directory created before
	tmpHlink=$(sed -n ${i}p $Hlinks)
	echo $tmpHlink

	#moves it
	mv $tmpHlink $Tmppreproc/CSV

done


