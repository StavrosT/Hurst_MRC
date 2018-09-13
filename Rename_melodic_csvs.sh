#!/bin/bash 
#This script changes the name of ICA_hurst files 
#that have been moved to the individual CSV dirs

#then the mv Hurst can be used with the added line of the
#melodic_dual regression directory (dr_stage) in that code


rootpath=~/Documents/ABIDE_1/MRC_AIMS/rsfMRI/raw_data

cd $rootpath

subjlist=$(echo $(printf '%s\n' *0*))

echo "These are the site subjects"
echo $subjlist

for g in $subjlist
do
	subpath=$rootpath/$g/preproc_2
	csvpath=$subpath/CSV


	cd $csvpath	
	echo $g
	ls dr*

	#filename into a variable
	dr_stage=$(printf '%s\n' dr_stage*)
	melodic="melodic"

	mv $dr_stage ${g}-${melodic}


	cd ${g}-${melodic}


	#old values
	Hurst_old=$(printf '%s\n' *_H.csv)
	fcor_old=$(printf '%s\n' *_fcor.csv)
	nfcor_old=$(printf '%s\n' *_nfcor.csv)

	#new values
	mv $Hurst_old ${g}_H.csv
	mv $fcor_old ${g}_fcor.csv
	mv $nfcor_old ${g}_nfcor.csv

	echo $g

	ls

	cd $rootpath
done