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
import simplejson as json

###########################################################################
#Fit functions
###########################################################################

def degree_dist_fit(x, a, b):
    return pow(x,-a)*b

def degree_dist_fit2(x, a, b, c):
	return (x*pow(x,-a)*b)*(1/c)

###########################################################################
#Plot functions
###########################################################################

def plot_info(degree_distribution,name,Graph=None):
	f=plt.figure()
	ax=f.add_subplot(111)
	
	#plt.yscale('log')
	plt.xscale('log')
	plt.title("Connectivity patterns")
	plt.ylabel("P(k) or P(k|x)")
	plt.xlabel("degree[k]")

	cmap = plt.get_cmap('rainbow')
	m = cm.ScalarMappable(cmap=cmap)
	m.set_array(degree_distribution['index'])	
	#colorbar=plt.colorbar(m)
	#colorbar.set_label('degree class x')
	
	
	size=str(degree_distribution['size'])
	links=str(degree_distribution['links'])
	k_mean=str(degree_distribution['kmean'])
	k_max=str(degree_distribution['kmax'])
	k_min=str(degree_distribution['kmin'])
	kmin=degree_distribution['kmin']
	kmax=degree_distribution['kmax']
	popt=degree_distribution['popt']
	popt2=degree_distribution['popt2']
	kmean=round(degree_distribution['kmean'])

	plt.text(0.4, 0.90, r'$Nodes='+size+'$',fontsize=20, ha='center', va='center', transform=ax.transAxes)
	plt.text(0.4, 0.83, r'$Links='+links+'$',fontsize=20, ha='center', va='center', transform=ax.transAxes)
	
	plt.text(0.8, 0.90, r'$\langle k\rangle='+k_mean+'$',fontsize=20, ha='center', va='center', transform=ax.transAxes)
	plt.text(0.8, 0.83, r'$k_{min}='+k_min+'$',fontsize=20, ha='center', va='center', transform=ax.transAxes)
	plt.text(0.8, 0.76, r'$k_{max}='+k_max+'$',fontsize=20, ha='center', va='center', transform=ax.transAxes)


	c=str(round(popt[1],3))
	gamma=str(round(popt[0],3))
	plt.text(0.85, 0.30,r'$P(k|x)=\frac{k Ck^{-\gamma}}{\langle k\rangle}$',fontsize=20, ha='center', va='center', transform=ax.transAxes)
	plt.text(0.85, 0.21,r'$P(k)=Ck^{-\gamma}$',fontsize=20, ha='center', va='center', transform=ax.transAxes)
	plt.text(0.85, 0.14, r'$C='+c+'$',fontsize=20, ha='center', va='center', transform=ax.transAxes)
	plt.text(0.85, 0.07, r'$\gamma='+gamma+'$',fontsize=20, ha='center', va='center', transform=ax.transAxes)

	plt.plot(degree_distribution['index'],degree_distribution['prob'],'ys',label=r'$P(k)Exp$')
	plt.plot(degree_distribution['index'],degree_dist_fit(degree_distribution['index'],popt[0],popt[1]),label=r'$P(k)Teo$')
	
	#for indices in degree_distribution['index']:
	#	if (kmin<=indices) and (indices<=kmax):
	#		plt.plot(degree_distribution['index'],degree_distribution['dgr_dgr_func'][indices],'.',color=m.to_rgba(indices))
	
	#plt.plot(degree_distribution['index'],degree_distribution['uncorrelated_prob'],'.',label=r'$UC P(k|x)$')
	
	#plt.plot(degree_distribution['index'],degree_distribution['dgr_dgr_func'][degree_distribution['kmax']],'r^',label=r'$P(k|k_{max})$')
	#plt.plot(degree_distribution['index'],degree_distribution['dgr_dgr_func'][degree_distribution['kmin']],'b^',label=r'$P(k|k_{min})$')
	#if kmean in degree_distribution['dgr_dgr_func']:
	#	plt.plot(degree_distribution['index'],degree_distribution['dgr_dgr_func'][kmean],'y^',label=r'$P(k|\langle k\rangle)$')

	#plt.plot(degree_distribution['index'],degree_dist_fit2(degree_distribution['index'],popt[0],popt[1],degree_distribution['kmean']),label=r'$P(k|x)Teo$')
	#plt.plot(degree_distribution['index'],degree_dist_fit2(degree_distribution['index'],popt2[0],popt2[1],popt2[2]),label=r'$P(k|x)Exp$')

	
	
	handles, labels = ax.get_legend_handles_labels()
	plt.legend(handles, labels,loc='center right')


	print(degree_distribution['assortativity'])
	print(degree_distribution['average_clustering'])
	plt.savefig(name+"degree_histogram.png")
	plt.show()
	

def degree_func(indices,counts,Graph):
	dgr_dgr={}
	dgr_dgr_func={}
	bins=[]
	degrees=[]
	prob=[]
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
	print(count,Graph.number_of_edges())
	for items in hist[0]:
		prob.append(float(items)/count)

	return (dgr_dgr_func,prob)

def degree_dist(degree_sequence,Graph):
	prob=[]
	index=[]
	count=[]
	kmean=0.0
	graph_size=Graph.number_of_nodes()

	for i in range(len(degree_sequence)):
		if degree_sequence[i]>0:
			value=float(degree_sequence[i])/graph_size
			prob.append(value)
			index.append(i)
			count.append(degree_sequence[i])
			kmean+=value*i

	popt, pcov = curve_fit(degree_dist_fit, index, prob)
	kmax=max(index)
	kmin=min(index)
	links=graph_size*kmean

	dgr_dgr_func,uncorrelated_prob=degree_func(index,count,Graph)

	popt2, pcov2 = curve_fit(degree_dist_fit2, index, uncorrelated_prob)
	average_clustering=nx.average_clustering(Graph)
	assortativity=nx.degree_assortativity_coefficient(Graph)
	#average_shortest_path_length=nx.average_shortest_path_length(Graph)
	return {'prob':prob,'uncorrelated_prob':uncorrelated_prob,'index':index, 'count':count,'dgr_dgr_func':dgr_dgr_func,'kmean':kmean,'kmax':kmax,'kmin':kmin,'popt':popt,'popt2':popt2, 'size':graph_size,'links':int(links),'average_clustering':average_clustering,'assortativity':assortativity}

def save(G, fname):
    json.dump(dict(nodes=[[n, G.node[n]] for n in G.nodes()],
                   edges=[[u, v, G.edge[u][v]] for u,v in G.edges()]),
              open(fname, 'w'), indent=2)

def load(fname):
    G = nx.DiGraph()
    d = json.load(open(fname))
    G.add_nodes_from(d['nodes'])
    G.add_edges_from(d['edges'])
    return G


def demo():
	print('Hola :D')
	#Revisamos si existe un backup
	if os.path.isfile("./saves/barabasi_albert_graph(100000,3)degree_distribution.bkp2"):
		with open('./saves/barabasi_albert_graph(100000,3)degree_distribution.bkp', 'rb') as f:
			degree_distribution=pickle.load(f)
		print('encontre un degree_distribution.bkp... asi que lo mostrare en pantalla :D')
		plot_info(degree_distribution,'no_name')
	else: 
		Graph = nx.barabasi_albert_graph(1000,3)
		print('OK... no me entregaste parametros y no existen los backups... decidi crear un grafo '+Graph.name)
		nx.write_gml(Graph,'./saves/'+Graph.name+'.gml')
		print('Si deseas utilizar el grafo, he guardado una copia en la carpeta "saves" con nombre '+Graph.name+'.gml')
		degree_sequence=nx.degree_histogram(Graph)
		degree_distribution=degree_dist(degree_sequence,Graph)
		with open('./saves/'+Graph.name+'degree_distribution.bkp', 'w') as f:	
			pickle.dump(degree_distribution, f)
		print('Para que no sea necesario cargar el grafo nuevamente, he almacenado la siguiente informacion:degree_distribution.bkp')
		plot_info(degree_distribution,'no_name')
	save(Graph,'test.json')
	
demo()
	