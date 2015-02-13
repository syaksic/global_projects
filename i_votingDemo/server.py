from utils import paillier
from utils.paillier import *
import simplejson as json
import pickle
import socket
import sys
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)



def setup_votation(voting_id):
    print "Generating keypair..."
    modulusbits=512
    priv, pub = generate_keypair(modulusbits)
    with open('savedkey'+str(voting_id), 'w') as f:   
        pickle.dump(priv, f)
    e_zero=encrypt(pub,0)
    print(pub)
    return {'pub_key':str(pub.n),'voting_id':voting_id,'modulusbits':modulusbits,'acum':str(e_zero)}


def receive_votes(acumvotes,voting_id,pub):
    print "Decripting total votes..."
    with open('savedkey'+str(voting_id), 'rb') as f:
        priv=pickle.load(f)
    total=decrypt(priv,pub,acumvotes)
    print(total,pub.n)
    return {'results':total}

def do_something(connstream, data):
    print "do_something:", data
    return False

def deal_with_client(conn):
    data=conn.recv(100000)
    data=data.decode("utf-8")
    while data:
        response=json.loads(data)
        print(response)
        if response['mode']=='new_voting':
            config=setup_votation(response['voting_id'])
            text=json.dumps(config,separators=(',', ':'), sort_keys=True)
            conn.send(text)
        elif response['mode']=='spy':
            content=receive_votes(int(response['acum']),response['voting_id'],PublicKey(int(response['pub_key'])))
            text=json.dumps(content,separators=(',', ':'), sort_keys=True)
            conn.send(text)
        if not do_something(conn, data):
            break
        data = conn.recv(100000)


host= '200.1.17.228'
port=int(10024)
s.bind((host,port))
s.listen(1)

while True:
    conn,addr =s.accept()
    print (conn,addr)
    try:
        deal_with_client(conn)
    finally:
        s.close
