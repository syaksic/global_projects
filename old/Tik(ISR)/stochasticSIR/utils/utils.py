import os
import pickle
import numpy as np

def back_up(dictionary,filename):
	with open(filename, 'w') as f: 
		pickle.dump(dictionary, f)

def load_dic(filename):
	if os.path.isfile(filename):
		with open(filename, 'rb') as f:
			return pickle.load(f)
	else:
		return {}

def load_csv(filename):
	data = np.genfromtxt(filename, delimiter=',', names=['t_t','I_t', 'S_t', 'R_t'])
	return data

def load_bkp(filename):
	with open(filename, 'rb') as f:
		data=pickle.load(f)['users']
	return data