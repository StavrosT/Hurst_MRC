#!/bin/bash/env python3

import os
import sys


def TEXT2CSV(filepath, txtfile):
	#cd into path
	os.chdir(filepath)
	#split fileinto before (& after) extension - thats why the dot
	SplFile = txtfile.split(".") #dod disappears -- list with two elements

	#New File
	NF = open(txtfile, "r") # read access

	#Loop
	
	ListInput = []
	for obj in NF:
		#This change the seperation tof values from line (\n) to tab (\t)
		#by makind the encoding to tab it automatically makes a list
		#for every row/line - its row now (.split by \t!), it used to be line i.e .txt
		#Keeps values but changes encoding basically
		Listrow = obj.replace("\n", "").split("\t") 
		#Feel the array
		ListInput.append(Listrow)


	NF.close()
	#Makes a new csv with the subject name (which is now in a list!) and a csv extension
	NF_writable = open(SplFile[0] + ".csv", "+w", encoding='UTF+8')


	#Loop
	#Take stuff and fill the csv for the list of lists (ListInput)

	for lst in ListInput:

		#join each list with a comma!
		#comma seperateion means R to L joining for each list of course
		Writerow = ",".join(lst) #str again
		NF_writable.write(Writerow + "\n")


TEXT2CSV(sys.argv[1], sys.argv[2]) #represents args separated by spaces

