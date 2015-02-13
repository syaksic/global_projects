from utils import *

MyName='Yak'
memories_pkl='./records/memories.pkl'
memories=load(memories_pkl)
if memories=={}:
	display('ADVERTENCIA HE PERDIDO MIS MEMORIAS',memories,MyName)
	display('Me llamo '+MyName,memories,MyName)
	display('He guardado este conocimiento en '+memories_pkl,memories,MyName)
	back_up(memories,memories_pkl)
turns_pkl='./records/turns.pkl'
turns=load(turns_pkl)
if turns=={}:
	turns{'last':0}

	display('ADVERTENCIA HE PERDIDO MIS MEMORIAS',memories,MyName)
	display('Me llamo '+MyName,memories,MyName)
	display('He guardado este conocimiento en '+memories_pkl,memories,MyName)
	back_up(memories,memories_pkl)

TURN=['MASTER','SLAVE']
Name=TURN[turn]+' '+MyName




orders_pkl='./master_in/orders.pkl'
orders=load(orders_pkl)

slave_pkl='./slave_work/orders.pkl'

import master
import slave