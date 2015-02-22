import numpy as np
import matplotlib.pyplot as plt
import pickle
import os.path
import time
from graph_utils import *

def back_up(dictionary,filename):
	with open(filename, 'w') as f: 
		pickle.dump(dictionary, f)

def load_dir(filename):
	if os.path.isfile(filename):
		with open(filename, 'rb') as f:
			return pickle.load(f)
	else:
		return {}

def set_inputs(inputs,v_alpha,v_beta,v_eta,v_lambda,v_delta,v_xi):
	probs=inputs['probabilities']
	probs['alpha']=np.float64(v_alpha)
	probs['beta']=np.float64(v_beta)
	probs['eta']=np.float64(v_eta)
	rates=inputs['rates']
	rates['lambda']=np.float64(v_lambda)
	rates['delta']=np.float64(v_delta)
	rates['xi']=np.float64(v_xi)
	inputs['status']='READY'

def set_graph(graph):
	if graph['status']=='INIT':
		if os.path.isfile("./graphs/demo0.json"):
			Graph=load("./graphs/demo0.json")
		else:
			graph['savefile'],Graph=generate_graph('demo0',10000)
		graph['nodes']=Graph.number_of_nodes()
		graph['edges']=Graph.number_of_edges()
		graph['name']=Graph.name
		degrees=degree_dist(nx.degree_histogram(Graph),graph['nodes'])
		graph['degree']['k_mean']=degrees['kmean']
		graph['degree']['count']=degrees['count']
		graph['degree']['index']=degrees['index']
		graph['degree']['BF']['degree_dist']=degrees['bf']
		graph['degree']['Teo']['degree_dist']=degrees['teo']
		graph['degree']['Exp']['degree_dist']=degrees['prob']
		degrees_degrees=degree_corr(degrees['index'],degrees['count'],Graph,degrees['kmean'])
		graph['degree']['BF']['uncorr_func']=degrees_degrees['bf']
		graph['degree']['Teo']['uncorr_func']=degrees_degrees['teo']
		graph['degree']['Exp']['uncorr_func']=degrees_degrees['uncorrelated_prob']
		graph['degree']['Exp']['corr_func']=degrees_degrees['dgr_dgr_func']
	graph['status']='READY'

def plot(show,Times,Ignorants,Retired,Spreaders):
	fig, ax = plt.subplots()
	ax.plot(Times,Ignorants,label='Ignorants',color='green')
	ax.plot(Times,Spreaders,label='Spreaders',color='purple')
	ax.plot(Times,Retired,label='Retired',color='orange')
	
	#ax.set_yscale('log')
	#ax.set_xscale('log')
	legend = ax.legend(loc='center right', shadow=True)
	frame = legend.get_frame()
	frame.set_facecolor('0.90')
	ax.set_title('refined SIR model')
	ax.set_xlabel('Time')
	ax.set_ylabel('Users/Total')
	for label in legend.get_texts():
		label.set_fontsize('large')
	for label in legend.get_lines():
		label.set_linewidth(1.5)
	if show==True:
		plt.show()	
	else:
		now = time.strftime('%Y-%m-%d-%H-%M-%S')
		plt.savefig(now+'plot.png')
	plt.close()

def iterate_BF(users,graph,rates):
	import time
	degree_dist=graph['degree']['BF']['degree_dist']
	uncorr_func=graph['degree']['BF']['uncorr_func']
	W_IS_k=[np.float64(0.0)]*len(graph['degree']['index'])
	W_IR_k=[np.float64(0.0)]*len(graph['degree']['index'])
	W_SR_k=[np.float64(0.0)]*len(graph['degree']['index'])
	W_RS_k=[np.float64(0.0)]*len(graph['degree']['index'])
	acum=np.float64(0.0)
	for k in range(len(graph['degree']['index'])):
		Theta_k=np.float64(0.0)
		for x in range(len(graph['degree']['index'])):
			if users['s_k_t'][x]>0:
				Theta_k+=uncorr_func[x]*users['s_k_t'][x]
		aux=graph['nodes']*degree_dist[k]
		W_IS_k[k]=aux*graph['degree']['index'][k]*rates['accepting_rate']*users['i_k_t'][k]*Theta_k
		W_IR_k[k]=aux*graph['degree']['index'][k]*rates['reffusing_rate']*users['i_k_t'][k]*Theta_k
		W_SR_k[k]=aux*(graph['degree']['index'][k]*rates['stifling_rate']*users['s_k_t'][k]*Theta_k+rates['forgetting_rate']*users['s_k_t'][k])
		W_RS_k[k]=aux*(graph['degree']['index'][k]*rates['persuading_rate']*users['r_k_t'][k]*Theta_k+rates['remembering_rate']*users['r_k_t'][k])
		acum+=W_IS_k[k]+W_IR_k[k]+W_SR_k[k]+W_RS_k[k]
	tau=1.0/acum
	
	r=np.random.random_sample()
	variation=np.float64(1.0/graph['nodes'])
	acum=np.float64(0.0)
	for k in range(len(graph['degree']['index'])):
		acum+=W_IS_k[k]
		if r<acum*tau:
			users['i_k_t'][k]-=variation
			users['s_k_t'][k]+=variation
			break
		acum+=W_IR_k[k]
		if r<acum*tau:
			users['i_k_t'][k]-=variation
			users['r_k_t'][k]+=variation
			break
		acum+=W_SR_k[k]
		if r<acum*tau:
			users['s_k_t'][k]-=variation
			users['r_k_t'][k]+=variation
			break
		acum+=W_RS_k[k]
		if r<acum*tau:
			users['r_k_t'][k]-=variation
			users['s_k_t'][k]+=variation
			break
	return users,tau


def execute(SIR):
	if SIR=={}:
		SIR=load_dir('SIR.pkl')
	else:
		back_up(SIR,'SIR.pkl')
	results=SIR['results']
	inputs=SIR['inputs']
	graph=SIR['graph']
	results['t_t'].append(np.float64(0.0))
	results['i_t'].append(np.float64(1.0))
	results['s_t'].append(np.float64(0.0))
	results['r_t'].append(np.float64(0.0))
	rates=SIR['results']['rates']
	rates['accepting_rate']=inputs['rates']['lambda']*(1-inputs['probabilities']['beta'])
	rates['reffusing_rate']=inputs['rates']['lambda']*(inputs['probabilities']['beta'])
	rates['stifling_rate']=inputs['rates']['lambda']*(inputs['probabilities']['alpha'])
	rates['persuading_rate']=inputs['rates']['lambda']*(1-inputs['probabilities']['eta'])
	rates['forgetting_rate']=inputs['rates']['delta']
	rates['remembering_rate']=inputs['rates']['xi']
	users={
		'i_k_t':graph['degree']['Exp']['degree_dist'],
		's_k_t':[np.float64(0.0)]*len(graph['degree']['index']),
		'r_k_t':[np.float64(0.0)]*len(graph['degree']['index'])
		}
	variation=np.float64(1.0/graph['nodes'])
	users['i_k_t'][0]-=variation
	users['s_k_t'][0]+=variation
	maxIters=100000
	while users['i_k_t']>0 and len(results['t_t'])<maxIters:
		users,time=iterate_BF(users,graph,rates)
		i_t=np.float64(0.0)
		s_t=np.float64(0.0)
		r_t=np.float64(0.0)
		t_t=results['t_t'][-1]+time
		for k in range(len(graph['degree']['index'])):
			i_t+=users['i_k_t'][k]
			s_t+=users['s_k_t'][k]
			r_t+=users['r_k_t'][k]
		results['t_t'].append(t_t)
		results['i_t'].append(i_t)
		results['s_t'].append(s_t)
		results['r_t'].append(r_t)
		cont=1000
		if len(results['t_t'])%cont==0:
			plot(False,results['t_t'],results['i_t'],results['r_t'],results['s_t'])
	back_up(users,'evolution.pkl')
		


SIR={
	'results':{
		'rates':{
			'accepting_rate':0,
			'reffusing_rate':0,
			'stifling_rate':0,
			'persuading_rate':0,
			'forgetting_rate':0,
			'remembering_rate':0},
		't_t':[],
		'i_t':[],
		's_t':[],
		'r_t':[]},
	'graph':{
		'status':'INIT',
		'nodes':0,
		'edges':0,
		'name':'None',
		'savefile':'',		
		'degree':{
			'k_mean':0,
			'count':[],
			'index':[],
			'Teo':{
				'degree_dist':[],
				'uncorr_func':[],
			},
			'BF':{
				'degree_dist':[],
				'uncorr_func':[],
			},
			'Exp':{
				'degree_dist':[],
				'uncorr_func':[],
				'corr_func':{},
			},
		},
	},
	'inputs':{
		'status':'INIT',	
		'probabilities':{
			'alpha':0,
			'beta':0,
			'eta':0},
		'rates':{
			'lambda':0,
			'delta':0,
			'xi':0},
	},
}

