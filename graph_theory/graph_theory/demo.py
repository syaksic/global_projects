#!/usr/bin/env python
"""
demo for graph_theory
"""
__author__ = """Sergio Yaksic <seanyabe@gmail.com>"""
from graph_utils import *

# This module have some demos that explain how to use graph_utils
def maindemo(graph_size,filename,path):
	print('Welcome to graph_utils[demo]')
	print('I will do the following tricks:')
	print('1. Create a barabasi_albert_graph of size '+str(graph_size))
	print('Under observations of prof. J.C. Losada each node will be connected to 3 previously added nodes')
	Graph = nx.barabasi_albert_graph(graph_size,3) 
	print('1. Create a barabasi_albert_graph of size '+str(graph_size)+' ...DONE')
	print('2. Extract the degree histogram')
	degree_sequence=nx.degree_histogram(Graph)
	print('2. Extract the degree histogram ...DONE')
	print('3. Calculate the Degree distribution')
	degree_distribution=degree_dist(degree_sequence,graph_size)
	print('3. Calculate the Degree distribution ...DONE')
	print('4. Calculate the Degree correlations ')
	degree_correlations=degree_corr(degree_distribution['index'],degree_distribution['count'],Graph)
	print('4. Calculate the Degree distribution ...DONE')
	print('5. Saving data')
	with open(path+'degree_distribution'+filename, 'w') as f:	
		pickle.dump(degree_distribution, f)
	with open(path+'degree_correlations'+filename, 'w') as f:	
		pickle.dump(degree_correlations, f)
	print('5. Saving data ...DONE')

def showdemo(path,filename,PlotOptions=None):
	if PlotOptions==None:
		PlotOptions={'log-log':True,'text':True,'assortativity':True,'degree_dist':True,'degree_dist_teo':False,'degree_correlations':False,'uncorrelated_prob':True,'teo_fit':False,'exp_fit':False}
	print('Welcome to graph_utils')
	print('I will do the following tricks:')
	print('1. Load data '+path+filename)
	with open(path+'degree_distribution'+filename, 'rb') as f:
		degree_distribution=pickle.load(f)
	with open(path+'degree_correlations'+filename, 'rb') as f:
		degree_correlations=pickle.load(f)
	print('1. Load data '+filename+' ...DONE')
	print('2. Plotting data')
	show(degree_distribution,degree_correlations,PlotOptions)

def plotdemo(path,filename,PlotOptions=None):
	if PlotOptions==None:
		PlotOptions={'log-log':True,'text':True,'assortativity':True,'degree_dist':True,'degree_dist_teo':False,'degree_correlations':False,'uncorrelated_prob':True,'teo_fit':False,'exp_fit':False}
	with open(path+'degree_distribution'+filename, 'rb') as f:
		degree_distribution=pickle.load(f)
	with open(path+'degree_correlations'+filename, 'rb') as f:
		degree_correlations=pickle.load(f)
	plot(degree_distribution,degree_correlations,PlotOptions,path,filename)

def generatordemo(filename,count,path,graph_size):
	mean_degree_sequence = [0.0] * graph_size
	
	for n in range(0,count):
		Graph = nx.barabasi_albert_graph(graph_size,3) 
		degree_sequence=nx.degree_histogram(Graph)
		for i in range(len(degree_sequence)):
			if i>3:
				mean_degree_sequence[i]+=float(degree_sequence[i])/count
	mean_degree_distribution=degree_dist(mean_degree_sequence,graph_size)
	
	last_degree_distribution=degree_dist(degree_sequence,graph_size)
	last_degree_correlations=degree_corr(last_degree_distribution['index'],last_degree_distribution['count'],Graph)
	
	with open(path+'degree_distribution'+filename, 'w') as f:	
		pickle.dump(mean_degree_distribution, f)
	with open(path+'degree_correlations'+filename, 'w') as f:	
		pickle.dump(last_degree_correlations, f)




