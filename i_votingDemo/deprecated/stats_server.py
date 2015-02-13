from paillier import *
import sum_server

priv = PrivateKey(128)

def setup_votation(options,codes):
	print "Generating keypair..."
	global priv
	pub = priv.pub
	votation_id=1234 #falta agregar un generador de votation_id
	sum_server.new_votation(votation_id)
	return {'pub_key':pub,'votation_id':votation_id}

def request_votes(votation_id):
	global priv
	acumvotes=sum_server.send_acumvotes(votation_id)
	total=decrypt(acumvotes, priv)
	return total