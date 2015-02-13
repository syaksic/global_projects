import sys
import os
import subprocess

def runTurn(turn={}):


	result={}
	return result


if __name__ == "__main__":
	if len(sys.argv)==2:
		players=sys.argv[1]
	else:
		players='Sergio-Yak' 
	if not os.path.exists(players): 
		os.makedirs(players)
	if not os.path.exists(players+'/core'): 
		os.makedirs(players+'/core')
	if not os.path.exists(players+'/saves'): 
		os.makedirs(players+'/saves')

	if not os.path.isfile(players+'/core/actual_turn.py'): 
		open(players+'/core/actual_turn.py','w').close()
	if not os.path.isfile(players+'/core/__init__.py'): 
		open(players+'/core/__init__.py','w').close()
	if not os.path.isfile(players+'/core/utils.py'): 
		open(players+'/core/utils.py','w').close()

	if not os.path.isfile(players+'/master.py'):
		open(players+'/master.py','w').close()
	subprocess.call(['gnome-terminal','-x','python','./'+players+'/master.py'])
	if not os.path.isfile(players+'/slave.py'):
		open(players+'/slave.py','w').close()
	subprocess.call(['gnome-terminal','-x','python','./'+players+'/slave.py'])

	runTurn()

