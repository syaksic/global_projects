from __init__ import *

def check_turn():
	if TURN[turn]=='MASTER':
		reload(master)
		seek=master.turn()
	elif TURN[turn]=='SLAVE':
		reload(slave)
		seek=slave.turn(60)	
	return seek

os.system('cls' if os.name == 'nt' else 'clear')
display('Iniciando turno 1',memories,MyName)
display('Iniciando turno 1',memories,MyName)
display('Me ha tocado modo '+TURN[turn],memories,Name)



display('Favor no reiniciarme tan frecuentemente',memories,MyName)
display('Aqui vamos...',memories,MyName)
display('Me ha tocado modo '+TURN[turn],memories,Name)
while True:
	if not(ready):
		seek=check_turn()
		if seek['ready']:
			input('no se que hacer aqui')







#		display('Mi turno como '+TURN[turn]+' ha finalizado',memories,MyName)
#
#		ready=seek['ready']
#	else:
#		print('===============')
#		print('Cambio de Turno')
#		print('===============')
#		turn=(turn+1)%2 
#		Name=TURN[turn]+' '+MyName
#		ready=False
	
	
	
	