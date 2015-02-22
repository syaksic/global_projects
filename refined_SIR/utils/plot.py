#!/usr/bin/env python
"""
plotting functions for refined SIR model
"""
__author__ = """Sergio Yaksic <seanyabe@gmail.com>"""

import matplotlib.pyplot as plt
import matplotlib.cm as cm
import time

def plot_graph_degrees(graph,path):
	f=plt.figure()
	ax=f.add_subplot(111)
	
	plt.yscale('log')
	plt.xscale('log')
	plt.title("Degree Distribution")
	plt.ylabel("Probability")
	plt.xlabel("degree[k]")
	
	plt.plot(graph['degree']['index'],graph['degree']['Exp']['degree_dist'],'ys',label=r'Experimental $P(k)$')
	plt.plot(graph['degree']['index'],graph['degree']['Teo']['degree_dist'],'ro',label=r'Theoretical $P(k)$')
	plt.plot(graph['degree']['index'],graph['degree']['BF']['degree_dist'],'b^',label=r'Best Fit $P(k)$')

	handles, labels = ax.get_legend_handles_labels()
	plt.legend(handles, labels,loc='lower left')

	
	mng = plt.get_current_fig_manager()
	mng.resize(*mng.window.maxsize())
	now = time.strftime('%Y-%m-%d-%H-%M-%S')
	plt.savefig(path+now+'dgr_dist.eps')

def plot_graph_degree_degree(graph,path):
	f=plt.figure()
	ax=f.add_subplot(111)
	
	plt.yscale('log')
	plt.xscale('log')
	plt.title("Degree-degree uncorrelated function")
	plt.ylabel("Probability")
	plt.xlabel("degree[k]")
	
	plt.plot(graph['degree']['index'],graph['degree']['Exp']['uncorr_func'],'ys',label=r'Experimental $P(k|x)$')
	plt.plot(graph['degree']['index'],graph['degree']['Teo']['uncorr_func'],'ro',label=r'Theoretical $P(k|x)$')
	plt.plot(graph['degree']['index'],graph['degree']['BF']['uncorr_func'],'b^',label=r'Best Fit $P(k|x)$')

	handles, labels = ax.get_legend_handles_labels()
	plt.legend(handles, labels,loc='lower left')

	
	mng = plt.get_current_fig_manager()
	mng.resize(*mng.window.maxsize())
	now = time.strftime('%Y-%m-%d-%H-%M-%S')
	plt.savefig(path+now+'dgr_corr.eps')

def plot_evolution(users,path):
	Times=users['t_t']
	Ignorants=users['I_t']
	Spreaders=users['S_t']
	Retired=users['R_t']	

	fig, ax = plt.subplots()
	ax.plot(Times,Ignorants,label='Ignorants',color='green')
	ax.plot(Times,Spreaders,label='Spreaders',color='purple')
	ax.plot(Times,Retired,label='Retired',color='orange')
	
	#ax.set_yscale('log')
	#ax.set_xscale('log')
	legend = ax.legend(loc='upper right', shadow=True)
	frame = legend.get_frame()
	frame.set_facecolor('0.90')
	ax.set_title('refined SIR model')
	ax.set_xlabel('Time')
	ax.set_ylabel('Users/Total')
	for label in legend.get_texts():
		label.set_fontsize('large')
	for label in legend.get_lines():
		label.set_linewidth(1.5)
	now = time.strftime('%Y-%m-%d-%H-%M-%S')
	plt.savefig(path+now+'evolution.jpg')
	plt.close()

def plot_evolutions(users1,users2,path):
	plt.clf()
	Times=users1['t_t']
	Ignorants=users1['I_t']
	Spreaders=users1['S_t']
	Retired=users1['R_t']	

	fig, ax = plt.subplots()
	ax.plot(users1['t_t'],users1['I_t'],label='Ignorants',color='green')
	ax.plot(users1['t_t'],users1['S_t'],label='Spreaders',color='purple')
	ax.plot(users1['t_t'],users1['R_t'],label='Retired',color='orange')

	ax.plot(users2['t_t'],users2['I_t'],label='Ignorants',color='green')
	ax.plot(users2['t_t'],users2['S_t'],label='Spreaders',color='purple')
	ax.plot(users2['t_t'],users2['R_t'],label='Retired',color='orange')
	
	#ax.set_yscale('log')
	ax.set_xscale('log')
	legend = ax.legend(loc='upper right', shadow=True)
	frame = legend.get_frame()
	frame.set_facecolor('0.90')
	ax.set_title('refined SIR model')
	ax.set_xlabel('Time')
	ax.set_ylabel('Users/Total')
	for label in legend.get_texts():
		label.set_fontsize('large')
	for label in legend.get_lines():
		label.set_linewidth(1.5)
	now = time.strftime('%Y-%m-%d-%H-%M-%S')
	plt.savefig(path+now+'evolution.jpg')
	#plt.show()
	plt.close()