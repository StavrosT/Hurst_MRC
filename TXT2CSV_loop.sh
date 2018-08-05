#!/bin/bash
#Calls txt2csv.py on the output of FSL's MELODIC - Dual R txt files


#Define where txt data are
rootpath=~/Documents/MELODIC_ALLmales/
#Define Dual R path
dualRpath=$rootpath/Dual_r
#Define code path
codepath=$rootpath/Code

#Define output dir
csvpath=$rootpath/CSVS
mkdir $csvpath


cd $dualRpath
pwd
#Grab whatever ends with .txt 
txtlist=$(printf '%s\n' *.txt)

for txtfile in $txtlist
do
	#Call txt2csv needs 2 args
	python3 $codepath/txt2csv.py $dualRpath $txtfile
	
	#Tell us how many csv in wordking dir
	ls *.csv | wc -l

done

mv *.csv $csvpath
ls $csvpath


#if everything is ok
if [ $? == 0 ]
	then
	#echo done 10 times
	printf "**  DONE - DONE - DONE **\n%.0s" {1..10}
else
	echo "**ERROR** There was an error somewhere! maybe not python3?? Maybe weird encoding of txtfile?? Dunno **ERROR** "
fi

