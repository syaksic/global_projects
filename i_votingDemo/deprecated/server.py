from paillier import *
import stats_server
import sum_server

N_max=10
options={'Obama':0,'Bachelet':1,'Putin':2}

def generate_voting_codes(options):
	voting_codes=[]
	code=0
	for i in range(len(options)):
		code+=pow(N_max,i)
		voting_codes.append(code)
	return voting_codes



def send_vote(enc_vote,id):
	sum_server.receive_vote(enc_vote,id)
	return enc_vote

def voting_emulator(options):
	voting_codes=generate_voting_codes(options)
	config=stats_server.setup_votation(options,voting_codes)
	print options
	for user in range(N_max):
		send_vote(encrypt(voting_codes[input('user'+str(user)+' seleccione preferencia ')],config['pub_key']),config['votation_id'])
		 
 	total=stats_server.request_votes(config['votation_id'])
 	count=[0]*len(options)
 	for i in reversed(range(len(options))):
 		count[i]=total/voting_codes[i]
 		total=total % voting_codes[i]
	results={}
	results.update(options)
	for key in results:
		results[key]=count[results[key]]
	print(results)


voting_emulator(options)