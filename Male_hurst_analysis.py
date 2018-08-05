#!/bin/bash/env python3
#for USM_Scans (UTAH)



#Import libraries 
import pandas as pd
from pandas import plotting #pandas plotting
import matplotlib.pyplot as plt #makes plots appear
import scipy 
import numpy as np
from os.path import join #Like matlabs fullfile
from statsmodels.formula.api import ols #For R like formulas 
from statsmodels.stats.multitest import fdrcorrection #FDR from statsmodels
from statsmodels.sandbox.stats.multicomp import multipletests #for bonferonni

#Paths
rootpath = "/Users/stavrostrakoshis/Documents/USM_Scans_Hurst"
codepath = join(rootpath, "Code")
datapath = join(rootpath, "data")
phenopath =join(rootpath, "pheno")

#Read in file
phenofile = join(phenopath, "Phenotypic_V1_0b.csv")

pheno_data = pd.read_csv(phenofile)

ardata = pd.DataFrame(pheno_data) #dataframe

#Subset UM1
USMpheno_data = pheno_data.loc[pheno_data['SITE_ID'] == 'USM']

#Get mean age of males
USMpheno_data[USMpheno_data['SEX'] == 1]['AGE_AT_SCAN'].mean() #13.17


#Remove columns that are full of NaNs
numrows = len(USMpheno_data.index)
USMpheno_data.dropna(axis=1, thresh=numrows, inplace=True) #20 cols remain


#Subset only males
pheno_data_males = USMpheno_data.loc[USMpheno_data['SEX'] == 1] #All males 101 rows


#Remove subjects we have no data for 



pheno_data_males.set_index('SUB_ID', inplace=True)

pheno_data_males.drop(index=50458, inplace=True)

pheno_data_males.drop(index=50487, inplace=True)

pheno_data_males.drop(index=50446, inplace=True)

pheno_data_males.drop(index=50432, inplace=True)




#Format SUB_ID to have leading zeros
#and use this further on to import H csvs


INDEX = pd.Series(pheno_data_males.index.get_values())
listINDEX = list(INDEX)
iternum = len(listINDEX)   
iterlist = list(np.arange(0, iternum))


for i in iterlist:
	print(listINDEX[i])
	strindexlist = str(listINDEX[i])
	J = strindexlist.zfill(7)
	listINDEX[i] = J #SUB_ID is now stored in str format
	print(listINDEX[i])




 #For this subject we have no data


#First col as row names used to be here but it messes up the indexing later!
#Good thing to remember that order matters

#Name rows correctly this time
pheno_data_males.set_index(pd.Series(listINDEX), inplace=True)

#

#Empty frame
colnum = 180
tmp_data = pd.DataFrame(np.zeros((len(listINDEX), colnum)))
tmp_data = tmp_data.set_index(pd.Series(listINDEX))  #names rows

#Specifies the number of itteration 

colnumlist = np.arange(1,colnum+1)

#Make an empty list 

colnames = []

#Loop for col names
for g in colnumlist:
 	colnames.append('Parcel_%s' % (g))

#Name empty matrix columns with colnames

tmp_data.columns = colnames


#Read in csvs for each subject

for isub in list(listINDEX):
	SubHurst = '%s__Hurst.csv' % (isub)
	subfname = join(datapath, SubHurst)
	data12 = pd.read_csv(subfname, header=None)
	tmp_data.loc[isub] = data12.values


'''''''''''
#Unlock to
#make a preliminary output for visual checking
PO = 'tmp_data.csv'
tmp_data_path = join(phenopath, PO)
tmp_data.to_csv(tmp_data_path)
'''''''''
 	
#Join them into a big frame

frames = [pheno_data_males, tmp_data]
extended_pheno_data_males = pd.concat(frames, axis=1) 

#Write it 

ExtPDM = 'extended_pheno_data_males.csv'
ExtPDMpath = join(phenopath, ExtPDM)
extended_pheno_data_males.to_csv(ExtPDMpath) 



#Mean (etc) of stuff
extended_pheno_data_males[extended_pheno_data_males['DX_GROUP'] == 	1]['FIQ'].mean()
extended_pheno_data_males[extended_pheno_data_males['DX_GROUP'] == 2][['FIQ', 'VIQ']].mean()



#Some FIQ values are wrong/lessthanzero find them 
lessthanzero = extended_pheno_data_males.loc[extended_pheno_data_males['FIQ'] <0]
ID_LTZ = lessthanzero.index.values
#Do we want replace them?
#
#
#
#
#extended_pheno_data_males.replace(to_replace=ID_LTZ, value=0, inplace=True) 


#Or
#for general descriptives
extended_pheno_data_males.describe()

#Groupby for better implementation
#cleaner aesthitics 
#groupby spits/is an object

ASD_TD_pheno_datamales = extended_pheno_data_males.groupby('DX_GROUP')
ASD_TD_mean = ASD_TD_pheno_datamales.mean()
ASD_TD_max = ASD_TD_pheno_datamales.max()


'''
#Plot some of them (?)
plotting.scatter_matrix(extended_pheno_data_males[['FIQ', 'Parcel_64','Parcel_148']])
plt.show() #shows
plt.close() #terminates figure?
plotting.scatter_matrix(extended_pheno_data_males[['FIQ', 'Parcel_1','Parcel_2', 'Parcel_3', 'Parcel_4', 'Parcel_5', 'Parcel_6', 'Parcel_7', 'Parcel_8', 'Parcel_9', 'Parcel_10', 'Parcel_11', 'Parcel_12', 'Parcel_13', 'Parcel_14', 'Parcel_15']])
plt.show()  #looking for bimodal plots as if there are 2 populations
'''
#STATS

output_res = pd.DataFrame(np.zeros(shape=(colnum, 2))) #empty df to write results
output_res = pd.DataFrame(output_res) #make sure! 



parcel_names = []
for col in colnumlist:
	parcel_names.append('Parcel_%s' % col)

output_res.insert(loc=0, column='Parcel_num', value=parcel_names) #parcel_names as first col

output_res.set_index('Parcel_num', inplace=True) #name rows from 1st col / inplace


output_res.columns = ['T-test', 'p_value']  #names cols

#Takes the value of H in each parcel for each subject in every group
#Performs independent t-test from scipy
for col in colnumlist:
	tmp_parcelASD = extended_pheno_data_males[extended_pheno_data_males['DX_GROUP'] == 1]['Parcel_%s' % col]
    tmp_parcelTD = extended_pheno_data_males[extended_pheno_data_males['DX_GROUP'] == 2]['Parcel_%s' % col]
    tmp_result = scipy.stats.ttest_ind(tmp_parcelASD, tmp_parcelTD, nan_policy='omit')
    tmp_result = list(tmp_result)
    output_res.loc['Parcel_%s' % col] = tmp_result
#Adjusting the p value: FDR
FDRcor = fdrcorrection(pvals=output_res['p_value'], alpha=0.05) # also returns a bolean if hypothesis has been rejected
bolFDRcor = FDRcor[0]
qvalFDRcor = FDRcor[1]
output_res['q_value'] = qvalFDRcor
output_res['bolFDR'] = bolFDRcor

#Save it 
output_resname1 = 'FDRcorrected_ASD_vs_TD_parcelwiseTtest.csv'
output_res.to_csv(join(phenopath, output_resname1))


#Adjusting the p value: Bonferonni
BonferonniCor = multipletests()








