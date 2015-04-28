import math
import matplotlib.pyplot as plt
import os
import pickle
import numpy as np

size=10000
k_mean=60
S0 = 1
I0 = 9999
R0 = 0
#rates
_lambda=1.0
_delta=0.01
_xi=0.001
#probs
_alpha=0.3
_beta=0.5
_eta=0.9
_etaNeg=1-_eta

#Aux rates:
_LAMBDA=_lambda*k_mean*(_etaNeg+_alpha)
_omega=_lambda*_etaNeg*k_mean-_delta
_OMEGA=-4*_LAMBDA*_xi-pow((_omega-_xi),2)+2*_xi*(_omega-_xi)-pow(_xi,2)

def plot_evolution(result,users,csv):
	Times1=result['t']
	Spreaders1=result['s']
	Times=users['t_t']
	Spreaders=users['S_t']
	Times2=csv['t_t']
	Spreaders2=csv['S_t']
	fig, ax = plt.subplots()
	ax.plot(Times,Spreaders,label='SpreadersSNA',color='purple')
	ax.plot(Times1,Spreaders1,label='SpreadersANA',color='blue')
	ax.plot(Times2,Spreaders2,label='SpreadersSIM',color='red')
	#ax.set_yscale('log')
	ax.set_xscale('log')
	legend = ax.legend(loc='upper right', shadow=True)
	frame = legend.get_frame()
	frame.set_facecolor('0.90')
	ax.set_title('refined SIR model')
	ax.set_xlabel('Time')
	ax.set_ylabel('Users/Total')
	for label in legend.get_texts():
		label.set_fontsize('large')
	for label in legend.get_lines():
		label.set_linewidth(1.5)
	#plt.axis((0.0001,10,0,1))
	plt.show()
	plt.close()

def s_1():
	a=-_LAMBDA
	b=(_omega-_xi)
	c=_xi
	Omega2=pow(b,2)+4*a*c
	sol1=(-b-math.sqrt(pow(b,2)-4*a*c))/(2*a)
	sol2=(-b+math.sqrt(pow(b,2)-4*a*c))/(2*a)
	if sol1>0:
		sol=sol1
		print(sol2)
	elif sol2>0:
		sol=sol2
	if sol1>0 and sol2>0:
		print('ESTO ES RARO')
	result={'result':sol,'sol1':sol1,'sol2':sol2,'Omega':math.sqrt(Omega2)}
	return result

def calc_C(t0,s0,s1):
	aux=1.0/(s0-s1['result'])-_LAMBDA
	C=math.exp(-s1['Omega']*t0)*(aux)
	return C

def s_t(t,s1,C):
	z=C*math.exp(s1['Omega']*t)+_LAMBDA
	sol=s1['result']+1.0/z
	result={'result':sol,'s1':s1['result'],'1/z':1.0/z}
	return result

def load_dic(filename):
	if os.path.isfile(filename):
		with open(filename, 'rb') as f:
			return pickle.load(f)
	else:
		return {}

def load_csv(filename):
	data = np.genfromtxt(filename, delimiter=',', names=['t_t','I_t', 'S_t', 'R_t'])
	return data

def load_csv(filename):
	data = np.genfromtxt(filename, delimiter=',', names=['t_t','I_t', 'S_t', 'R_t'])
	return data

bkp=load_dic('test.bkp')
csv=load_csv('test.csv')
s1=s_1()
s0=float(1)/size
s=[s0*size]
t0=.0001
times=[t0]
C=calc_C(t0,s0,s1)
print({'C':C,'s1':s1['result']})
for dt in range(100000):
	t=times[-1]+0.0001
	times.append(t)
	s.append(s_t(t,s1,C)['result']*size)
result={'s':s,'t':times}
plot_evolution(result,bkp,csv)

#s(t) = (sqrt(-4 a c-b^2+2 b c-c^2) tan(1/2 (k_1 sqrt(-4 a c-b^2+2 b c-c^2)-t sqrt(-4 a c-b^2+2 b c-c^2)))+b-c)/(2 a)
#
