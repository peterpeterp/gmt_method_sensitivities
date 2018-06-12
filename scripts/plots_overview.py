import os,sys,glob,time,collections,gc
import numpy as np
from netCDF4 import Dataset,netcdftime,num2date
import matplotlib.pylab as plt
import dimarray as da
import itertools
import matplotlib
import pandas as pd
import seaborn as sn

os.chdir('/Users/peterpfleiderer/Documents/Projects/gmt/gmt_method_sensitivities')


gmt_cowtan=da.read_nc('../data/gmt_all_cowtan.nc')['gmt']

gmt_all=da.read_nc('data/gmt_reproducedErrors.nc')['gmt']

# select special runs
all_model_runs=[u'ACCESS1-0_r1i1p1',u'ACCESS1-3_r1i1p1',u'CCSM4_r1i1p1',u'CESM1-BGC_r1i1p1',u'CMCC-CMS_r1i1p1',u'CMCC-CM_r1i1p1',u'CNRM-CM5_r1i1p1',\
		u'CSIRO-Mk3-6-0_r1i1p1',u'CanESM2_r1i1p1',u'EC-EARTH_r1i1p1',u'GFDL-CM3_r1i1p1',u'GFDL-ESM2G_r1i1p1',u'GFDL-ESM2M_r1i1p1',u'GISS-E2-H-CC_r1i1p1',u'GISS-E2-H_r1i1p1',\
		u'GISS-E2-R-CC_r1i1p1',u'GISS-E2-R_r1i1p1',u'HadGEM2-AO_r1i1p1',u'HadGEM2-CC_r1i1p1',u'HadGEM2-ES_r1i1p1',u'IPSL-CM5A-LR_r1i1p1',u'IPSL-CM5A-MR_r1i1p1',u'IPSL-CM5B-LR_r1i1p1',\
		u'MIROC-ESM-CHEM_r1i1p1',u'MIROC-ESM_r1i1p1',u'MIROC5_r1i1p1',u'MPI-ESM-LR_r1i1p1',u'MPI-ESM-MR_r1i1p1',u'MRI-CGCM3_r1i1p1',u'MRI-ESM1_r1i1p1',u'NorESM1-ME_r1i1p1',u'NorESM1-M_r1i1p1'] #,u'CESM1-CAM5_r1i1p1'

# tos issue models
tos_issues=[u'EC-EARTH_r1i1p1',
 u'MIROC5_r1i1p1',
 u'MRI-CGCM3_r1i1p1',
 u'MRI-ESM1_r1i1p1',]

var='gmt'
for style in ['xax','had4']:
	plt.close('all')
	fig,axes=plt.subplots(nrows=5,ncols=7,figsize=(8,8),gridspec_kw = {'width_ratios':[3,3,3,3,3,3,3]})
	axes=axes.flatten()
	for model_run,ax,i in zip(all_model_runs,axes[0:len(all_model_runs)],range(len(all_model_runs))):
		if np.isfinite(np.nanmean(gmt_all['_normal','_remapbil',style,'rcp85',model_run,'gmt',:].values)):
			diff=(gmt_all['_naive','_remapbil',style,'rcp85',model_run,var,1861:2100].values-gmt_cowtan[style,'rcp85',model_run,var,1861:2100].values)
			ax.plot(range(1861,2100,1),diff.reshape((len(gmt_cowtan.time)/12,12)).mean(axis=-1),label='straight forward pre-processing')
			# diff=(gmt_all['_normal','_remapbil',style,'rcp85',model_run,var,1861:2100].values-gmt_cowtan[style,'rcp85',model_run,var,1861:2100].values)
			# ax.plot(range(1861,2100,1),diff.reshape((len(gmt_cowtan.time)/12,12)).mean(axis=-1),label='closest to original')

		ax.annotate(model_run.split('_')[0],fontsize=9, xy=(0.02, 0.9), xycoords='axes fraction')
		ax.set_xlim((1850,2100))
		ax.set_ylim((-0.05,0.05))
		ax.get_xaxis().set_visible(False)
		ax.set_yticks([-0.05,-0.025,0,0.025,0.05])
		if i%7 != 0:
			ax.yaxis.set_ticklabels([])
		if i==14:
			ax.set_ylabel('deviations from original [K]')

	#ax.legend(loc='left',bbox_to_anchor=(4.4, 1.05))

	for ax in axes[-3:]:
		ax.axis('off')

	#plt.tight_layout()
	plt.savefig('figures/overview_'+style+'.png')
#


var='gmt'
for style in ['xax']:
	plt.close('all')
	fig,axes=plt.subplots(nrows=5,ncols=7,figsize=(8,8),gridspec_kw = {'width_ratios':[3,3,3,3,3,3,3]})
	axes=axes.flatten()
	for model_run,ax,i in zip(all_model_runs,axes[0:len(all_model_runs)],range(len(all_model_runs))):
		if np.isfinite(np.nanmean(gmt_all['_normal','_remapbil',style,'rcp85',model_run,'gmt',:].values)):
			for regrid in ['_remapdis','_remapbil','_remapnn','_remapdis_sftlfBased','_remapbil_sftlfBased','_remapnn_sftlfBased']:
				diff=(gmt_all['_normal',regrid,style,'rcp85',model_run,var,1861:2100].values-gmt_cowtan[style,'rcp85',model_run,var,1861:2100].values)
				ax.plot(range(1861,2100,1),diff.reshape((len(gmt_cowtan.time)/12,12)).mean(axis=-1),label=regrid.replace('_',''))

		ax.annotate(model_run.split('_')[0],fontsize=9, xy=(0.02, 0.9), xycoords='axes fraction')
		ax.set_xlim((1850,2100))
		ax.set_ylim((-0.025,0.025))
		ax.get_xaxis().set_visible(False)
		ax.set_yticks([-0.025,-0.0125,0,0.0125,0.025])
		if i%7 != 0:
			ax.yaxis.set_ticklabels([])

	ax.legend(bbox_to_anchor=(1.1, 1.05))
	for ax in axes[-3:]:
		ax.axis('off')

	#plt.tight_layout()
	plt.savefig('figures/overview_'+style+'_remapSFTOF.png')
