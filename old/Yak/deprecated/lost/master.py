from __init__ import *

if orders=={}:
	orders=load(orders_pkl)
	orders['last_id']=0
	orders['list']={}
	back_up(orders,orders_pkl)

def createOrder(name=None):
	newOrder={}
	if name==None:
		newOrder['name']=raw_input('order name: ')
	else:
		newOrder['name']=name
	orders['last_id']+=1
	newOrder['id']=orders['last_id']
	newOrder['status']='ToDo'
	orders['list'][newOrder['id']]=newOrder
	back_up(orders,orders_pkl)
	return orders

def sendOrders():
	orders=load(orders_pkl)
	back_up(orders,slave_pkl)

def turn(result={}):
	if result=={}:
		result['ready']=False
	if result['ready']:
		display('Avisame cuando hayas terminado',memories,Name)
	if len(orders['list'])==0:
		createOrder('demo')	
	display('Ejecutar estas ordenes!!!',memories,Name)
	for order in orders['list']:
		if orders['list'][order]['status']=='ToDo':
			display('Tarea '+str(order)+': '+orders['list'][order]['name'],memories)	
	result['response']='Ejecutar estas ordenes!!!'
	back_up(orders,orders_pkl)
	sendOrders()
	result['ready']=True
	return result






def main():
	createOrder()
	sendOrders()
	print('')


def MasterTerminal():
	print('MasterTerminal')
	order={'id':00000,'msg':'OrderDEMO','triggers':		['demo','test'],'status':'ToDo'}
	input('hola')
	new_order={'name':order_name}
	with open('./master_in/'+order_name, 'w') as f: 
		pickle.dump(new_order, f)


if __name__ == "__main__":
	main()






#display('Para agregar ordenes usa el MasterTerminal',memories)
#
#
#
#subprocess.call(['gnome-terminal','-x','python','./master.py'])
#display('Iniciando turno SLAVE',memories)
#
#while True:
#
#	back_up(memories,memories_pkl)
#	master_in=os.path.dirname(master_pkl)
#	if len(os.listdir(master_in))>0:
#		display('He detectado ordenes pendientes en '+master_in,memories) 
#		for items in os.listdir(master_in):
#			display(str(items),memories)
#		time.sleep(10)
#	elif len(os.listdir(master_in))==0:
#		time.sleep(1)





