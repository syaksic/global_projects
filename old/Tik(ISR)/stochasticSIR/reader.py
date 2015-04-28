import matplotlib.pyplot as plt
import numpy as np
import config
from os import listdir
import os.path
from utils.utils import *
from utils import plot
from utils import inform
import time
import shutil



def Menu():
	op=config.src_Menu()
	if op==None:
		op=config.demo
	return op


def read(op=None):
	if op==None:
		op=Menu()

	graph=load_dic(config.src+op+'/graph.pkl')
	print(graph['degree']['k_mean'])

	SNA_results=config.src+op+'/results/'
	SIM_output=config.src+op+'/output/'
	
	SNAfiles = [ f for f in listdir(SNA_results) if os.path.isfile(os.path.join(SNA_results,f)) ]
	SIMfiles = [ f for f in listdir(SIM_output) if os.path.isfile(os.path.join(SIM_output,f)) ]
	

	
	data1=load_bkp(SNA_results+SNAfiles[0])
	plot.plot_spreaders(data1,graph,config.src+op+'/plots/')
	data2=load_csv(SIM_output+SIMfiles[0])
	plot.plot_evolutions(data1,data2,config.src+op+'/plots/')
	
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

	Inform_output=config.src+op+'/inform/'
	if not os.path.exists(Inform_output):
	    os.makedirs(path+'inform')
	
	if not os.path.exists(Inform_output+'/latex'):
	    os.makedirs(Inform_output+'/latex')
	shutil.copy2('./templates/Formato_Propuesta_Tesis_Doctorado.bib', Inform_output+'/latex/Formato_Propuesta_Tesis_Doctorado.bib')
	latex=Inform_output+'/latex/inform.tex'
	inform.create_latex(latex)
	inform.add_tittle(latex,op)
	inform.add_Author(latex,['Sergio Yaksic','Werner Creixell','Juan Carlos Lozada'])
	inform.add_Abstract(latex)
	with open('./templates/intro.tex') as f:
		intro = f.read()
	inform.add_Introduction(latex,intro)
	with open('./templates/background.tex') as f:
		back = f.read()
	inform.add_Background(latex,back)
	with open('./templates/Metodology.tex') as f:
		meto = f.read()
	inform.add_Background(latex,meto)
	with open('./templates/Results.tex') as f:
		resu = f.read()
	inform.add_Background(latex,resu)
	
if __name__ == "__main__":
	read()