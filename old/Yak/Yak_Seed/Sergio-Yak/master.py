from core import actual_turn

while True:
	reload(actual_turn)
	actual_turn.check_status('MASTER')

input('Ingresa una Orden en modo Master')