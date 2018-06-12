import os,sys,glob,time,collections,gc
import numpy as np
from netCDF4 import Dataset,netcdftime,num2date
import matplotlib.pylab as plt
import dimarray as da
import itertools
import matplotlib
import pandas as pd
import seaborn as sn

import cartopy.crs as ccrs
import cartopy

try:
	os.chdir('/p/projects/tumble/carls/shared_folder/gmt')
except:
	os.chdir('/Users/peterpfleiderer/Documents/Projects/gmt')

sys.path.append('gmt_method_sensitivities/scripts')

import plot_maps as pl_mp; reload(pl_mp)


# sic treatment
arguments={
	'files':['data_models/ACCESS1-0_r1i1p1/sic_rcp85_1861-2014.nc','data_models/ACCESS1-0_r1i1p1/sic_rcp85_sicFix_1861-2014.nc'],
	'var_names':['sic','sic'],
	'titles':['no NAN-treatment','correct NAN-treatment'],
	'outfile':'gmt_method_sensitivities/figures/maps_ACCESS1-0_sicTreatment.png',
	'label':'sic [%]',
	'color_range':[0,100],
	'extend':[-105,-75,50,85],
	'time_steps':[0,0],
}
pl_mp.plot_maps(**arguments)


# tos treatment
arguments={
	'files':['data_models/MIROC5_r1i1p1/tos_rcp85_tosError_1861-2014.nc','data_models/MIROC5_r1i1p1/tos_rcp85_1861-2014.nc'],
	'var_names':['tos','tos'],
	'titles':['no NAN-treatment','correct NAN-treatment'],
	'outfile':'gmt_method_sensitivities/figures/maps_MIROC5_tosTreatment.png',
	'label':'tos [K]',
	'color_range':[270,290],
	'extend':[-10,20,30,65],
	'time_steps':[0,0],
}
pl_mp.plot_maps(**arguments)

# CanESM2 tas
arguments={
	'files':['data_models/CanESM2_r1i1p1/sample_tas.nc','data_models/CanESM2_r1i1p1/sample_tas.nc'],
	'var_names':['tas','tas'],
	'titles':['January','August'],
	'time_steps':[0,7],
	'outfile':'gmt_method_sensitivities/figures/maps_CanESM2_tas.png',
	'label':'tas [K]',
	'color_range':[270,300],
	'extend':[-10,20,30,65],
	'nrows':1,
}
pl_mp.plot_maps(**arguments)

# CanESM2 tos
arguments={
	'files':['data_models/CanESM2_r1i1p1/sample_tos.nc','data_models/CanESM2_r1i1p1/sample_tos.nc'],
	'var_names':['tos','tos'],
	'titles':['January','August'],
	'time_steps':[0,7],
	'outfile':'gmt_method_sensitivities/figures/maps_CanESM2_tos.png',
	'label':'tos [K]',
	'color_range':[270,300],
	'extend':[-10,20,30,65],
	'nrows':1,
}
pl_mp.plot_maps(**arguments)

# CanESM2 sftof replace
arguments={
	'files':['sftof_regrid/ACCESS1-0_remapdis.nc','sftof_regrid/CanESM2_remapdis.nc'],
	'var_names':['sftof','sftof'],
	'titles':['ACCESS1-0','CanESM2'],
	'outfile':'gmt_method_sensitivities/figures/maps_sftof_CanESM2_ACCESS1-0.png',
	'label':'sftof [0-100]',
	'color_range':[0,100],
	'extend':[-10,20,30,65],
	'nrows':1,
}
pl_mp.plot_maps(**arguments)

# IPSL-CM5A-LR sftof replace
arguments={
	'files':['sftof_regrid/IPSL-CM5A-LR_remapbil.nc','sftof_regrid/IPSL-CM5A-LR_remapbil_NanTreated.nc','sftof_regrid/ACCESS1-0_remapbil.nc'],
	'var_names':['sftof','sftof','sftof'],
	'titles':['IPSL-CM5A-LR','IPSL-CM5A-LR nan treatment','ACCESS1-0'],
	'outfile':'gmt_method_sensitivities/figures/maps_sftof_IPSL-CM5A-LR.png',
	'label':'sftof [0-100]',
	'color_range':[0,100],
	'extend':[-10,20,30,65],
	'nrows':1,
}
pl_mp.plot_maps(**arguments)

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
