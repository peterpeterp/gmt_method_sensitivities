import os,glob,sys
from subprocess import Popen,PIPE
import dimarray as da
import numpy as np
from netCDF4 import Dataset,netcdftime,num2date


try:
	os.chdir('/p/projects/tumble/carls/shared_folder/gmt')
except:
	os.chdir('/Users/peterpfleiderer/Documents/Projects/gmt')


for file_name in glob.glob('sftof_regrid/raw/sftof_fx_*_historical_r0i0p0.nc'):
	model=file_name.split('_')[-3]
	for regrid_style in ['remapdis','remapnn','remapbil']:
		#Popen("cdo "+regrid_style+",blend-runnable/grid1x1.cdo "+file_name+" sftof_regrid/"+model+"_"+regrid_style+".nc",shell=True).wait()
		cdoinfo=Popen('cdo info '+file_name,shell=True, stdout=PIPE).stdout.read()
		if len(cdoinfo.split('\n')[1].split(' 0 '))==2:
			Popen("cdo "+regrid_style+",blend-runnable/grid1x1.cdo -setmisstoc,0 "+file_name+" sftof_regrid/"+model+"_"+regrid_style+"_NanTreated.nc",shell=True).wait()


# # using sftlf
# for file_name in glob.glob('/p/projects/ipcc_pcmdi/ipcc_ar5_pcmdi/pcmdi_data/historical/fx/sftlf/*/*/*'):
# 	model=file_name.split('_')[-3]
# 	Popen('cdo -mulc,-1 -subc,100 -chname,sftlf,sftof '+file_name+' sftof_raw/from_sftlf/'+model+'nc',shell=True).wait()
# 	for regrid_style in ['remapdis','remapnn','remapbil']:
# 		Popen("cdo "+regrid_style+",blend-runnable/grid1x1.cdo sftof_raw/from_sftlf/"+model+"nc sftof_regrid/"+model+"_"+regrid_style+"_sftlfBased.nc",shell=True).wait()
