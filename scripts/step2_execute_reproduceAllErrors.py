import os,glob,sys
from subprocess import Popen
import numpy as np

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
parser.add_argument('--model_run','-mr',help='model name',default=None)
parser.add_argument('--job_id','-ji',help='id',default=None,type=np.int)
# parser.add_argument('--style','-s' ,help='blending-masking style',required=True)
parser.add_argument('--versions','-v' ,help='error versions',nargs='+',default=None)
parser.add_argument('--regrid_styles','-rs' ,help='sftof regrid_styles',nargs='+',default=None)
args = parser.parse_args()

if args.overwrite:
    overwrite=True
else:
    overwrite=False

if args.job_id is None:
	model_run=args.model_run
else:
	model_run=all_model_runs[args.job_id]
model=model_run.split('_')[0]
run=model_run.split('_')[1]

if args.versions is None:
	versions=['_normal','_sftofError','_tosError','_CRU46','_sicError']
else:
	versions=args.versions

if args.regrid_styles is None:
	regrid_styles=['_remapnn','_remapdis','_remapbil']
	regrid_styles=['_remapnn_sftlfBased','_remapdis_sftlfBased','_remapbil_sftlfBased']
else:
	regrid_styles=args.regrid_styles

# style=args.style



scenario = 'rcp85'

# some replacements because sftof missing
# some replacements because of bad sftof file
sftof_replace_dict={'HadGEM2-AO':'HadGEM2-ES',
					'GISS-E2-R-CC':'GISS-E2-R',
					'GISS-E2-H-CC':'GISS-E2-H',
					'CNRM-CM5':'CNRM-CM5-2',
					'BNU-ESM':'ACCESS1-0',
					'CESM1-CAM5':'ACCESS1-0',
					'CanESM2':'ACCESS1-0',
					'IPSL-CM5A-LR':'ACCESS1-0',
					'IPSL-CM5A-MR':'ACCESS1-0',
					'IPSL-CM5B-LR':'ACCESS1-0',
					} #'CESM1-CAM5':'CESM1-BGC'

sftof_replace_dict_naive={'HadGEM2-AO':'HadGEM2-ES',
					'GISS-E2-R-CC':'GISS-E2-R',
					'GISS-E2-H-CC':'GISS-E2-H',
					'CNRM-CM5':'CNRM-CM5-2',
					} #'CESM1-CAM5':'CESM1-BGC'


for sftof_style in regrid_styles:


	# reproduce all errors
	if '_naive' in versions:
		tas='data_models/'+model+'_'+run+'/tas_'+scenario+'_1861-2099.nc'
		if os.path.isfile('data_models/'+model+'_'+run+'/tos_'+scenario+'_tosError.nc'):
			tos='data_models/'+model+'_'+run+'/tos_'+scenario+'_tosError_1861-2099.nc'
		else:
			tos='data_models/'+model+'_'+run+'/tos_'+scenario+'_1861-2099.nc'
		sic='data_models/'+model+'_'+run+'/sic_'+scenario+'_1861-2099.nc'
		if model in sftof_replace_dict_naive.keys():
			sftof='sftof_regrid/'+sftof_replace_dict_naive[model]+sftof_style+'.nc'
		else:
			sftof='sftof_regrid/'+model+sftof_style+'.nc'
		Popen('python gmt_methods/ncblendmask-nc4.py '+style+' '+tas+' '+tos+' '+sic+' '+sftof+' > data_models/'+model+'_'+run+'/'+style+'_'+scenario+sftof_style+'_naive.txt',shell=True).wait()
		Popen('python gmt_methods/ncblendhadcrut-nc4.py '+tas.replace('2099','2014')+' '+tos.replace('2099','2014')+' '+sic.replace('2099','2014')+' '+sftof+'  blend-runnable/CRU.nc blend-runnable/SST.nc > data_models/'+model+'_'+run+'/had4_'+scenario+sftof_style+'_naive.txt',shell=True).wait()


	# reproduce sic error only
	if '_sicError' in versions:
		tas='data_models/'+model+'_'+run+'/tas_'+scenario+'_1861-2099.nc'
		tos='data_models/'+model+'_'+run+'/tos_'+scenario+'_1861-2099.nc'
		sic='data_models/'+model+'_'+run+'/sic_'+scenario+'_1861-2099.nc'
		if model in sftof_replace_dict.keys():
			sftof='sftof_regrid/'+sftof_replace_dict[model]+sftof_style+'.nc'
		else:
			sftof='sftof_regrid/'+model+sftof_style+'.nc'
		Popen('python gmt_methods/ncblendmask-nc4.py '+style+' '+tas+' '+tos+' '+sic+' '+sftof+' > data_models/'+model+'_'+run+'/'+style+'_'+scenario+sftof_style+'_sicError.txt',shell=True).wait()
		Popen('python gmt_methods/ncblendhadcrut-nc4.py '+tas.replace('2099','2014')+' '+tos.replace('2099','2014')+' '+sic.replace('2099','2014')+' '+sftof+'  blend-runnable/CRU.nc blend-runnable/SST.nc > data_models/'+model+'_'+run+'/had4_'+scenario+sftof_style+'_sicError.txt',shell=True).wait()




	# reproduce tos error only
	if '_tosError' in versions:
		tas='data_models/'+model+'_'+run+'/tas_'+scenario+'_1861-2099.nc'
		sic='data_models/'+model+'_'+run+'/sic_'+scenario+'_sicFix_1861-2099.nc'
		if os.path.isfile('data_models/'+model+'_'+run+'/tos_'+scenario+'_tosError.nc'):
			tos='data_models/'+model+'_'+run+'/tos_'+scenario+'_tosError_1861-2099.nc'
			if model in sftof_replace_dict.keys():
				sftof='sftof_regrid/'+sftof_replace_dict[model]+sftof_style+'.nc'
			else:
				sftof='sftof_regrid/'+model+sftof_style+'.nc'
			Popen('python gmt_methods/ncblendmask-nc4.py '+style+' '+tas+' '+tos+' '+sic+' '+sftof+' > data_models/'+model+'_'+run+'/'+style+'_'+scenario+sftof_style+'_tosError.txt',shell=True).wait()
			Popen('python gmt_methods/ncblendhadcrut-nc4.py '+tas.replace('2099','2014')+' '+tos.replace('2099','2014')+' '+sic.replace('2099','2014')+' '+sftof+'  blend-runnable/CRU.nc blend-runnable/SST.nc > data_models/'+model+'_'+run+'/had4_'+scenario+sftof_style+'_tosError.txt',shell=True).wait()


	# reproduce sftof replace only
	if '_sftofError' in versions:
		tas='data_models/'+model+'_'+run+'/tas_'+scenario+'_1861-2099.nc'
		tos='data_models/'+model+'_'+run+'/tos_'+scenario+'_1861-2099.nc'
		sic='data_models/'+model+'_'+run+'/sic_'+scenario+'_sicFix_1861-2099.nc'
		if model in sftof_replace_dict_naive.keys():
			sftof='sftof_regrid/'+sftof_replace_dict_naive[model]+sftof_style+'.nc'
		else:
			sftof='sftof_regrid/'+model+sftof_style+'.nc'
		Popen('python gmt_methods/ncblendmask-nc4.py '+style+' '+tas+' '+tos+' '+sic+' '+sftof+' > data_models/'+model+'_'+run+'/'+style+'_'+scenario+sftof_style+'_sftofError.txt',shell=True).wait()
		Popen('python gmt_methods/ncblendhadcrut-nc4.py '+tas.replace('2099','2014')+' '+tos.replace('2099','2014')+' '+sic.replace('2099','2014')+' '+sftof+'  blend-runnable/CRU.nc blend-runnable/SST.nc > data_models/'+model+'_'+run+'/had4_'+scenario+sftof_style+'_sftofError.txt',shell=True).wait()


	# reproduce normal
	if '_normal' in versions:
		tas='data_models/'+model+'_'+run+'/tas_'+scenario+'_1861-2099.nc'
		tos='data_models/'+model+'_'+run+'/tos_'+scenario+'_1861-2099.nc'
		sic='data_models/'+model+'_'+run+'/sic_'+scenario+'_sicFix_1861-2099.nc'
		if model in sftof_replace_dict.keys():
			sftof='sftof_regrid/'+sftof_replace_dict[model]+sftof_style+'.nc'
		else:
			sftof='sftof_regrid/'+model+sftof_style+'.nc'
		Popen('python gmt_methods/ncblendmask-nc4.py '+style+' '+tas+' '+tos+' '+sic+' '+sftof+' > data_models/'+model+'_'+run+'/'+style+'_'+scenario+sftof_style+'_normal.txt',shell=True).wait()
		Popen('python gmt_methods/ncblendhadcrut-nc4.py '+tas.replace('2099','2014')+' '+tos.replace('2099','2014')+' '+sic.replace('2099','2014')+' '+sftof+'  blend-runnable/CRU.nc blend-runnable/SST.nc > data_models/'+model+'_'+run+'/had4_'+scenario+sftof_style+'_normal.txt',shell=True).wait()

		Popen('python gmt_methods/ncblendhadcrut-nc4.py '+tas.replace('2099','2014')+' '+tos.replace('2099','2014')+' '+sic.replace('2099','2014')+' '+sftof+'  ReScience/data/CRU46.nc ReScience/data/SST31.nc > data_models/'+model+'_'+run+'/had4_'+scenario+sftof_style+'_CRU46.txt',shell=True).wait()
