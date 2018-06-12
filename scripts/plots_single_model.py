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


import cartopy.crs as ccrs
import cartopy

try:
	os.chdir('/p/projects/tumble/carls/shared_folder/gmt')
except:
	os.chdir('/Users/peterpfleiderer/Documents/Projects/gmt')

sys.path.append('gmt_method_sensitivities/scripts')

import plot_maps as pl_mp; reload(pl_mp)

os.system('ls')

gmt_cowtan=da.read_nc('data/gmt_all_cowtan.nc')['gmt']

gmt_all=da.read_nc('gmt_method_sensitivities/data/gmt_reproducedErrors.nc')['gmt']

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

def plot_single(model_run,style,var,versions,sftof_styles,outname,labels=None,ylabel=None,title=None,loc='best'):
	if labels is None: labels=versions
	if title is None: title=model_run.replace('_',' ')
	plt.close('all')
	fig,ax=plt.subplots(nrows=1,ncols=1,figsize=(3,3))
	for version,sftof_style,label in zip(versions,sftof_styles,labels):
		diff=(gmt_all[version,sftof_style,style,'rcp85',model_run,var,1861:2100].values-gmt_cowtan[style,'rcp85',model_run,var,1861:2100].values)
		ax.plot(range(1861,2100,1),diff.reshape((len(gmt_cowtan.time)/12,12)).mean(axis=-1),label=label)

	ax.set_xlim((1850,2100))
	#ax.set_ylim((-0.05,0.05))
	#ax.set_yticks([-0.05,-0.025,0,0.025,0.05])
	ax.set_title(title)
	ax.set_ylabel(ylabel)
	ax.legend(loc=loc)
	plt.tight_layout()
	plt.savefig(outname)

def add_single(ax,model_run,style,var,versions,sftof_styles,outname,labels=None,ylabel=None,title=None,loc='best'):
	if labels is None: labels=versions
	if title is None: title=model_run.replace('_',' ')
	for version,sftof_style,label in zip(versions,sftof_styles,labels):
		diff=(gmt_all[version,sftof_style,style,'rcp85',model_run,var,1861:2100].values-gmt_cowtan[style,'rcp85',model_run,var,1861:2100].values)
		ax.plot(range(1861,2100,1),diff.reshape((len(gmt_cowtan.time)/12,12)).mean(axis=-1),label=label)
	ax.set_xlim((1850,2100))
	ax.set_xticks(range(1850,2100,100))

	#ax.set_ylim((-0.05,0.05))
	#ax.set_yticks([-0.05,-0.025,0,0.025,0.05])
	ax.set_title(title)
	ax.set_ylabel(ylabel)
	ax.legend(loc=loc)


# sftof replace treatment
arguments={
	'files':['sftof_regrid/IPSL-CM5A-LR_remapbil.nc','sftof_regrid/IPSL-CM5A-LR_remapbil_NanTreated.nc','sftof_regrid/ACCESS1-0_remapbil.nc'],
	#'files':['data_models/CanESM2_r1i1p1/sample_tas.nc','data_models/CanESM2_r1i1p1/sample_tas.nc','data_models/CanESM2_r1i1p1/sample_tas.nc'],
	'var_names':['sftof','sftof','sftof'],
	'titles':['IPSL-CM5A-LR','IPSL-CM5A-LR nan treatment','ACCESS1-0'],
	'label':'sftof [0-100]',
	'color_range':[0,100],
	'extend':[-10,20,30,65],
	#'time_steps':[0,0,0],
	'nrows':1,
	'add_cols':1,
}
fig,axes=pl_mp.plot_maps(**arguments)
new_ax=fig.add_axes([0.05,0.071,0.18,0.858])
add_single(ax=new_ax,
			model_run='IPSL-CM5A-LR_r1i1p1',
			style='xax',
			var='gmt',
			ylabel='deviation from Cowtan2015 [K]',
			versions=['_sftofError','_sftofNanTreated','_normal'],
			labels=['original sftof','NAN treatment in sftof','ACCESS1-0 sftof'],
			sftof_styles=['_remapbil','_remapbil','_remapbil'],
			outname='figures/sftofError_IPSL-CM5A-LR.png')
fig.tight_layout()
plt.savefig('gmt_method_sensitivities/figures/sftofError_IPSL-CM5A-LR.png',dpi=300)

asdasd
# sic treatment
arguments={
	'files':['data_models/ACCESS1-0_r1i1p1/sic_rcp85_1861-2014.nc','data_models/ACCESS1-0_r1i1p1/sic_rcp85_sicFix_1861-2014.nc'],
	'var_names':['sic','sic'],
	'titles':['no NAN-treatment','correct NAN-treatment'],
	'label':'sic [%]',
	'color_range':[0,100],
	'extend':[-105,-75,50,85],
	'time_steps':[0,0],
	'add_cols':1,
}
fig,axes=pl_mp.plot_maps(**arguments)
new_ax=fig.add_axes([0.1,0.1,0.18,0.8])
add_single(ax=new_ax,
			model_run='ACCESS1-0_r1i1p1',
			style='xax',
			var='gmt',
			ylabel='deviation from Cowtan2015 [K]',
			versions=['_sicError','_normal'],
			labels=['0 over land-cells','missing over land-cells'],
			loc='lower left',
			sftof_styles=['_remapbil','_remapbil','_remapbil'],
			outname='figures/sicError_ACCESS1-0.png')
fig.tight_layout()
plt.savefig('gmt_method_sensitivities/figures/sicError_ACCESS1-0.png',dpi=300)

# tos treatment
arguments={
	'files':['data_models/MIROC5_r1i1p1/tos_rcp85_tosError_1861-2014.nc','data_models/MIROC5_r1i1p1/tos_rcp85_1861-2014.nc'],
	'var_names':['tos','tos'],
	'titles':['no NAN-treatment','correct NAN-treatment'],
	'label':'tos [K]',
	'color_range':[270,290],
	'extend':[-10,20,30,65],
	'time_steps':[0,0],
	'add_cols':1,
}
fig,axes=pl_mp.plot_maps(**arguments)
new_ax=fig.add_axes([0.1,0.1,0.18,0.8])
add_single(ax=new_ax,
			model_run='MIROC5_r1i1p1',
			style='xax',
			var='gmt',
			ylabel='deviation from Cowtan2015 [K]',
			versions=['_tosError','_normal'],
			labels=['0 over land-cells','missing over land-cells'],
			sftof_styles=['_remapbil','_remapbil','_remapbil'],
			outname='figures/tosError_MIROC5.png')
fig.tight_layout()
plt.savefig('gmt_method_sensitivities/figures/tosError_MIROC5.png',dpi=300)



# ACCESS1-0 sftof regridding
arguments={
	'files':['sftof_regrid/ACCESS1-0_remapdis.nc','sftof_regrid/ACCESS1-0_remapbil.nc','sftof_regrid/ACCESS1-0_remapnn.nc','sftof_regrid/ACCESS1-0_remapdis_sftlfBased.nc','sftof_regrid/ACCESS1-0_remapbil_sftlfBased.nc','sftof_regrid/ACCESS1-0_remapnn_sftlfBased.nc'],
	'var_names':['sftof','sftof','sftof','sftof','sftof','sftof'],
	'titles':['remapdis','remapbil','remapnn','remapdis from sftlf','remapbil from sftlf','remapnn from sftlf'],
	'outfile':'gmt_method_sensitivities/figures/maps_ACCESS1-0_sftofRegrid.png',
	'label':'sftof [0-100]',
	'color_range':[0,100],
	'extend':[-10,20,40,65],
	'nrows':2,
}
pl_mp.plot_maps(**arguments)



plot_single(model_run='ACCESS1-0_r1i1p1',
			style='xax',
			var='gmt',
			ylabel='deviation from Cowtan2015 [K]',
			versions=['_normal','_normal','_normal','_normal','_normal','_normal'],
			labels=['remapdis','remapbil','remapnn','remapdis from sftlf','remapbil from sftlf','remapnn from sftlf'],
			sftof_styles=['_remapdis','_remapbil','_remapnn','_remapdis_sftlfBased','_remapbil_sftlfBased','_remapnn_sftlfBased'],
			outname='gmt_method_sensitivities/figures/sftofSensitivity_ACCESS1-0_r1i1p1.png')


plot_single(model_run='ACCESS1-0_r1i1p1',
			style='had4',
			var='gmt',
			ylabel='deviation from Cowtan2015 [K]',
			versions=['_CRU46','_normal'],
			labels=['CRU4.6.0','CRU4.3.0'],
			sftof_styles=['_remapbil','_remapbil'],
			outname='gmt_method_sensitivities/figures/CRU46_ACCESS1-0.png')
