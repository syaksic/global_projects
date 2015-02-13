from utils import paillier
from utils.paillier import *
import simplejson as json
import pickle
import socket, ssl



def setup_votation():
	print "Generating keypair..."
	priv, pub = generate_keypair(512)
	votation_id=1234 #falta agregar un generador de votation_id
	with open('savedkey'+str(votation_id), 'w') as f:	
		pickle.dump(priv, f)
	return {'pub_key':pub.n,'votation_id':votation_id}


def receive_votes(acumvotes,votation_id,pub):
	print "Decripting total votes..."
	with open('savedkey'+str(votation_id), 'rb') as f:
		priv=pickle.load(f)
	total=decrypt(priv,pub,acumvotes)
	return {'results':total}

def do_something(connstream, data):
    print "do_something:", data
    return False

def deal_with_client(connstream):
    data = connstream.read()
    while data:
    	response=json.loads(data)
    	print(response)
    	if response['mode']=='new_voting':
    		config=setup_votation()
    		text=json.dumps(config,separators=(',', ':'), sort_keys=True)
    		connstream.write(text)
    	elif response['mode']=='spy':
    		content=receive_votes(response['acum'],response['voting_id'],PublicKey(response['pub_key']))
    		text=json.dumps(content,separators=(',', ':'), sort_keys=True)
    		connstream.write(text)
        if not do_something(connstream, data):
            break
        data = connstream.read()



bindsocket = socket.socket()
bindsocket.bind(('', 10023))
bindsocket.listen(5)


while True:
    newsocket, fromaddr = bindsocket.accept()
    connstream = ssl.wrap_socket(newsocket,
                                 server_side=True,
                                 certfile="server.crt",
                                 keyfile="server.key",
                                 ssl_version=ssl.PROTOCOL_SSLv3)
    try:
        deal_with_client(connstream)
    finally:
        connstream.shutdown(socket.SHUT_RDWR)
        connstream.close()


