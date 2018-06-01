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


# arguments={
# 	'files':['data_models/rcp85-xxx_rcp85_EC-EARTH_r1i1p1/tos.nc','data_models/EC-EARTH_r1i1p1/tos.nc'],
# 	'var_names':['tos','tos'],
# 	'titles':['correct NAN-treatment','no NAN-treatment'],
# 	'outfile':'gmt_method_sensitivities/figures/maps_tosTreatment.png',
# 	'label':'tos [K]',
# 	'color_range':[270,290],
# 	'extend':[-10,20,40,65],
# 	'time_step':0,
# }
#
# pl_mp.plot_maps(**arguments)
#

# # ACCESS1-0 sftof regridding
# arguments={
# 	'files':['sftof_regrid/ACCESS1-0_remapdis.nc','sftof_regrid/ACCESS1-0_remapbil.nc','sftof_regrid/ACCESS1-0_remapnn.nc','sftof_regrid/ACCESS1-0_remapdis_sftlfBased.nc','sftof_regrid/ACCESS1-0_remapbil_sftlfBased.nc','sftof_regrid/ACCESS1-0_remapnn_sftlfBased.nc'],
# 	'var_names':['sftof','sftof','sftof','sftof','sftof','sftof'],
# 	'titles':['remapdis','remapbil','remapnn','remapdis from sftlf','remapbil from sftlf','remapnn from sftlf'],
# 	'outfile':'gmt_method_sensitivities/figures/maps_sftofRegrid.png',
# 	'label':'sftof [0-100]',
# 	'color_range':[0,100],
# 	'extend':[-10,20,40,65],
# 	'nrows':2,
# }

# CanESM2 tas
arguments={
	'files':['data_models/CanESM2_r1i1p1/sample_tas.nc','data_models/CanESM2_r1i1p1/sample_tas.nc'],
	'var_names':['tas','tas'],
	'titles':['tas','tas'],
	'time_steps':[0,7],
	'outfile':'gmt_method_sensitivities/figures/maps_CanESM2_tas.png',
	'label':'tas [K]',
	'color_range':[270,300],
	'extend':[-10,20,40,65],
	'nrows':1,
}
pl_mp.plot_maps(**arguments)

# ACCESS1-0 sftof regridding
arguments={
	'files':['sftof_regrid/ACCESS1-0_remapbil.nc','sftof_regrid/CanESM2_remapbil.nc'],
	'var_names':['sftof','sftof'],
	'titles':['ACCESS1-0','CanESM2'],
	'outfile':'gmt_method_sensitivities/figures/maps_sftof_CanESM2_ACCESS1-0.png',
	'label':'sftof [0-100]',
	'color_range':[0,100],
	'extend':[-10,20,40,65],
	'nrows':1,
}
