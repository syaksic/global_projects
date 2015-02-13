import socket, ssl, pprint
import simplejson as json
import operator
import ast
import pickle
from utils import paillier
from utils.paillier import *

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Require a certificate from the server. We used a self-signed certificate
# so here ca_certs must be the server certificate itself.
ssl_sock = ssl.wrap_socket(s,
                           ca_certs="server.crt",
                           cert_reqs=ssl.CERT_REQUIRED)

ssl_sock.connect(('200.1.17.228', 10023))

#print repr(ssl_sock.getpeername())
#print ssl_sock.cipher()
#print pprint.pformat(ssl_sock.getpeercert())



def startvotation():
    print('startvotation')
    N_max=10
    options={'Obama':0,'Bachelet':1,'Putin':2}
    #generating voting codes
    voting_codes=[]
    code=0
    for i in range(len(options)):
        code+=pow(N_max,i)
        voting_codes.append(code)
    msg={'mode':'new_voting'}
    text=json.dumps(msg,separators=(',', ':'), sort_keys=True)
    ssl_sock.write(text)
    data = ssl_sock.read()
    ssl_sock.close()
    response=json.loads(data)
    zero=encrypt(PublicKey(response['pub_key']),0)
    acum=e_add(PublicKey(response['pub_key']),zero,zero)
    votation={'Nmax':N_max,'codes':voting_codes,'options':options,'acumvotes':acum,'pub_key':response['pub_key']}
    with open('votation'+str(response['votation_id']), 'w') as f:    
        pickle.dump(votation, f)
    print('votation initiated')
    return 1

def spyvotation(voting_id):
    print('spyvotation')
    with open('votation'+str(voting_id), 'rb') as f:
        votation=pickle.load(f)
    msg={'mode':'spy','acum':votation['acumvotes'],'voting_id':voting_id,'pub_key':votation['pub_key']}
    text=json.dumps(msg,separators=(',', ':'), sort_keys=True)
    ssl_sock.write(text)
    data = ssl_sock.read()
    ssl_sock.close()
    response=json.loads(data)
    total=response['results']

    count=[0]*len(votation['options'])
    for i in reversed(range(len(votation['options']))):
        count[i]=total/votation['codes'][i]
        total=total % votation['codes'][i]
    results={}
    results.update(votation['options'])
    for key in results:
        results[key]=count[results[key]]

    print(results)
    return 2

def endvotation(voting_id):
    print('endvotation')
    return 3


def servermode():
    print('server')
    x={'start votation':1,'spy votation':2,'end votation':3,'exit':0}
    options = sorted(x.items(), key=operator.itemgetter(1))
    selection=-1
    while not(selection==0) : 
        print(options)
        selection=input('seleccione opcion')
        for option in x:
            if x[option]==selection:
                break
        if option=='start votation':
            selection=startvotation()
        elif option=='spy votation':
            selection=spyvotation(input('votation_id: '))
        elif option=='end votation':
            selection=endvotation()
        else:
            print('error de opcion')
            selection=-1


def clientmode(voting_id):
    print('client')
    with open('votation'+str(voting_id), 'rb') as f:
        votation=pickle.load(f)
    print(votation['options'])
    value=encrypt(PublicKey(votation['pub_key']),votation['codes'][input('seleccione opcion: ')])
    acum=e_add(PublicKey(votation['pub_key']),votation['acumvotes'],value)
    votation['acumvotes']=acum
    with open('votation'+str(voting_id), 'w') as f:    
        pickle.dump(votation, f)
    print('Su voto ha sido ingresado exitosamente')



modes={'server':0,'client':1}
print(modes)
selection=input('seleccione version')
for option in modes:
    if modes[option]==selection:
        break
if option=='server':
    servermode()
elif option=='client':
    clientmode(input('votation_id: '))
else:
    print('error de opcion')





if False: # from the Python 2.7.3 docs
    # Set a simple HTTP request -- use httplib in actual code.
    ssl_sock.write("Llegada fallida")

    # Read a chunk of data.  Will not necessarily
    # read all the data returned by the server.
    data = ssl_sock.read()

    # note that closing the SSLSocket will also close the underlying socket
    ssl_sock.close()


