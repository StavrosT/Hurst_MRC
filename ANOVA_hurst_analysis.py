#!/bin/bash/env python3
#ANOVA with gender and diagnosis on each parcel
#after checking if assumptions are met


#Import libraries 
import pandas as pd
from pandas import plotting #pandas plotting
import matplotlib.pyplot as plt #makes plots appear
import scipy 
import numpy as np
from os.path import join #Like matlabs fullfile
import statsmodels.api as sm #for ANOVA output
from statsmodels.formula.api import ols #For R like formulas 
from statsmodels.stats.multitest import fdrcorrection #FDR from statsmodels

#Paths
rootpath = "/Users/stavrostrakoshis/Documents/MRC_Hurst"
codepath = join(rootpath, "code")
datapath = join(rootpath, "data")
phenopath =join(rootpath, "pheno")

#Read in file
pheno_file = join(phenopath, "tidy_data.xlsx")

pheno_data = pd.read_excel(pheno_file)

ardata = pd.DataFrame(pheno_data) #dataframe

#Subset only males
#maledata = ardata.loc[ardata['Sex'] == "M"]  

#Subset use subs

pheno_data = ardata.loc[ardata['use_subs'] == 1]

#First col as row names used to be here but it messes up the indexing later!
#Good thing to remember that order matters


#Get subject list to loop over

subjlist = pheno_data['sub_id']
subjlist = subjlist.values #makes it an array from df

#First col as row names (index in python)

pheno_data = pheno_data.set_index('sub_id')

#Empty frame
colnum = 180
tmp_data = pd.DataFrame(np.zeros((len(subjlist), colnum)))
tmp_data = tmp_data.set_index(subjlist)  #names rows

#Make a list from 1 to 180 (instead of 0-179) 
colnumlist = np.arange(1,colnum+1)

#Make an empty list 
colnames = []

#Loop for col names
for g in colnumlist:
 	colnames.append('Parcel_%s' % (g))

#Name empty matrix columns with colnames

tmp_data.columns = colnames


#Read in csvs for each subject

for isub in list(subjlist):
	SubHurst = '%s__Hurst.csv' % (isub)
	subfname = join(datapath, SubHurst)
	data12 = pd.read_csv(subfname, header=None)
	tmp_data.loc[isub] = data12.values


'''''''''''
#Unlock to
#make a preliminary output for visual checking
PO = 'ANOVA_tmp_data.csv'
tmp_data_path = join(phenopath, PO)
tmp_data.to_csv(tmp_data_path)
'''''''''
 	
#Join them into a big frame

frames = [pheno_data, tmp_data]
extended_pheno_data = pd.concat(frames, axis=1) 

#Write it 

ExtPDM = 'ANOVA_extended_pheno_data.csv'
ExtPDMpath = join(phenopath, ExtPDM)
extended_pheno_data.to_csv(ExtPDMpath) 

#Mean (etc) of stuff
extended_pheno_data[extended_pheno_data['Diagnosis'] == 'TD']['FIQ'].mean()
extended_pheno_data[extended_pheno_data['Diagnosis'] == 'TD'][['FIQ', 'VIQ']].mean()
#Or
#for general descriptives
extended_pheno_data.describe()

#Groupby for better implementation
#cleaner aesthitics 
#groupby spits/is an object

ASD_TD_pheno_datamales = extended_pheno_data.groupby('Diagnosis')
ASD_TD_mean = ASD_TD_pheno_datamales.mean()
ASD_TD_max = ASD_TD_pheno_datamales.max()


#CHECKING FOR two way ANOVA assumptions
maledata = extended_pheno_data.loc[extended_pheno_data['Sex'] == "M"]
femaledata = extended_pheno_data.loc[extended_pheno_data['Sex'] == "F"]

#Levene's test for equality of variances
Levene_output = pd.DataFrame(np.zeros(shape=(colnum, 2)))

#Take the names of parcels

parcel_names = []
for col in colnumlist:
	parcel_names.append('Parcel_%s' % col)
#index is parcel names
Levene_output.index = parcel_names

#colnames 
Levene_output.columns = ['Leven_Statistic_SEX', 'p_value']


#for 2nd comparison
Levene_output_DX = pd.DataFrame(np.zeros(shape=(colnum, 2)))
Levene_output_DX.index = parcel_names
Levene_output_DX.columns = ['Leven_Statistic_DX', 'p_value']

#Takes the value of H in each SEX
#and performs Levenes test
for col in colnumlist:
	tmp_F = extended_pheno_data[extended_pheno_data['Sex'] == 'F']['Parcel_%s' % col]
	tmp_M = extended_pheno_data[extended_pheno_data['Sex'] == 'M']['Parcel_%s' % col]
	tmp_out = scipy.stats.levene(tmp_F, tmp_M, center='mean')
	tmp_out = list(tmp_out)
	Levene_output.loc['Parcel_%s' % col] = tmp_out


#Levene in each DX
for col in colnumlist:	
	tmp_ASD = extended_pheno_data[extended_pheno_data['Diagnosis'] == 'Autism']['Parcel_%s' % col]
	tmp_TD = extended_pheno_data[extended_pheno_data['Diagnosis'] == 'TD']['Parcel_%s' % col]
	tmp_out_DX = list(scipy.stats.levene(tmp_ASD, tmp_TD, center='mean'))
	Levene_output_DX.loc['Parcel_%s' % col] = tmp_out_DX

#write them
ANOVA_Levene_SEX = 'ANOVA_Levene_SEX'
Levene_output.to_csv(join(phenopath, ANOVA_Levene_SEX))


ANOVA_Levene_DX = 'ANOVA_Levene_DX'
Levene_output_DX.to_csv(join(phenopath, ANOVA_Levene_DX))

#Normal distribution 
#with the shapiro Wilk test

Wilk_ASD=pd.DataFrame(np.zeros(shape=(colnum, 2)), index=parcel_names, columns=['Shapiro-Wilk','p_value'])
Wilk_TD=Wilk_ASD
Wilk_M=Wilk_ASD
Wilk_F=Wilk_M


for col in colnumlist:
	NT_ASD = extended_pheno_data[extended_pheno_data['Diagnosis'] == 'Autism']['Parcel_%s' % col]
	result_ASD = list(scipy.stats.normaltest(NT_ASD, axis=None, nan_policy='omit'))
	Wilk_ASD.loc['Parcel_%s' % col] = result_ASD

	NT_TD = extended_pheno_data[extended_pheno_data['Diagnosis'] == 'TD']['Parcel_%s' % col]
	result_TD = list(scipy.stats.normaltest(NT_TD, axis=None, nan_policy='omit'))
	Wilk_TD.loc['Parcel_%s' % col] = result_TD

	NT_M = extended_pheno_data[extended_pheno_data['Sex'] == 'M']['Parcel_%s' % col]
	result_M = list(scipy.stats.normaltest(NT_M, axis=None, nan_policy='omit'))
	Wilk_M.loc['Parcel_%s' % col] = result_M


	NT_F = extended_pheno_data[extended_pheno_data['Sex'] == 'F']['Parcel_%s' % col]
	result_F = list(scipy.stats.normaltest(NT_F, axis=None, nan_policy='omit'))
	Wilk_F.loc['Parcel_%s' % col] = result_F


#round every float in the resulting DFs to only 2 decimals
#I can't read imaginary nums

Wilk_ASD = Wilk_ASD.round(decimals=2)
Wilk_TD = Wilk_TD.round(decimals=2)
Wilk_M = Wilk_M.round(decimals=2)
Wilk_F = Wilk_F.round(decimals=2)

#Write them
ANOVA_Wilk_ASD = 'ANOVA_Normality_test_ASD.csv'
Wilk_ASD.to_csv(join(phenopath, ANOVA_Wilk_ASD))


ANOVA_Wilk_TD = 'ANOVA_Normality_test_TD.csv'
Wilk_TD.to_csv(join(phenopath, ANOVA_Wilk_TD))


ANOVA_Wilk_M = 'ANOVA_Normality_test_M.csv'
Wilk_M.to_csv(join(phenopath, ANOVA_Wilk_M))

ANOVA_Wilk_F = 'ANOVA_Normality_test_F.csv'
Wilk_F.to_csv(join(phenopath, ANOVA_Wilk_F))




#We want multiple logical/boolean indexing
#ANOVA



#empty df with 4 cols

output_res = pd.DataFrame(np.zeros(shape=(colnum, 6)))
output_res.index = parcel_names
output_res.columns = ['Dx-F_test', 'Dx-p_value', 'Sex-F_test', 'Sex-p_value', 'Interaction', 'Interaction-p_value']

#Conditions
for col in colnumlist:
	print(col)
	if  (Wilk_ASD.loc['Parcel_%s' % col, 'p_value'] > 0.05 and
		Wilk_TD.loc['Parcel_%s' % col, 'p_value'] > 0.05 and
		Wilk_M.loc['Parcel_%s' % col, 'p_value'] > 0.05 and
		Wilk_F.loc['Parcel_%s' % col, 'p_value'] > 0.05):


		print([col, 'its satisfied, will do an ANOVA on that'])
		#C is for categorical
		# % col thing can only be outside the string
		# this * in the linear model tests for interactions
		# otherwise is this +

		anova_lm = ols('Parcel_%s  ~ C(Diagnosis) * C(Sex)' % col, data=extended_pheno_data).fit()
		out_anova = pd.DataFrame(sm.stats.anova_lm(anova_lm))

		#index out_anova to get F, p on each comparison and feed it into output_res
		#up to 4 decimals
		output_res.loc['Parcel_%s' % col, 'Dx-F_test'] = out_anova.loc['C(Diagnosis)', 'F'].round(decimals=4)
		output_res.loc['Parcel_%s' % col, 'Dx-p_value'] = out_anova.loc['C(Diagnosis)', 'PR(>F)'].round(decimals=4)
		output_res.loc['Parcel_%s' % col, 'Sex-F_test'] = out_anova.loc['C(Sex)', 'F'].round(decimals=4)
		output_res.loc['Parcel_%s' % col, 'Sex-p_value'] = out_anova.loc['C(Sex)', 'PR(>F)'].round(decimals=4)
		output_res.loc['Parcel_%s' % col, 'Interaction'] = out_anova.loc['C(Diagnosis):C(Sex)', 'F'].round(decimals=4)
		output_res.loc['Parcel_%s' % col, 'Interaction-p_value'] = out_anova.loc['C(Diagnosis):C(Sex)', 'PR(>F)'].round(decimals=4)
	else:

		output_res.loc['Parcel_%s' % col, 'Dx-F_test'] = np.nan
		output_res.loc['Parcel_%s' % col, 'Dx-p_value'] = np.nan
		output_res.loc['Parcel_%s' % col, 'Sex-p_value'] = np.nan
		output_res.loc['Parcel_%s' % col, 'Sex-p_value'] = np.nan
		output_res.loc['Parcel_%s' % col, 'Interaction'] = np.nan
		output_res.loc['Parcel_%s' % col, 'Interaction-p_value'] = np.nan



#Adjusting the p value
Dx_pval = pd.DataFrame(output_res['Dx-p_value'])
Dx_pval.dropna(inplace=True)

Sex_pval = output_res['Sex-p_value']
Sex_pval.dropna(inplace=True)

Int_pval = output_res['Interaction-p_value']
Int_pval.dropna(inplace=True)


#most of this line is to remove nan
#and join the fdr results with output res

DxFDRcor = np.array(fdrcorrection(pvals=output_res['Dx-p_value'].dropna(), alpha=0.05)) # also returns a bolean if hypothesis has been rejected
dx_nonan = output_res['Dx-p_value'].dropna()
dx_index = dx_nonan.index.values
DxbolFDRcor = pd.DataFrame(DxFDRcor[0])
DxbolFDRcor.index = dx_index
DxbolFDRcor.rename(columns={0:'DxFDRlogical'}, inplace=True)
DxqvalFDRcor = pd.DataFrame(DxFDRcor[1])
DxqvalFDRcor.index = dx_index
DxqvalFDRcor.rename(columns={0:'DxFDR-q_val'}, inplace=True)
DxQ = pd.concat([DxbolFDRcor, DxqvalFDRcor], axis=1)
output_res = output_res.join(DxQ)



SexFDRcor = np.array(fdrcorrection(pvals=output_res['Sex-p_value'].dropna(), alpha=0.05))
sex_nonan = output_res['Sex-p_value'].dropna()
sex_index = sex_nonan.index.values
SexbolFDR = pd.DataFrame(SexFDRcor[0])
SexbolFDR.index = sex_index
SexbolFDR.rename(columns={0:'SexFDRlogical'}, inplace=True)
SexqvalFDR = pd.DataFrame(SexFDRcor[1])
SexqvalFDR.index = sex_index
SexqvalFDR.rename(columns={0: 'SexFDR-q_val'}, inplace=True)
SexQ = pd.concat([SexbolFDR, SexqvalFDR], axis=1)
output_res = output_res.join(SexQ)



IntFDRcor = np.array(fdrcorrection(pvals=output_res['Interaction-p_value'].dropna(), alpha=0.05))
Int_nonan = output_res['Interaction-p_value'].dropna()
Int_index = Int_nonan.index.values
IntbolFDR = pd.DataFrame(IntFDRcor[0])
IntbolFDR.index = Int_index
IntbolFDR.rename(columns={0: 'InteractionFDRlogical'}, inplace=True)
IntqvalFDR = pd.DataFrame(IntFDRcor[1])
IntqvalFDR.index = Int_index
IntqvalFDR.rename(columns={0: 'InteractionFDR-q_val'}, inplace=True)
IntQ = pd.concat([IntbolFDR, IntqvalFDR], axis=1)
output_res = output_res.join(IntQ)


#Save it 
output_resname1 = 'ANOVA_FDRcorrected.csv'
output_res.to_csv(join(phenopath, output_resname1))

#PLOTS  for FDR surviros
#these are sig in sex

parcel_147 = 'Parcel_147'
plotting.boxplot(extended_pheno_data, column='Parcel_147', by='Sex')
plt.savefig(join(phenopath, parcel_147))




parcel_37 = 'Parcel_37'
plotting.boxplot(extended_pheno_data, column='Parcel_37', by='Sex')
plt.savefig(join(phenopath, parcel_37))

plt.show()

parcel = 'Parcel_120'
plotting.boxplot(extended_pheno_data, column='Parcel_120', by='Sex')
plt.savefig(join(phenopath, parcel))

plt.show()


parcel = 'Parcel_1'
plotting.boxplot(extended_pheno_data, column='Parcel_1', by='Sex')
plt.savefig(join(phenopath, parcel))

plt.show()


#OK
#Adding covariates




