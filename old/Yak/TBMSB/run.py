from __init__ import *
# un seek guarda muchos turnos






turn0={}
turn0['order']=['init','Sergio-Yak']
turn0['job']=['initTurn("'+turn0['order'][1]+'")']
def initTurn(players):
	seek={'turns':{},'user':{},'bot':{}}
	seek['user']['name']=players.split('-')[0]
	seek['bot']['name']=players.split('-')[1]
	if not os.path.exists(players): 
		os.makedirs(players)
	seek['turns'][0]=turn0
	seek['back_up']='./'+players+'/t0.pkl'
	return back_up(seek,seek['back_up'])
	
def runTurn(turn):
	print(turn['order'])
	print(eval(turn['job'][0]))
	print(turn['job'])




runTurn(turn0)
seek=load('./Sergio-Yak/t0.pkl')
print(seek)



