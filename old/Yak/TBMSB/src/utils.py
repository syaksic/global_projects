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

def initTurn(players):
	seek={'turns':{},'user':{},'bot':{}}
	seek['user']['name']=players.split('-')[0]
	seek['bot']['name']=players.split('-')[1]
	if not os.path.exists(players): 
		os.makedirs(players)
	seek['turns'][0]=turn0
	seek['back_up']='./'+players+'/t0.pkl'
	return back_up(seek,seek['back_up'])

