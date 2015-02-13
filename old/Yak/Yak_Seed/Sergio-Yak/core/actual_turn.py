import time
from utils import *

def Master(turn):
	print('MASTER')
	turn['order']=raw_input('Ingresa orden ')
	turn['MASTER']='User'

def Slave():
	print('SLAVE')
	print('Ejecuta estas ordenes.')

def check_status(mode):
	turn=load('./saves/turn.pkl')
	if turn=={}:
		if mode=='MASTER':
			Master(turn)
	if mode=='SLAVE':
		Slave()
	back_up(turn,'./saves/turn.pkl')
	print(turn)
	time.sleep(5)

