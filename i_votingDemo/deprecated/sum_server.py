import pickle


def new_votation(id):
	votation={'acumvotes':1}
	with open('votation'+str(id), 'w') as f:	
		pickle.dump(votation, f)

def receive_vote(enc_vote,id):
	with open('votation'+str(id), 'rb') as f:
		votation=pickle.load(f)
	votation['acumvotes']=votation['acumvotes']*enc_vote
	with open('votation'+str(id), 'w') as f:	
		pickle.dump(votation, f)

def send_acumvotes(id):
	with open('votation'+str(id), 'rb') as f:
		votation=pickle.load(f)
	return votation['acumvotes']