
#!/usr/bin/env python
"""
configurations for refined SIR model
"""
__author__ = """Sergio Yaksic <seanyabe@gmail.com>"""

from utils.plot import *
from utils.graph import *
import os
import shutil

##########  __  __  ____  _____ _____ ________     __  __________  _   _ ______ ###########
########## |  \/  |/ __ \|  __ \_   _|  ____\ \   / / |___  / __ \| \ | |  ____|###########
########## | \  / | |  | | |  | || | | |__   \ \_/ /     / / |  | |  \| | |__   ###########
########## | |\/| | |  | | |  | || | |  __|   \   /     / /| |  | | . ` |  __|  ###########
########## | |  | | |__| | |__| || |_| |       | |     / /_| |__| | |\  | |____ ###########
########## |_|  |_|\____/|_____/_____|_|       |_|    /_____\____/|_| \_|______|###########
##########                                                                      ###########                                                                    
#Setup parameters for new experiments
#Initial conditions S0+I0+R0=size
size=10000
S0 = 10
I0 = 9990
R0 = 0
#rates
_lambda=1.0
_delta=0.01
_xi=0.001
#probs
_alpha=0.6
_beta=0.4
_eta=0.7
#iterations
SNAIter=40000
SIMIter=500
###############################   _____                                    _ ################
###############################  / ____|           /\                     | |################
############################### | |  __  ___      /  \__      ____ _ _   _| |################
############################### | | |_ |/ _ \    / /\ \ \ /\ / / _` | | | | |################
############################### | |__| | (_) |  / ____ \ V  V / (_| | |_| |_|################
###############################  \_____|\___/  /_/    \_\_/\_/ \__,_|\__, (_)################
###############################                                       __/ |  ################
###############################                                      |___/   ################

#
#By default all experiments ends in experiment folder you may change the default here
##
src='./experiments/'
if not os.path.exists(src):
	os.makedirs(src)
#
#By default a demo folder is created you may change the default here
#
demo='demo'+str(size)
path=src+demo+'/'


def config_sim(inifile):
	text='''
[Simulation]
iterations = %s
dt = 0.1
process_class = SIRProcess
process_class_module = extended_SIR
module_paths = %s
network_func = load_network
network_func_module = nepidemix.utilities.networkgeneratorwrappers
node_init = true
edge_init = true

[Output]
output_dir = %s
base_name = test_SIR
unique = yes
save_config = no
save_state_count = yes
save_state_count_interval = 1
save_network = no
save_network_interval = 0
save_state_influx_interval = 1
save_state_influx = no
save_state_transition_cnt = false
save_network_format = gpickle
save_network_compress_file = true
print_progress_bar = false

[ProcessParameters]
_lambda = %s
_delta = %s
_xi = %s
_alpha = %s
_beta = %s
_eta = %s

[NetworkParameters]
file = %s

[NodeStateDistribution]
S = %s
I = %s
R = %s
''' % (int(SIMIter),path+'modules',path+'output',str(_lambda),str(_delta),str(_xi),str(_alpha),str(_beta),str(_eta),path+"graph.gpickle",str(S0),str(I0),str(R0))
	with open(inifile, 'w') as f:
		f.write(text)
	return text

###############################   _____                                    _ ################
###############################  / ____|           /\                     | |################
############################### | |  __  ___      /  \__      ____ _ _   _| |################
############################### | | |_ |/ _ \    / /\ \ \ /\ / / _` | | | | |################
############################### | |__| | (_) |  / ____ \ V  V / (_| | |_| |_|################
###############################  \_____|\___/  /_/    \_\_/\_/ \__,_|\__, (_)################
###############################                                       __/ |  ################
###############################                                      |___/   ################



def src_Menu():
	experimentsDirs= [ f for f in os.listdir(src) if os.path.isdir(os.path.join(src,f)) ]
	num=0
	menu={}
	for op in experimentsDirs:
		num+=1
		menu[num]=op
	print(menu)
	if len(menu)>0:
		if len(menu)==1 and menu[1]==demo:
			op=None
		else:
			op=menu[input('seleccione experimento')]
	else:
		op=None
	return op

def set_graph():
	graph={}
	graph['status']='INIT'
	if os.path.isfile(path+"graph.json"):
		Graph=loadjson(path+"graph.json")
	elif os.path.isfile(path+"graph.gpickle"):
		Graph=loadtest(path+"graph.gpickle")
	else:
		graph['savefile'],Graph=generate_graph(path+'graph',size)
	graph['nodes']=Graph.number_of_nodes()
	graph['edges']=Graph.number_of_edges()
	graph['name']=Graph.name
	degrees=degree_dist(nx.degree_histogram(Graph),graph['nodes'])
	degrees_degrees=degree_corr(degrees['index'],degrees['count'],Graph,degrees['kmean'])
	graph['degree']={}
	graph['degree']['k_mean']=degrees['kmean']
	graph['degree']['count']=degrees['count']
	graph['degree']['index']=degrees['index']
	graph['degree']['BF']={}
	graph['degree']['BF']['degree_dist']=degrees['bf']
	graph['degree']['BF']['uncorr_func']=degrees_degrees['bf']
	graph['degree']['Teo']={}
	graph['degree']['Teo']['degree_dist']=degrees['teo']
	graph['degree']['Teo']['uncorr_func']=degrees_degrees['teo']
	graph['degree']['Exp']={}	
	graph['degree']['Exp']['degree_dist']=degrees['prob']
	graph['degree']['Exp']['uncorr_func']=degrees_degrees['uncorrelated_prob']
	graph['degree']['Exp']['corr_func']=degrees_degrees['dgr_dgr_func']
	graph['status']='READY'
	back_up(graph,path+'graph.pkl')

def set_inputs():
	inputs={'probabilities':{},'rates':{},'initial':{}}
	inputs['status']='INIT'
	inputs['MaxIter']=SNAIter
	probs=inputs['probabilities']
	probs['alpha']=np.float64(_alpha)
	probs['beta']=np.float64(_beta)
	probs['eta']=np.float64(_eta)
	rates=inputs['rates']
	rates['lambda']=np.float64(_lambda)
	rates['delta']=np.float64(_delta)
	rates['xi']=np.float64(_xi)
	initial=inputs['initial']
	initial['I0']=I0
	initial['S0']=S0
	initial['R0']=R0
	inputs['status']='READY'
	back_up(inputs,path+'/inputs.pkl')


def set_up(new_path=None):
	if not(new_path==None):
		global demo
		global path
		demo=new_path
		path=src+demo+'/'

	if not os.path.exists(path):
	    os.makedirs(path)
	if not os.path.exists(path+'results'):
	    os.makedirs(path+'results')
	if not os.path.exists(path+'plots'):
	    os.makedirs(path+'plots')
	if not os.path.exists(path+'modules'):
	    os.makedirs(path+'modules')
	    shutil.copy2('./utils/extended_SIR.py', path+'modules'+'/extended_SIR.py')
	if not os.path.exists(path+'output'):
	    os.makedirs(path+'output')
	if not os.path.exists(path+'conf'):
	    os.makedirs(path+'conf')
	    config_sim(path+'conf'+'/SIR.ini')

	global graph
	graph=load_dic(path+'graph.pkl')
	if graph=={}:
		set_graph()
		graph=load_dic(path+'graph.pkl')
		plot_graph_degrees(graph,path+'plots/')
		plot_graph_degree_degree(graph,path+'plots/')
	global inputs
	inputs=load_dic(path+'inputs.pkl')
	if inputs=={}:
		set_inputs()
		inputs=load_dic(path+'inputs.pkl')
	return graph,inputs,path