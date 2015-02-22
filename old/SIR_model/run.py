#!/usr/bin/python

from source.data import *
#import source import utils

def Calculate():
	print(SIR)
	graph=SIR['graph']
	if not(graph['status']=='READY'):
		set_graph(graph)
	inputs=SIR['inputs']
	if not(inputs['status']=='READY'):
		#tasa de contacto: 1 usuario cada 1 segundo
		mean_contact_rate=1.0/1.0
		#tasa de olvido: 1 olvido cada 1 dia 86400 segundos
		mean_forgetting_rate=1.0/3000.0
		#tasa de recuerdo: 1 recuerdo cada 10 dias 864000 segundos
		mean_remember_rate=0.0
		#probabilidade de ostigarse de un rumor 0.1
		stifling_prob=0.9
		#probabilidade de rechazar/aceptar un rumor 0.9/0.1
		reffusing_prob=0.9
		#probabilidade de no-recapacitar/recapacitar sobre un rumor 0.99/0.01
		unrethinking_prob=0.0
		set_inputs(inputs,
			stifling_prob,reffusing_prob,stifling_prob,
			mean_contact_rate,mean_forgetting_rate,mean_remember_rate)
	execute(SIR)
	return 

#execute({})
Calculate()
