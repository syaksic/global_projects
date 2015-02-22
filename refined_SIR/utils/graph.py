#!/usr/bin/env python
"""
generate a graph and extract the two more basics connectivity pattern functions P(k) and P(k'|k).
"""
__author__ = """Sergio Yaksic <seanyabe@gmail.com>"""
from __init__ import *
import networkx as nx
from scipy.optimize import curve_fit
import json

def degree_dist_fit(x, a, b):
    return pow(x,-a)*b

def degree_degree_cor_func_fit(x, a, b, c):
	return (x*pow(x,-a)*b)*(1/c)

def savejson(G, fname):
    json.dump(dict(nodes=[[n, G.node[n]] for n in G.nodes()],
                   edges=[[u, v, G.edge[u][v]] for u,v in G.edges()]),
              open(fname, 'w'), indent=2)

def loadjson(fname):
    G = nx.Graph()
    d = json.load(open(fname))
    G.add_nodes_from(d['nodes'])
    G.add_edges_from(d['edges'])
    return G

def loadtest(fname):
	G = nx.read_gpickle(fname)
	return G

def savegplickle(G, fname):
	nx.write_gpickle(G,fname)
	return fname

def generate_graph(name,size):
	Graph=nx.barabasi_albert_graph(size,3)
	fname=name+'.json'
	savejson(Graph,fname)
	nx.write_gml(Graph, name+'.gml')
	fname=name+'.gpickle'
	savegplickle(Graph,fname)
	return fname,Graph

def degree_dist(degree_sequence,graph_size):
	prob=[]
	index=[]
	count=[]
	kmean=0.0

	for i in range(len(degree_sequence)):
		if degree_sequence[i]>0:
			value=float(degree_sequence[i])/graph_size
			prob.append(np.float64(value))
			index.append(i)
			count.append(degree_sequence[i])
			kmean+=value*i
	popt, pcov = curve_fit(degree_dist_fit, index, prob)
	bf=degree_dist_fit(index,popt[0],popt[1])
	teo=degree_dist_fit(index,np.float64(3.0),np.float64(kmean*kmean))
	return{'index':index,'count':count,'prob':prob, 'popt':popt,'kmean':kmean,'bf':bf,'teo':teo}

def degree_corr(indices,counts,Graph,kmean):
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
	teo=degree_degree_cor_func_fit(indices,np.float64(3.0),np.float64(kmean*kmean),np.float64(kmean))
	bf=degree_degree_cor_func_fit(indices,popt[0],popt[1],popt[2])
	return {'assortativity':assortativity,'uncorrelated_prob':uncorrelated_prob,'dgr_dgr_func':dgr_dgr_func,'popt':popt,'bf':bf,'teo':teo}
