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


def plot_maps(**kwargs):
	print(kwargs)

	if 'time_steps' not in kwargs.keys():
		data=[]
		for file,var in zip(kwargs['files'],kwargs['var_names']):
			data.append(da.read_nc(file)[var].ix[:,:].squeeze())

	elif 'levels' not in kwargs.keys():
		data=[]
		for file,var,t in zip(kwargs['files'],kwargs['var_names']),kwargs['time_steps']:
			data.append(da.read_nc(file)[var].ix[t,:,:].squeeze())

	else:
		data=[]
		for file,var,t,l in zip(kwargs['files'],kwargs['var_names'],kwargs['time_steps'],kwargs['levels']):
			data.append(da.read_nc(file)[var].ix[t,l,:,:].squeeze())

	ext=kwargs['extend']
	asp=(ext[1]-ext[0])/float(ext[3]-ext[2])

	plt.close('all')
	plate_carree = ccrs.PlateCarree()

	if 'nrows' in kwargs.keys():
		nrows=kwargs['nrows']
		ncols=len(data)/nrows
	else:
		nrows=1
		ncols=len(data)/nrows

	print((3*asp*len(data)/nrows,3*nrows))
	fig,axes = plt.subplots(nrows=nrows,ncols=ncols+1,figsize=(3*asp*len(data)/nrows,3*nrows),subplot_kw={'projection': plate_carree},gridspec_kw = {'width_ratios':[3]*ncols+[1]})
	print(axes,axes.shape)
	if len(axes.shape)==1: axes=np.expand_dims(axes, axis=0)
	print(axes,axes.shape)
	for ax,i in zip(axes[:,:-1].flatten()[:len(data)],range(len(data))):
		ax.set_global()
		ax.coastlines(edgecolor='black')
		ax.axis('off')
		ax.set_extent(ext,crs=plate_carree)

		xx,yy=data[i].lon.copy(),data[i].lat.copy()
		x_step,y_step=np.diff(xx,1).mean(),np.diff(yy,1).mean()
		xx=np.append(xx-x_step*0.5,xx[-1]+x_step*0.5)
		yy=np.append(yy-y_step*0.5,yy[-1]+y_step*0.5)
		lons,lats=np.meshgrid(xx,yy)
		im=ax.pcolormesh(lons,lats,data[i],vmin=kwargs['color_range'][0],vmax=kwargs['color_range'][1],cmap=plt.cm.jet);
		ax.set_title(kwargs['titles'][i])
		#ax.annotate(season+'\n'+dataset, xy=(0.02, 0.05), xycoords='axes fraction', fontsize=9,fontweight='bold')

	for ax in axes[:,-1]:
		ax.axis('off')
		ax.outline_patch.set_edgecolor('white')

	cbar_ax=fig.add_axes([ncols/float(ncols+1.33),0.2,1/float(ncols+1.33),0.6])
	cbar_ax.axis('off')
	cb=fig.colorbar(im,orientation='vertical',label=kwargs['label'],ax=cbar_ax)

	#plt.suptitle('mean persistence', fontweight='bold')
	fig.tight_layout()
	plt.savefig(kwargs['outfile'],dpi=300)


if __name__=='__main__':
	'''
	example call:
	python ReScience/plots_map_samples.py --extend -40 0 50 70 -f1 data_models/EC-EARTH_r1i1p1/tos.nc -f2 data_models/rcp85-xxx_rcp85_EC-EARTH_r1i1p1/tos.nc -of ReScience/figures/test.png -v1 tos -cr 270 300 -t1 "nan treatment" -t2 "naive" -l "tos [K]"
	'''

	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('--file1','-f1',help='file1',required=True)
	parser.add_argument('--var_name1','-v1',help='var name in file 1',required=True)
	parser.add_argument('--file2','-f2',help='file2',required=True)
	parser.add_argument('--var_name2','-v2',help='var name in file 2 -default is the same as in file one',default=None)

	parser.add_argument('--title1','-t1' ,help='title of subplot 1',default='--title1 -t1')
	parser.add_argument('--title2','-t2' ,help='title of subplot 2',default='--title2 -t2')

	parser.add_argument('--outfile','-of',help='outfile',required=True)
	parser.add_argument('--time_step','-ts' ,help='time_step of plot',default=0)
	parser.add_argument('--level','-lev' ,help='level of plot',default=None)
	parser.add_argument('--extend','-ext' ,help='xmin xmax ymin ymax',nargs='+',type=np.int,default=[-180,180,-90,90])
	parser.add_argument('--color_range','-cr' ,help='min max',nargs='+',type=np.int,default=[0,1])
	parser.add_argument('--label','-l' ,help='color bar label',default='--label -l')

	args = parser.parse_args()

	if args.var_name2 is None:
		args.var_name2=args.var_name1

	arguments={
		'file1':args.file1,
		'file2':args.file2,
		'var_name1':args.var_name1,
		'var_name2':args.var_name2,
		'title1':args.title1,
		'title2':args.title2,
		'outfile':args.outfile,
		'time_step':args.time_step,
		'level':args.level,
		'extend':args.extend,
		'color_range':args.color_range,
		'label':args.label,
	}

	if args.time_step is not None:	arguments['time_step']=args.time_step
	if args.level is not None:	arguments['level']=args.level

	plot_maps(**arguments)
