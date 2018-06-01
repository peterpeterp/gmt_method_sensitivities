import os,sys,glob,time,collections,gc
import numpy as np
from netCDF4 import Dataset,netcdftime,num2date
import matplotlib.pylab as plt
import dimarray as da
import itertools
import matplotlib
import pandas as pd
import seaborn as sns
sns.set()
plt.rc('font',family='Calibri')

os.chdir('/Users/peterpfleiderer/Documents/Projects/gmt/gmt_method_sensitivities')


gmt_cowtan=da.read_nc('../data/gmt_all_cowtan.nc')['gmt']

gmt_all=da.read_nc('data/gmt_reproducedErrors.nc')['gmt']

# select special runs
all_model_runs=[u'ACCESS1-0_r1i1p1',u'ACCESS1-3_r1i1p1',u'CCSM4_r1i1p1',u'CESM1-BGC_r1i1p1',u'CESM1-CAM5_r1i1p1',u'CMCC-CMS_r1i1p1',u'CMCC-CM_r1i1p1',u'CNRM-CM5_r1i1p1',\
		u'CSIRO-Mk3-6-0_r1i1p1',u'CanESM2_r1i1p1',u'EC-EARTH_r1i1p1',u'GFDL-CM3_r1i1p1',u'GFDL-ESM2G_r1i1p1',u'GFDL-ESM2M_r1i1p1',u'GISS-E2-H-CC_r1i1p1',u'GISS-E2-H_r1i1p1',\
		u'GISS-E2-R-CC_r1i1p1',u'GISS-E2-R_r1i1p1',u'HadGEM2-AO_r1i1p1',u'HadGEM2-CC_r1i1p1',u'HadGEM2-ES_r1i1p1',u'IPSL-CM5A-LR_r1i1p1',u'IPSL-CM5A-MR_r1i1p1',u'IPSL-CM5B-LR_r1i1p1',\
		u'MIROC-ESM-CHEM_r1i1p1',u'MIROC-ESM_r1i1p1',u'MIROC5_r1i1p1',u'MPI-ESM-LR_r1i1p1',u'MPI-ESM-MR_r1i1p1',u'MRI-CGCM3_r1i1p1',u'MRI-ESM1_r1i1p1',u'NorESM1-ME_r1i1p1',u'NorESM1-M_r1i1p1']

# tos issue models
tos_issues=[u'EC-EARTH_r1i1p1',
 u'MIROC5_r1i1p1',
 u'MRI-CGCM3_r1i1p1',
 u'MRI-ESM1_r1i1p1',]

def plot_single(model_run,style,var,versions,sftof_styles,outname,labels=None):
	if labels is None: labels=versions
	plt.close('all')
	fig,ax=plt.subplots(nrows=1,ncols=1,figsize=(4,4))
	for version,sftof_style,label in zip(versions,sftof_styles,labels):
		diff=(gmt_all[version,sftof_style,style,'rcp85',model_run,var,1861:2100].values-gmt_cowtan[style,'rcp85',model_run,var,1861:2100].values)
		ax.plot(range(1861,2100,1),diff.reshape((len(gmt_cowtan.time)/12,12)).mean(axis=-1),label=label)

	ax.text(1853,0.033,model_run.replace('_','\n'),fontsize=9)
	ax.set_xlim((1850,2100))
	#ax.set_ylim((-0.05,0.05))
	#ax.set_yticks([-0.05,-0.025,0,0.025,0.05])
	plt.legend()
	plt.tight_layout()
	plt.savefig(outname)

plot_single(model_run='EC-EARTH_r1i1p1',
			style='xax',
			var='gmt',
			versions=['_tosError','_sicError','_normal'],
			sftof_styles=['_remapbil','_remapbil','_remapbil'],
			outname='figures/tosError_EC-EARTH_r1i1p1.png')


plot_single(model_run='CanESM2_r1i1p1',
			style='xax',
			var='gmt',
			versions=['_sftofError','_normal'],
			sftof_styles=['_remapbil','_remapbil'],
			outname='figures/sftofError_CanESM2_r1i1p1.png')


plot_single(model_run='ACCESS1-0_r1i1p1',
			style='xax',
			var='gmt',
			versions=['_normal','_normal','_normal','_normal','_normal','_normal'],
			labels=['remapdis','remapbil','remapnn','remapdis from sftlf','remapbil from sftlf','remapnn from sftlf'],
			sftof_styles=['_remapdis','_remapbil','_remapnn','_remapdis_sftlfBased','_remapbil_sftlfBased','_remapnn_sftlfBased'],
			outname='figures/sftofSensitivity_ACCESS1-0_r1i1p1.png')
