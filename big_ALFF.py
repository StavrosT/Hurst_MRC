#!/bin/bash/env python

#make a big ALFF csv 


#libraries

import pandas as pd
import numpy as np 
from os.path import join
import os

#path to LFF.csv data
datapath='/home/stavros/Documents/MRC_LFF/ALFF'

#output path
output_path = '/home/stavros/Documents/MRC_LFF/ALFF/ALL'

#output dir
os.mkdir(output_path)

#outname
output_name = 'ALL_ALFF.csv'

#path to tidy data
td_path = '/home/stavros/Documents/ABIDE_1/MRC_AIMS/tidy_data.xlsx'

td_data = pd.read_excel(td_path)


#parcel num
parcenum = 180



#get subjlist
sublist = list([12002, 12004, 12005, 12007, 12008, 12010, 12012, 12013, 12014, 12015, 12016, 12017, 12018, 12021, 12022, 12023, 12025, 12026, 12027, 12028, 12029, 12030, 12031, 12032, 12034, 12036, 12037, 12038, 12040, 22001, 22002, 22005, 22006, 22007, 22009, 22012, 22013, 22015, 22017, 22019, 22021, 22022, 22023, 22025, 22026, 22027, 22030, 22031, 22034, 22035, 22037, 22038, 22039, 22040, 22041, 22043, 22044, 22045, 22046, 22047, 22049, 22050, 32001, 32002, 32003, 32004, 32005, 32007, 32008, 32009, 32010, 32012, 32013, 32014, 32015, 32016, 32017, 32018, 32020, 32021, 32022, 32023, 32024, 32025, 32026, 32027, 32028, 32029, 32030, 32031, 32032, 32034, 32035, 32036, 32037, 32038, 42001, 42002, 42003, 42004, 42005, 42006, 42007, 42008, 42009, 42011, 42013, 42014, 42015, 42016, 42017, 42020, 42021, 42022, 42024, 42025, 42026, 42027, 42028, 42029, 42030, 42031, 42033, 42034, 42035, 42036, 42037, 42039, 42040])



#empty output df
output = pd.DataFrame(np.zeros((len(sublist), parcenum)))

output.index = sublist

#make col names

colnames = []

#an array of 1 - 180
colnumlist = np.arange(1, parcenum+1)

for g in colnumlist:
	print(g)
	colnames.append('Parcel_%s' % g) 



#name columns of output 

output.columns = colnames


#read in csvs
#into output
for sub in sublist:
	tmp_csv_file = '%s__ALFF.csv' % sub
	tmp_csv_path = join(datapath, tmp_csv_file)
	tmp_df = pd.read_csv(tmp_csv_path, header=0)
	tmp_Series = pd.Series(tmp_df.iloc[0])
	tmp_Series.drop(labels='Unnamed: 0', inplace=True)
	output.loc[sub] = tmp_Series


output.to_csv(join(output_path, output_name))