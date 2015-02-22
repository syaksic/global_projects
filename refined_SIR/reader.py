import matplotlib.pyplot as plt
import numpy as np
import config
from os import listdir
import os.path
from utils.utils import *
from utils import plot
import time



def Menu():
	op=config.src_Menu()
	if op==None:
		op=config.demo
	return op


def read(op=None):
	if op==None:
		op=Menu()

	SNA_results=config.src+op+'/results/'
	SIM_output=config.src+op+'/output/'
	
	SNAfiles = [ f for f in listdir(SNA_results) if os.path.isfile(os.path.join(SNA_results,f)) ]
	SIMfiles = [ f for f in listdir(SIM_output) if os.path.isfile(os.path.join(SIM_output,f)) ]
	
	
	for files in SNAfiles:
		extension = os.path.splitext(files)[1]
		if extension=='.bkp':
			data=load_bkp(SNA_results+files)
			plot.plot_evolution(data,config.src+op+'/plots/')
			time.sleep(1)
	
	
	for files in SIMfiles:
		extension = os.path.splitext(files)[1]
		if extension=='.csv':
			data=load_csv(SIM_output+files)
			plot.plot_evolution(data,config.src+op+'/plots/')
			time.sleep(1)
	
	data1=load_bkp(SNA_results+SNAfiles[0])
	data2=load_csv(SIM_output+SIMfiles[0])
	plot.plot_evolutions(data1,data2,config.src+op+'/plots/')

if __name__ == "__main__":
	read()