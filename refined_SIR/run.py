#!/usr/bin/env python
"""
execution code for refined SIR model
"""
__author__ = """Sergio Yaksic <seanyabe@gmail.com>"""

from utils.sirSNA import *
import sys
from config import set_up, src_Menu
from subprocess import call
import reader



if __name__ == "__main__":
	Max=1
	if len(sys.argv)==1:
		exp=src_Menu()
		if exp==None:
			graph,inputs,path=set_up()
		else:
			graph,inputs,path=set_up(exp)
		Max=int(raw_input('Numero de ejecuciones? '))
	if len(sys.argv)==2:
		graph,inputs,path=set_up(sys.argv[1])
		Max=int(raw_input('Numero de ejecuciones? '))
	if len(sys.argv)==3:
		graph,inputs,path=set_up(sys.argv[1])
		Max=int(sys.argv[2])
	for x in range(Max):
		print('EXECUTION '+str(x+1))
		execute(graph,inputs,path+'results/')
		call(["nepidemix_runsimulation", path+"conf/SIR.ini"])
	if len(sys.argv)>1:
		reader.read(sys.argv[1])
