#!bin/bash env python3



'''
This script adds the positive values of an Autocorrelation Function(ACF) of a time-series
before the first dive below zero as in Watanabe, T., Rees, G., & Masuda, N. (2019).
 Atypical intrinsic neural timescale in autism. eLife, 8, e42256.

The autocorrelation function is calculated based on the Furrier Fast Transform (FFT)
 and when the signal is not periodic there is the option to use FFT with zero-padding
e.g. in speech signal (DOI: 10.1109/89.952490).


Everything is store in a newly made Intrinsic_Time_Scale directory.



Arguments:
-i :Input e.g. *.csv Input is a dataframe with timepoints as rows and regions as columns

-t :The distance between time points e.g. the TR should be entered after the 

-o :Output name e.g. output.csv

-z :If entered do zeropadding

-p :If entered do 2 kinds of figures 


Examples 

python3 path/to/autocorrelation_fft.py -i TimeSeries.csv -t 2 -o AFC_.csv

python3 path/to/autocorrelation_fft.py -i TimeSeries.csv -t 0.5 -z -p -o AFC_.csv






'''
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt 
import os
from pandas.plotting import autocorrelation_plot
from statsmodels.graphics.tsaplots import plot_acf
from scipy.fftpack import fft, ifft, ifftshift
from optparse import OptionParser


#Define Arguments
def parse_args():

	parser=OptionParser()


	#input
	parser.add_option('-i', "--input", \
		dest='TimeSeries_Array', \
		help='DF (e.g. csv) with time-points as rows and location as columns', \
		default=None)
	#TR
	parser.add_option('-t', "--TimeResolution", \
		dest='TR', \
		help='Distance of time points in seconds (e.g. TR). In the original code its called TimeResolution', \
		default=None)
	#output
	parser.add_option('-o', "--output", \
		dest='output_fname', \
		help= 'Define output name', \
		default=None)
	#zero padding
	parser.add_option('-z', "--zero_padding", \
		dest='ZeroPadding', \
		help='Set this to True if you want zero-padding with the FFT (e.g. if signal is not periodic)', \
		default=False,
		action='store_true')
	#plots
	parser.add_option('-p', "--plots", \
		dest='PLOTS', \
		help='Set this to True if you want plots for every region', \
		action='store_true')



	#return values
	(options,args) = parser.parse_args()
	return (options)




#Calculate AFC using fft
#Without zero padding
#Any signal
def autocorrelation_nz(x):
    xp = (x - np.average(x))/np.std(x)
    lxp_d_2 = int(len(xp)/2)
    f = fft(xp)
    p = np.absolute(f)**2
    pi = ifft(p)
    output = np.real(pi)[:lxp_d_2]/(len(xp))
    return np.round(output, 2)


#Calculate AFC using fft
#with zeropadding 
#if signal not periodic


def autocorrelation_z_p(x):

    xp = ifftshift((x - np.average(x))/np.std(x))
    n, = xp.shape
    xp = np.r_[xp[:n//2], np.zeros_like(xp), xp[n//2:]]
    f = fft(xp)
    p = np.absolute(f)**2
    pi = ifft(p)
    output = np.real(pi)[:n//2]/(np.arange(n//2)[::-1]+n//2)
    return np.round(output, 2)


#get greater than 0
#first instances before first time AFC goes below zero
#without first elemnt which euqls to 1 (almost every time)

def greater_than_zero(output):
    
    import pandas as pd
    tmp_list = list()

    output = output[1:]
    for i in output:
        
        if i < 0:
            
            break
        else:
            tmp_list.append(i)

    return pd.Series(tmp_list)





#the sum of the positive AFC values
#is multiplied by the TR as in 

'''
Watanabe, T., Rees, G., & Masuda, N. (2019). Atypical intrinsic neural timescale in autism. eLife, 8, e42256.
'''

def intrinsic_ts(tmp_list):

	AFC_list = pd.Series(tmp_list)

	OUTPUT = np.round(np.sum(AFC_list) * TR, 4)
	return OUTPUT

'''
Initiate
'''
#read the inputs

if __name__ == '__main__':
	# parse arguments
    opts = parse_args()
    TimeSeries_Array = opts.TimeSeries_Array
    TR = int(opts.TR)
    output_fname = opts.output_fname
    ZeroPadding = opts.ZeroPadding
    PLOTS = opts.PLOTS




'''

##
#importing data

'''

df = pd.read_csv(TimeSeries_Array)
dirname = 'Intrinsic_Time_Scale'

if os.path.isdir(dirname) == False:
	os.mkdir(dirname)


#Make empty lists
i_list = [] #result list
region_list = [] #location list



#Evaluate Zeropadding option
#start process
for region in df:
	tmp_df = df[region]
	region_list.append(str(region))

	if ZeroPadding == False:
		output = autocorrelation_nz(tmp_df)
		G_T_Z = greater_than_zero(output)
		I_N_T_S = intrinsic_ts(G_T_Z)
		i_list.append(I_N_T_S)

		if PLOTS == True:
			tmp_fig = autocorrelation_plot(tmp_df)
			plt.title('AFC on all time points without FFT')
			plt.savefig(os.path.join(dirname,'AFC without FFT on region %s' %(region)))
			plt.clf()
			plt.close()

			print('**+fig 1 of %s was saved' %(region))

			tmp_fig2 = plot_acf(tmp_df, lags=20, fft=True)
			plt.title('AFC on all time points with FFT, on 20 lags')
			plt.savefig(os.path.join(dirname,'AFC with FFT on region %s' %(region)))
			plt.clf()
			plt.close()
			print('**+fig 2 of %s was saved' %(region))



	elif ZeroPadding == True:
		output = autocorrelation_z_p(tmp_df) #zeropadding
		G_T_Z = greater_than_zero(output)
		I_N_T_S = intrinsic_ts(G_T_Z)
		i_list.append(I_N_T_S)

		if PLOTS == True:
			tmp_fig = autocorrelation_plot(tmp_df)
			plt.title('AFC on all time points without FFT')
			plt.savefig(os.path.join(dirname,'AFC without FFT on region %s' %(region)))
			plt.clf()
			plt.close()

			print('**+fig 1 of %s was saved' %(region))

			tmp_fig2 = plot_acf(tmp_df, lags=20, fft=True, zero=True)
			plt.title('AFC on all time points with FFT on 20 lags including 0 lag')
			plt.savefig(os.path.join(dirname,'AFC with FFT on region %s' %(region)))
			plt.clf()
			plt.close()
			print('**+fig 2 of %s was saved' %(region))

	else:
		print('++*ZeroPadding must be True or False')






#dictionary and save as df
dictionary = {'regions': region_list, 'Intrinsic Time-scale': i_list}

df_out = pd.DataFrame(dictionary)
df_out.to_csv(os.path.join(dirname,output_fname))

print('**+ Done +**')




