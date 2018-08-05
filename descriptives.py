#!/bin/bash/env python

#runs with python3 in my mac-laptop, or ANACONDA 

#Import libs
import pandas as pd
from scipy.stats import ttest_ind #independent t-test
import scipy


#Insert path to data xlsx
data_path = '/Users/stavrostrakoshis/Documents/MRC_Hurst/pheno/tidy_data_males.xlsx'


#Read the excel

Exdata = pd.read_excel(data_path)

#Make it data frame

data = pd.DataFrame(Exdata)

#TD males,
#iloc is for integers

TDdata = data.iloc[0:33]
ASDdata = data.iloc[33:68]

#loc : subsets if and returns the value in a different column
#use subs if 'use_subs' == 1 and throw it into new variable
#.describe method provides sum stats

TDusable = TDdata.loc[data['use_subs'] == 1]

TDmalesDescriptives_all = TDusable.describe()

TDmalesDescriptives_all.to_csv('/Users/stavrostrakoshis/Documents/MRC_Hurst/pheno/TDmalesDescriptives.csv')

ASDusable = ASDdata.loc[data['use_subs'] == 1]

ASDmalesDescriptives_all = ASDusable.describe()

ASDmalesDescriptives_all.to_csv('/Users/stavrostrakoshis/Documents/MRC_Hurst/pheno/ASDmalesDescriptives.csv')

#stats

#Normality tests

scipy.stats.mstats.normaltest(TDusable['Age'], axis=None) #normal
scipy.stats.mstats.normaltest(ASDusable['Age'], axis=None) #normal

scipy.stats.mstats.normaltest(TDusable['FIQ'], axis=None) #NOT normal
scipy.stats.mstats.normaltest(ASDusable['FIQ'], axis=None) #normal

#Mann-whitney
#report median
ASDfiqMedian = ASDusable['FIQ']
ASDfiqMedian.median
TDfiqMedian = TDusable['FIQ']
TDfiqMedian.median

scipy.stats.mannwhitneyu(ASDusable['FIQ'], TDusable['FIQ'])

#t-test
ttest_ind(ASDusable['Age'], TDusable['Age'])