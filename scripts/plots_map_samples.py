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
	'files':['/p/projects/ipcc_pcmdi/ipcc_ar5_pcmdi/pcmdi_data/historical/OImon/sic/EC-EARTH/r1i1p1/sic_OImon_EC-EARTH_historical_r1i1p1_185001-200912.nc','data_models/EC-EARTH_r1i1p1/sic_rcp85_1861-2014.nc','data_models/EC-EARTH_r1i1p1/sic_rcp85_sicFix_1861-2014.nc'],
	'var_names':['sic','sic','sic'],
	'titles':['no NAN-treatment','correct NAN-treatment'],
	'outfile':'gmt_method_sensitivities/figures/maps_EC-EARTH_sicTreatment.png',
	'label':'sic [0-1]',
	'color_range':[0,1],
	'extend':[5,35,50,85],
	'time_steps':[132,0,0],
}
pl_mp.plot_maps(**arguments)


# tos treatment
arguments={
	'files':['/p/projects/ipcc_pcmdi/ipcc_ar5_pcmdi/pcmdi_data/historical/Omon/tos/EC-EARTH/r1i1p1/tos_Omon_EC-EARTH_historical_r1i1p1_185001-200912.nc','data_models/EC-EARTH_r1i1p1/tos_rcp85_tosError_1861-2014.nc','data_models/EC-EARTH_r1i1p1/tos_rcp85_1861-2014.nc'],
	'var_names':['tos','tos'],
	'titles':['no NAN-treatment','correct NAN-treatment'],
	'outfile':'gmt_method_sensitivities/figures/maps_EC-EARTH_tosTreatment.png',
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
