#!/bin/bash/env python
#takes fALFF values from csv files created by LFF.sh

#Stavros Trakshis
#15/10/2018


#import libraris
import pandas as pd 
import numpy as np 
from os.path import join
import os


#cd into rootpath
rootpath = "/home/stavros/Documents/MRC_LFF"
os.chdir(rootpath)

#output dirs
outdir = join(rootpath, 'fALFF')
os.mkdir(outdir)

#output extension 
falff = "__fALFF.csv"

#reads files in a dir
filelist = os.listdir(rootpath)




for file in filelist:
	#does what is says!
	if file.endswith(".csv"):

		print(file)
		tmp_df = pd.read_csv(file)
		tmp_df.index
		#take parcel names!
		parcel_names = tmp_df['Parcel num']
		#needs to be a df instead of a series for transpose to works
		tmp_fALFF = pd.DataFrame(tmp_df['fALFF'])
		T_tmp_fALFF = tmp_fALFF.T

		#name cols
		T_tmp_fALFF.columns = parcel_names


		#lets take subname
		#sebarate file by separator
		#returns a list with 2 elemnts before 
		#and after separator
		filenm_lst = file.split("__")
		subname = filenm_lst[0]

		#catenate strings
		fullfile = subname + falff
		
		#back to writing output to csv
		T_tmp_fALFF.to_csv(join(outdir, fullfile))
