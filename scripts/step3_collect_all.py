import os,sys,glob,time,collections,gc
import numpy as np
from netCDF4 import Dataset,netcdftime,num2date
import matplotlib.pylab as plt
import dimarray as da
import pandas as pd

models=[]
runs=[]
model_runs=[]
for folder in [fl.split('/')[-1] for fl in glob.glob('../data_models/*')]:
	models.append(folder.split('_')[0])
	runs.append(folder.split('_')[1])
	model_runs.append(folder)

models=list(set(models))
runs=list(set(runs))
model_runs=list(set(model_runs))

styles=['xax','had4']
variables=['air','gmt']
versions=['_normal','_sftofError','_tosError','_CRU46','_sicError','_naive']
regrids=['_remapnn','_remapdis','_remapbil','_remapnn_sftlfBased','_remapdis_sftlfBased','_remapbil_sftlfBased']

'''
execute this to delete failed files
find ../data_models/*/ -name "*.txt" -size -99 -print
find ../data_models/*/ -name "*.txt" -size -99 -exec rm {} \;
'''

os.chdir('/p/projects/tumble/carls/shared_folder/gmt/gmt_method_sensitivities/')

tmp_example=pd.read_table('../data_models/ACCESS1-0_r1i1p1/had4_rcp85.txt',sep=' ',header=None)
gmt=da.DimArray(axes=[versions,regrids,styles,['rcp85'],model_runs,variables,np.array(tmp_example[0])],dims=['version','sftof_regrid','style','scenario','model_run','variable','time'])

for style in gmt.style:
	print style
	for scenario in gmt.scenario:
		print scenario
		for model_run in model_runs:
			for version in versions:
				for regrid in regrids:
					version_file='../data_models/'+model_run+'/'+style+'_'+scenario+regrid+version+'.txt'
					if os.path.isfile(version_file):
						tmp=pd.read_table(version_file,sep=' ',header=None)
						tmp.columns=['time','air','gmt','diff']
						time_ax=np.array(tmp['time'])
						useful_years=time_ax[(time_ax>1850) & (time_ax<2100)]
						gmt[version,regrid,style,scenario,model_run,'air',useful_years]=np.array(tmp['air'])[(time_ax>1850) & (time_ax<2100)]
						gmt[version,regrid,style,scenario,model_run,'gmt',useful_years]=np.array(tmp['gmt'])[(time_ax>1850) & (time_ax<2100)]



ds=da.Dataset({'gmt':gmt})
ds.write_nc('data/gmt_reproducedErrors.nc', mode='w')
