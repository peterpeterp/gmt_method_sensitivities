import os,glob,sys
import subprocess
from subprocess import Popen
import numpy as np
from netCDF4 import Dataset,netcdftime,num2date
import dimarray as da
import pandas as pd
import collections

try:
	os.chdir('/p/projects/tumble/carls/shared_folder/gmt')
except:
	os.chdir('/Users/peterpfleiderer/Documents/Projects/gmt')


all_model_runs=['ACCESS1-0_r1i1p1','CCSM4_r2i1p1','CESM1-CAM5_r1i1p1','CNRM-CM5_r10i1p1','CSIRO-Mk3-6-0_r1i1p1','CSIRO-Mk3-6-0_r7i1p1','CanESM2_r4i1p1',\
	'EC-EARTH_r1i1p1','FIO-ESM_r1i1p1','GISS-E2-H-CC_r1i1p1','GISS-E2-R_r1i1p2','HadGEM2-ES_r3i1p1','IPSL-CM5A-LR_r4i1p1','MIROC5_r2i1p1','MRI-CGCM3_r1i1p1',\
	'ACCESS1-3_r1i1p1','CCSM4_r3i1p1','CESM1-CAM5_r2i1p1','CNRM-CM5_r1i1p1','CSIRO-Mk3-6-0_r2i1p1','CSIRO-Mk3-6-0_r8i1p1','CanESM2_r5i1p1','EC-EARTH_r2i1p1',\
	'FIO-ESM_r2i1p1','GISS-E2-H_r1i1p1','GISS-E2-R_r1i1p3','HadGEM2-ES_r4i1p1','IPSL-CM5A-MR_r1i1p1','MIROC5_r3i1p1','MRI-ESM1_r1i1p1','BCC-CSM1-1-M_r1i1p1',\
	'CCSM4_r4i1p1','CESM1-CAM5_r3i1p1','CNRM-CM5_r2i1p1','CSIRO-Mk3-6-0_r3i1p1','CSIRO-Mk3-6-0_r9i1p1','EC-EARTH_r11i1p1','EC-EARTH_r6i1p1','FIO-ESM_r3i1p1',\
	'GISS-E2-H_r1i1p2','HadGEM2-AO_r1i1p1','INMCM4_r1i1p1','IPSL-CM5B-LR_r1i1p1','MPI-ESM-LR_r1i1p1','NorESM1-ME_r1i1p1','BCC-CSM1-1_r1i1p1','CCSM4_r5i1p1',\
	'CESM1-WACCM_r2i1p1','CNRM-CM5_r4i1p1','CSIRO-Mk3-6-0_r4i1p1','CanESM2_r1i1p1','EC-EARTH_r12i1p1','EC-EARTH_r7i1p1','GFDL-CM3_r1i1p1','GISS-E2-H_r1i1p3',\
	'HadGEM2-CC_r1i1p1','IPSL-CM5A-LR_r1i1p1','MIROC-ESM-CHEM_r1i1p1','MPI-ESM-LR_r2i1p1','NorESM1-M_r1i1p1','BNU-ESM_r1i1p1','CCSM4_r6i1p1','CMCC-CMS_r1i1p1',\
	'CNRM-CM5_r6i1p1','CSIRO-Mk3-6-0_r5i1p1','CanESM2_r2i1p1','EC-EARTH_r13i1p1','EC-EARTH_r8i1p1','GFDL-ESM2G_r1i1p1','GISS-E2-R-CC_r1i1p1','HadGEM2-ES_r1i1p1',\
	'IPSL-CM5A-LR_r2i1p1','MIROC-ESM_r1i1p1','MPI-ESM-LR_r3i1p1','CCSM4_r1i1p1','CESM1-BGC_r1i1p1','CMCC-CM_r1i1p1','CSIRO-Mk3-6-0_r10i1p1','CSIRO-Mk3-6-0_r6i1p1',\
	'CanESM2_r3i1p1','EC-EARTH_r14i1p1','EC-EARTH_r9i1p1','GFDL-ESM2M_r1i1p1','GISS-E2-R_r1i1p1','HadGEM2-ES_r2i1p1','IPSL-CM5A-LR_r3i1p1','MIROC5_r1i1p1','MPI-ESM-MR_r1i1p1']


import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--overwrite",'-o', help="overwrite output files",action="store_true")
parser.add_argument("--keep",'-k', help="keep in between files files",action="store_true")
parser.add_argument('--model_run','-mr',help='model name',default=None)
parser.add_argument('--job_id','-ji',help='id',default=None,type=np.int)
parser.add_argument('--variable','-v' ,help='variables to prepare',nargs='+',required=False)
args = parser.parse_args()

if args.overwrite:
	overwrite=True
else:
	overwrite=False

if args.keep:
	keep=True
else:
	keep=False

if args.job_id is None:
	model_run=args.model_run
else:
	model_run=all_model_runs[args.job_id]

model=model_run.split('_')[0]
run=model_run.split('_')[1]

if args.variable is not None:
	var_names=args.variable
else:
	var_names=['tas','sic','tos']

# there seems to be some issue with cdo/1.8.0 and this script
# the command has to be executed outside the script?
# os.system('module load cdo/1.7.0')


Popen('mkdir data_models/'+model+'_'+run, shell=True).wait()
os.chdir('data_models/'+model+'_'+run+'/')

os.system('export SKIP_SAME_TIME=1')

# ++++++++++++++++++++++++++++++
# + get files
# ++++++++++++++++++++++++++++++

variable={'tas':'Amon','sic':'OImon','tos':'Omon'}

sftof_replace_dict_naive={'HadGEM2-AO':'HadGEM2-ES',
					'GISS-E2-R-CC':'GISS-E2-R',
					'GISS-E2-H-CC':'GISS-E2-H',
					'CNRM-CM5':'CNRM-CM5-2',
					} #'CESM1-CAM5':'CESM1-BGC'

def normal_procedure(model,run,scenario,group,var,overwrite):
	command='cdo -O -a mergetime '
	hist_files=glob.glob('/p/projects/ipcc_pcmdi/ipcc_ar5_pcmdi/pcmdi_data/historical/'+group+'/'+var+'/'+model+'/'+run+'/*')
	if len(hist_files)==0:
		hist_files=glob.glob('/p/projects/tumble/carls/shared_folder/gmt/missing_files/'+var+'*'+group+'*'+model+'*historical*'+run+'*')
	scenario_files=glob.glob('/p/projects/ipcc_pcmdi/ipcc_ar5_pcmdi/pcmdi_data/'+scenario+'/'+group+'/'+var+'/'+model+'/'+run+'/*')
	if len(scenario_files)==0:
		scenario_files=glob.glob('/p/projects/tumble/carls/shared_folder/gmt/missing_files/'+var+'*'+group+'*'+model+'*'+scenario+'*'+run+'*')

	sftof_files=glob.glob('../../sftof_raw/*'+model+'*')
	if len(scenario_files)!=0:
		if var=='sic' and len(sftof_files)==1:
			sftof_file=sftof_files[0]
			for file_name in scenario_files+hist_files:
				print file_name
				command+=file_name+' '
			Popen(command+'tmp_m_'+var+'.nc',shell=True).wait()
			Popen('cdo -O ifthen '+sftof_file+' -selyear,1861/2099 tmp_m_'+var+'.nc tmp_s_'+var+'.nc',shell=True).wait()
			Popen('cdo -O remapdis,../../blend-runnable/grid1x1.cdo tmp_s_'+var+'.nc '+var+'_'+scenario+'_sicFix_1861-2099.nc',shell=True).wait()
			os.system('cdo -O -selyear,1861/2014 '+var+'_'+scenario+'_sicFix_1861-2099.nc '+var+'_'+scenario+'_sicFix_1861-2014.nc')
			if keep==False:
				Popen('rm tmp_s_'+var+'.nc tmp_m_'+var+'.nc tmp_zwi_'+var+'.nc',shell=True).wait()

for scenario in ['rcp85']:
	for var in var_names:
		group=variable[var]
		print scenario,var,group
		print model,run
		normal_procedure(model,run,scenario,group,var,overwrite)
