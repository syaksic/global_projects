#!/usr/bin/env python
"""
generate a graph and extract the two more basics connectivity pattern functions P(k) and P(k'|k).
"""
__author__ = """Sergio Yaksic <seanyabe@gmail.com>"""
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import os.path
from scipy.optimize import curve_fit
import pickle
import sys
import matplotlib.cm as cm
import math
#######################################################################################################################################
#######################################################################################################################################
########################  _____  _       _      __                  _   _                 #############################################
######################## |  __ \| |     | |    / _|                | | (_)                #############################################
######################## | |__) | | ___ | |_  | |_ _   _ _ __   ___| |_ _  ___  _ __  ___ #############################################
######################## |  ___/| |/ _ \| __| |  _| | | | '_ \ / __| __| |/ _ \| '_ \/ __|#############################################
######################## | |    | | (_) | |_  | | | |_| | | | | (__| |_| | (_) | | | \__ \#############################################
######################## |_|    |_|\___/ \__| |_|  \__,_|_| |_|\___|\__|_|\___/|_| |_|___/#############################################
########################                                                                  #############################################
########################                                                                  #############################################
#######################################################################################################################################
#######################################################################################################################################	

def show(degree_distribution,degree_correlations,PlotOptions):
	f=plt.figure()
	ax=f.add_subplot(111)
	
	if PlotOptions['log-log']:
		plt.yscale('log')
	plt.xscale('log')
	plt.title("Connectivity patterns")
	plt.ylabel("P(k|x)")
	plt.xlabel("degree[k]")

	
	popt=degree_distribution['popt']
	popt2=degree_correlations['popt']

	c=str(round(popt[1],3))
	gamma=str(round(popt[0],3))

	
	if PlotOptions['text']:	
		plt.text(0.20, 0.37,r'$P(k|x)=\frac{k Ck^{-\gamma}}{\langle k\rangle}$',fontsize=20, ha='center', va='center', transform=ax.transAxes)
		plt.text(0.20, 0.30,r'$P(k)=Ck^{-\gamma}$',fontsize=20, ha='center', va='center', transform=ax.transAxes)
		plt.text(0.20, 0.21, r'$C='+c+'$',fontsize=20, ha='center', va='center', transform=ax.transAxes)
		plt.text(0.20, 0.14, r'$\gamma='+gamma+'$',fontsize=20, ha='center', va='center', transform=ax.transAxes)
	if PlotOptions['assortativity']:
		plt.text(0.75, 0.90, r'$Assortativity='+str(degree_correlations['assortativity'])+'$',fontsize=20, ha='center', va='center', transform=ax.transAxes)

	if PlotOptions['degree_dist']:
		plt.plot(degree_distribution['index'],degree_distribution['prob'],'ys',label=r'$P(k)Exp$')
	
	if PlotOptions['degree_dist_teo']:
		plt.plot(degree_distribution['index'],degree_dist_fit(degree_distribution['index'],popt[0],popt[1]),label=r'$P(k) Best Fit$')
		teo=[0.0]*len(degree_distribution['index'])
		for i in range(len(degree_distribution['index'])):
			teo[i]=pow(degree_distribution['index'][i],-3.0)*pow(degree_distribution['kmean'],2)
		plt.plot(degree_distribution['index'],teo,label=r'$P(k)Teo$')	
	if PlotOptions['degree_correlations']:
		cmap = plt.get_cmap('rainbow')
		m = cm.ScalarMappable(cmap=cmap)
		m.set_array(degree_distribution['index'])	
		colorbar=plt.colorbar(m)
		colorbar.set_label('degree class x')
		for indices in degree_distribution['index']:
			plt.plot(degree_distribution['index'],degree_correlations['dgr_dgr_func'][indices],'.',color=m.to_rgba(indices))
	
	if PlotOptions['uncorrelated_prob']:
		plt.plot(degree_distribution['index'],degree_correlations['uncorrelated_prob'],'y.',label=r'$P(k|x) Uncorrelated$')
	
	if PlotOptions['teo_fit']:
		teo2=[0.0]*len(degree_distribution['index'])
		for i in range(len(degree_distribution['index'])):
			teo2[i]=pow(degree_distribution['index'][i],-3.0)*degree_distribution['kmean']*degree_distribution['index'][i]

		plt.plot(degree_distribution['index'],teo2,label=r'$P(k|x)Teo$')
	if PlotOptions['exp_fit']:
		plt.plot(degree_distribution['index'],degree_degree_cor_func_fit(degree_distribution['index'],popt2[0],popt2[1],popt2[2]),label=r'$P(k|x) Best Fit$')

	
	
	handles, labels = ax.get_legend_handles_labels()
	plt.legend(handles, labels,loc='center right')

	
	mng = plt.get_current_fig_manager()
	mng.resize(*mng.window.maxsize())
	plt.show()

def plot(degree_distribution,degree_correlations,PlotOptions,path,filename):
	f=plt.figure()
	ax=f.add_subplot(111)
	
	if PlotOptions['log-log']:
		plt.yscale('log')
	plt.xscale('log')
	plt.title("Connectivity patterns")
	plt.ylabel("P(k) or P(k|x)")
	plt.xlabel("degree[k]")

	
	popt=degree_distribution['popt']
	popt2=degree_correlations['popt']

	c=str(round(popt[1],3))
	gamma=str(round(popt[0],3))

	
	if PlotOptions['text']:	
		plt.text(0.25, 0.37,r'$P(k|x)=\frac{k Ck^{-\gamma}}{\langle k\rangle}$',fontsize=20, ha='center', va='center', transform=ax.transAxes)
		plt.text(0.25, 0.30,r'$P(k)=Ck^{-\gamma}$',fontsize=20, ha='center', va='center', transform=ax.transAxes)
		plt.text(0.25, 0.21, r'$C='+c+'$',fontsize=20, ha='center', va='center', transform=ax.transAxes)
		plt.text(0.25, 0.14, r'$\gamma='+gamma+'$',fontsize=20, ha='center', va='center', transform=ax.transAxes)
	if PlotOptions['assortativity']:
		plt.text(0.25, 0.07, r'$Assortativity='+str(degree_correlations['assortativity'])+'$',fontsize=20, ha='center', va='center', transform=ax.transAxes)

	if PlotOptions['degree_dist']:
		plt.plot(degree_distribution['index'],degree_distribution['prob'],'ys',label=r'$P(k)Exp$')
	if PlotOptions['degree_dist_teo']:
		plt.plot(degree_distribution['index'],degree_dist_fit(degree_distribution['index'],popt[0],popt[1]),label=r'$P(k)Teo$')
		teo=[0.0]*len(degree_distribution['index'])
		for i in range(len(degree_distribution['index'])):
			teo[i]=pow(degree_distribution['index'][i],-3.0)*pow(degree_distribution['kmean'],2)
		plt.plot(degree_distribution['index'],teo,label=r'$P(k)Teo,\gamma=3.0$')	
	if PlotOptions['degree_correlations']:
		cmap = plt.get_cmap('rainbow')
		m = cm.ScalarMappable(cmap=cmap)
		m.set_array(degree_distribution['index'])	
		colorbar=plt.colorbar(m)
		colorbar.set_label('degree class x')
		for indices in degree_distribution['index']:
			plt.plot(degree_distribution['index'],degree_correlations['dgr_dgr_func'][indices],'.',color=m.to_rgba(indices))
	
	if PlotOptions['uncorrelated_prob']:
		plt.plot(degree_distribution['index'],degree_correlations['uncorrelated_prob'],'.',label=r'$UC P(k|x)$')
	
	if PlotOptions['teo_fit']:
		plt.plot(degree_distribution['index'],degree_degree_cor_func_fit(degree_distribution['index'],popt[0],popt[1],degree_distribution['kmean']),label=r'$P(k|x)Teo$')
	if PlotOptions['exp_fit']:
		plt.plot(degree_distribution['index'],degree_degree_cor_func_fit(degree_distribution['index'],popt2[0],popt2[1],popt2[2]),label=r'$P(k|x)Exp$')

	
	
	handles, labels = ax.get_legend_handles_labels()
	plt.legend(handles, labels,loc='center right')

	
	mng = plt.get_current_fig_manager()
	mng.resize(*mng.window.maxsize())
	plt.savefig(path+filename+'.eps')
	
#######################################################################################################################################
#######################################################################################################################################
########################  _____                              __                  _   _                 ################################
######################## |  __ \                            / _|                | | (_)                ################################
######################## | |  | | ___  __ _ _ __ ___  ___  | |_ _   _ _ __   ___| |_ _  ___  _ __  ___ ################################
######################## | |  | |/ _ \/ _` | '__/ _ \/ _ \ |  _| | | | '_ \ / __| __| |/ _ \| '_ \/ __|################################
######################## | |__| |  __/ (_| | | |  __/  __/ | | | |_| | | | | (__| |_| | (_) | | | \__ \################################
######################## |_____/ \___|\__, |_|  \___|\___| |_|  \__,_|_| |_|\___|\__|_|\___/|_| |_|___/################################
########################               __/ |                                                           ################################
########################              |___/  														   ################################
#######################################################################################################################################
#######################################################################################################################################	

def degree_dist_fit(x, a, b):
    return pow(x,-a)*b

def degree_degree_cor_func_fit(x, a, b, c):
	return (x*pow(x,-a)*b)*(1/c)



def degree_dist(degree_sequence,graph_size):
	prob=[]
	index=[]
	count=[]
	kmean=0.0

	for i in range(len(degree_sequence)):
		if degree_sequence[i]>0:
			value=float(degree_sequence[i])/graph_size
			prob.append(value)
			index.append(i)
			count.append(degree_sequence[i])
			kmean+=value*i
	popt, pcov = curve_fit(degree_dist_fit, index, prob)
	return{'index':index,'count':count,'prob':prob, 'popt':popt,'kmean':kmean}


def degree_corr(indices,counts,Graph):
	dgr_dgr={}
	dgr_dgr_func={}
	bins=[]
	degrees=[]
	uncorrelated_prob=[]
	for index in indices:
		dgr_dgr.update({index:[]})
		bins.append(index)
	bins.append(bins[-1]+1)


	for links in Graph.edges():
		dgr_dgr[Graph.degree(links[0])].append(Graph.degree(links[1]))
		dgr_dgr[Graph.degree(links[1])].append(Graph.degree(links[0]))
		degrees.append(Graph.degree(links[1]))
		degrees.append(Graph.degree(links[0]))
	
	for x in range(len(dgr_dgr)):
		k=indices[x]
		hist=np.histogram(dgr_dgr[k],bins)
		p=[]
		count=counts[x]*k
		for items in hist[0]:
			p.append(float(items)/count)
		dgr_dgr_func.update({k:p})

	hist=np.histogram(degrees,bins)
	count=len(degrees)
	for items in hist[0]:
		uncorrelated_prob.append(float(items)/count)

	popt, pcov = curve_fit(degree_degree_cor_func_fit, indices, uncorrelated_prob)
	assortativity=nx.degree_assortativity_coefficient(Graph)

	return {'assortativity':assortativity,'uncorrelated_prob':uncorrelated_prob,'dgr_dgr_func':dgr_dgr_func,'popt':popt}

#######################################################################################################################################
#######################################################################################################################################
#######################################################################################################################################
#######################################################################################################################################
#######################################################################################################################################
#######################################################################################################################################
#######################################################################################################################################
#######################################################################################################################################
#######################################################################################################################################
#######################################################################################################################################
#######################################################################################################################################	
#######################################################################################################################################