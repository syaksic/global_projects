import scipy.integrate as spi
import numpy as np
import pylab as pl

#rates
_lambda=1.0
_delta=0.01
_xi=0.001
#probs
_alpha=0.3
_beta=0.5
_eta=0.9

TS=1.0
tmax =50
I0=1.0-1.0/1000
S0=1.0/1000
INPUT = (I0, S0, 0.0)

def diff_eqs(INP,t):
	Y=np.zeros((3))
	V = INP
	Y[0] = - _lambda * V[0] * V[1]
	Y[1] = _lambda * V[0] * V[1] * (1-_beta) - _delta * V[1] + V[2] *_xi - V[1] * V[1] * _lambda*_alpha + V[1]*V[2]* _lambda*(1-_eta)
	Y[2] = _lambda * V[0] * V[1] * _beta + _delta * V[1] - V[2] *_xi + V[1] * V[1] * _lambda*_alpha - V[1]*V[2]* _lambda*(1-_eta)
	return Y   # For odeint

t_start = 0.0; t_end = tmax; t_inc = TS
t_range = np.arange(t_start, t_end+t_inc, t_inc)
RES = spi.odeint(diff_eqs,INPUT,t_range)

print RES

#Ploting
pl.subplot(211)
pl.plot(RES[:,0], '-g', label='Ignorant')
pl.plot(RES[:,2], '-k', label='Retired')
pl.legend(loc=0)
pl.title('SIR.py')
pl.xlabel('Time')
pl.ylabel('Susceptibles and Recovereds')
pl.subplot(212)
pl.plot(RES[:,1], '-r', label='Spreaders')
pl.xlabel('Time')
pl.ylabel('Infectious')
pl.show()


#http://jiansenlu.blogspot.com/2010/06/solve-sir-model-c.html