#!/usr/bin/env python
"""
Stochastic Numerical Approach for refined SIR model
"""
__author__ = """Sergio Yaksic <seanyabe@gmail.com>"""
from __init__ import *
from plot import *
import time
import random


def start(graph,inputs):
	results={}
	initial=inputs['initial']
	results['rates']={
			'accepting_rate':inputs['rates']['lambda']*(1-inputs['probabilities']['beta']),
			'reffusing_rate':inputs['rates']['lambda']*(inputs['probabilities']['beta']),
			'stifling_rate':inputs['rates']['lambda']*(inputs['probabilities']['alpha']),
			'persuading_rate':inputs['rates']['lambda']*(1-inputs['probabilities']['eta']),
			'forgetting_rate':inputs['rates']['delta'],
			'remembering_rate':inputs['rates']['xi']
			}
	results['users']={
			't_t':[0],
			'Theta_k':[0],
			'I_t':[initial['I0']],
			'S_t':[initial['S0']],
			'R_t':[initial['R0']]
			}
	results['iterations']={
			'I_k_t':list(graph['degree']['count']),
			'S_k_t':[0]*len(graph['degree']['count']),
			'R_k_t':[0]*len(graph['degree']['count'])
			}
	for s in range(initial['S0']):
		k=random.randint(0,len(graph['degree']['index'])-1)
		while results['iterations']['I_k_t'][k]==0:
			k=random.randint(0,len(graph['degree']['index'])-1)
		results['iterations']['I_k_t'][k]-=1
		results['iterations']['S_k_t'][k]+=1
	for r in range(initial['R0']):
		k=random.randint(0,len(graph['degree']['index'])-1)
		while results['iterations']['I_k_t'][k]==0:
			k=random.randint(0,len(graph['degree']['index'])-1)
		results['iterations']['I_k_t'][k]-=1
		results['iterations']['R_k_t'][k]+=1
	results['users']['S_t_min']=[results['iterations']['S_k_t'][0]]
	results['users']['S_t_max']=[results['iterations']['S_k_t'][-1]]
	results['users']['S_t_big']=[results['iterations']['S_k_t'][-3]]
	results['users']['S_t_mean']=[results['iterations']['S_k_t'][3]]
	weights={}
	weights['W_IS_k']=[np.float64(0.0)]*len(graph['degree']['index'])
	weights['W_IR_k']=[np.float64(0.0)]*len(graph['degree']['index'])
	weights['W_SR_k']=[np.float64(0.0)]*len(graph['degree']['index'])
	weights['W_RS_k']=[np.float64(0.0)]*len(graph['degree']['index'])
	return results,weights

def iterate_uncorr(results,graph,weights):
	degree_dist=graph['degree']['Exp']['degree_dist']
	uncorr_func=graph['degree']['Exp']['uncorr_func']
	acum=np.float64(0.0)
	Theta_k=np.float64(0.0)
	for x in range(len(graph['degree']['index'])):
		if results['iterations']['S_k_t'][x]>0:
			Theta_k+=uncorr_func[x]*np.float64(results['iterations']['S_k_t'][x])/graph['degree']['count'][x]
	for i in range(len(graph['degree']['index'])):
		k=graph['degree']['index'][i]	
		weights['W_IS_k'][i]=results['iterations']['I_k_t'][i]*k*results['rates']['accepting_rate']*Theta_k
		weights['W_IR_k'][i]=results['iterations']['I_k_t'][i]*k*results['rates']['reffusing_rate']*Theta_k
		weights['W_SR_k'][i]=results['iterations']['S_k_t'][i]*(k*results['rates']['stifling_rate']*Theta_k+results['rates']['forgetting_rate'])
		weights['W_RS_k'][i]=results['iterations']['R_k_t'][i]*(k*results['rates']['persuading_rate']*Theta_k+results['rates']['remembering_rate'])
		acum+=weights['W_IS_k'][i]+weights['W_IR_k'][i]+weights['W_SR_k'][i]+weights['W_RS_k'][i]
	tau=1.0/acum
	r=np.random.random_sample()
	acum=np.float64(0.0)
	for k in range(len(graph['degree']['index'])):
		acum+=weights['W_IS_k'][k]
		if r<acum*tau:
			results['iterations']['I_k_t'][k]-=1
			results['iterations']['S_k_t'][k]+=1
			break
		acum+=weights['W_IR_k'][k]
		if r<acum*tau:
			results['iterations']['I_k_t'][k]-=1
			results['iterations']['R_k_t'][k]+=1
			break
		acum+=weights['W_SR_k'][k]
		if r<acum*tau:
			results['iterations']['S_k_t'][k]-=1
			results['iterations']['R_k_t'][k]+=1
			break
		acum+=weights['W_RS_k'][k]
		if r<acum*tau:
			results['iterations']['R_k_t'][k]-=1
			results['iterations']['S_k_t'][k]+=1
			break
	return results,tau,Theta_k

def iterate_corr(results,graph,weights):
	degree_dist=graph['degree']['Exp']['degree_dist']
	corr_func=graph['degree']['Exp']['corr_func']
	total=graph['nodes']
	acum=np.float64(0.0)
	for i in range(len(graph['degree']['index'])):
		k=graph['degree']['index'][i]
		Theta_k=np.float64(0.0)
		for x in range(len(graph['degree']['index'])):
			if results['iterations']['S_k_t'][x]>0:
				Theta_k+=corr_func[k][x]*results['iterations']['S_k_t'][x]/total
		weights['W_IS_k'][i]=degree_dist[i]*k*results['rates']['accepting_rate']*results['iterations']['I_k_t'][i]*Theta_k
		weights['W_IR_k'][i]=degree_dist[i]*k*results['rates']['reffusing_rate']*results['iterations']['I_k_t'][i]*Theta_k
		weights['W_SR_k'][i]=degree_dist[i]*(graph['degree']['index'][i]*results['rates']['stifling_rate']*results['iterations']['S_k_t'][i]*Theta_k+results['rates']['forgetting_rate']*np.float64(results['iterations']['S_k_t'][i])/total)
		weights['W_RS_k'][i]=degree_dist[i]*(graph['degree']['index'][i]*results['rates']['persuading_rate']*results['iterations']['R_k_t'][i]*Theta_k+results['rates']['remembering_rate']*np.float64(results['iterations']['R_k_t'][i])/total)
		acum+=weights['W_IS_k'][i]+weights['W_IR_k'][i]+weights['W_SR_k'][i]+weights['W_RS_k'][i]
	tau=1.0/acum
	r=np.random.random_sample()
	acum=np.float64(0.0)
	for k in range(len(graph['degree']['index'])):
		acum+=weights['W_IS_k'][k]
		if r<acum*tau:
			results['iterations']['I_k_t'][k]-=1
			results['iterations']['S_k_t'][k]+=1
			break
		acum+=weights['W_IR_k'][k]
		if r<acum*tau:
			results['iterations']['I_k_t'][k]-=1
			results['iterations']['R_k_t'][k]+=1
			break
		acum+=weights['W_SR_k'][k]
		if r<acum*tau:
			results['iterations']['S_k_t'][k]-=1
			results['iterations']['R_k_t'][k]+=1
			break
		acum+=weights['W_RS_k'][k]
		if r<acum*tau:
			results['iterations']['R_k_t'][k]-=1
			results['iterations']['S_k_t'][k]+=1
			break
	return results,tau

def condition(results,maxIters):
	result=False
	if len(results['users']['t_t'])>=maxIters:
		result=True
	elif results['users']['I_t'][-1]==0 and results['users']['S_t'][-1]==0:
		result=True
	elif results['users']['S_t'][-1]==0 and (results['rates']['persuading_rate']==0.0 and results['rates']['remembering_rate']==0.0):
		result=True
	elif results['users']['I_t'][-1]==0 and (results['rates']['stifling_rate']==0.0 and results['rates']['forgetting_rate']==0.0) and (results['rates']['persuading_rate']==0.0 and results['rates']['remembering_rate']==0.0):
		result=True
	return result

def execute(graph,inputs,path):
	results,weights=start(graph,inputs)
	maxIters=inputs['MaxIter']
	spy=inputs['MaxIter']/10
	while True:
		results,duration,Theta_k=iterate_uncorr(results,graph,weights)
		#results,duration=iterate_corr(results,graph,weights)
		i_t=0
		s_t=0
		r_t=0
		t_t=results['users']['t_t'][-1]+duration
		for k in range(len(graph['degree']['index'])):
			i_t+=results['iterations']['I_k_t'][k]
			s_t+=results['iterations']['S_k_t'][k]
			r_t+=results['iterations']['R_k_t'][k]
		results['users']['Theta_k'].append(Theta_k)
		results['users']['t_t'].append(t_t)
		results['users']['I_t'].append(i_t)
		results['users']['S_t'].append(s_t)
		results['users']['S_t_min'].append(results['iterations']['S_k_t'][0])
		results['users']['S_t_max'].append(results['iterations']['S_k_t'][-1])
		results['users']['S_t_big'].append(results['iterations']['S_k_t'][-3])
		results['users']['S_t_mean'].append(results['iterations']['S_k_t'][3])
		results['users']['R_t'].append(r_t)
		if len(results['users']['t_t'])%spy==0:
			print('remaining: '+str((results['users']['I_t'][-1],results['users']['S_t'][-1],results['users']['R_t'][-1],results['users']['t_t'][-1]))+' -- '+str(100*float(len(results['users']['t_t']))/maxIters)+'%')
			print(duration)
		if condition(results,maxIters):
			print('end: '+str((results['users']['I_t'][-1],results['users']['S_t'][-1],results['users']['R_t'][-1],results['users']['t_t'][-1]))+' -- '+str(100*float(len(results['users']['t_t']))/maxIters)+'%')
			break
	#plot_evolution(results['users'],path)
	now = time.strftime('%Y-%m-%d-%H-%M-%S')
	back_up(results,path+now+'result.bkp')