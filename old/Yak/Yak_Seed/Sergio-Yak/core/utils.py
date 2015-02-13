import pickle
import os

def back_up(dictionary,filename):
	with open(filename, 'w') as f: 
		pickle.dump(dictionary, f)
	return filename

def load(filename):
	if os.path.isfile(filename):
		with open(filename, 'rb') as f:
			return pickle.load(f)
	else:
		return {}