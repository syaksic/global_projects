from core import actual_turn

while True:
	reload(actual_turn)
	actual_turn.check_status('SLAVE')

input('Hola este es mi modo Slave')