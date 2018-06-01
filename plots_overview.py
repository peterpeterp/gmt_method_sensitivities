import os,sys,glob,time,collections,gc
import numpy as np
from netCDF4 import Dataset,netcdftime,num2date
import matplotlib.pylab as plt
import dimarray as da
import itertools
import matplotlib
import pandas as pd
import seaborn as sn

os.chdir('/Users/peterpfleiderer/Documents/Projects/gmt/ReScience')


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


plt.close('all')
fig,axes=plt.subplots(nrows=1,ncols=5,figsize=(6,2),gridspec_kw = {'width_ratios':[3.3,3,3,3,2]})
axes=axes.flatten()
for model_run,ax,i in zip(tos_issues,axes[0:len(tos_issues)],range(len(tos_issues))):
	if np.isfinite(np.nanmean(gmt_all['_tosError','_remapbil','xax','rcp85',model_run,'gmt',:].values)):
		diff=(gmt_all['_tosError','_remapbil','xax','rcp85',model_run,var,1861:2100].values-gmt_cowtan['xax','rcp85',model_run,var,1861:2100].values)
		ax.plot(gmt_cowtan.time,diff)
		diff=(gmt_all['_normal','_remapbil','xax','rcp85',model_run,var,1861:2100].values-gmt_cowtan['xax','rcp85',model_run,var,1861:2100].values)
		ax.plot(gmt_cowtan.time,diff)
		diff=(gmt_all['_normal','_remapdis','xax','rcp85',model_run,var,1861:2100].values-gmt_cowtan['xax','rcp85',model_run,var,1861:2100].values)
		ax.plot(gmt_cowtan.time,diff)
	ax.text(1853,0.033,model_run.replace('_','\n'),fontsize=9)
	ax.set_xlim((1850,2100))
	ax.set_ylim((-0.05,0.05))
	ax.get_xaxis().set_visible(False)
	if i != 0:
		ax.get_yaxis().set_visible(False)
	else:
		ax.set_yticks([-0.05,-0.025,0,0.025,0.05])

ax=axes[-1]
ax.axis('off')

#plt.tight_layout()
plt.savefig('figures/overview_'+'xax'+'_tosError'+'.png')
#
