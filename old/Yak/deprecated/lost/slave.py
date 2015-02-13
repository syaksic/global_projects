from __init__ import *

slave_pkl='./slave_work/orders.pkl'

def turn(duration):
	result={}
	result['ready']=False
	elapsed=0
	while True:
		if elapsed>duration:
			result['response']='No hay nada que hacer'
			result['ready']=True
			break
		if os.path.isfile(slave_pkl):
			result['response']='Hay nuevas ordenes'
			result['ready']=False
			break
		time.sleep(1)
		elapsed+=1	
	return result

#	subprocess.call(['gnome-terminal','-x','python','./master.py'])