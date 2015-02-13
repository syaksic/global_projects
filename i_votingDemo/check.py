#!/usr/bin/python
# -*- coding: utf-8 -*-

from utils import paillier
from utils.paillier import *
import sys
import pickle

if __name__ == "__main__":
	if len(sys.argv) == 4: 
		if sys.argv[1]=='encrypt':#python run.py 'encrypt' pub_key int
			print(encrypt(PublicKey(int(sys.argv[2])),int(sys.argv[3])))
		if sys.argv[1]=='e_votes':#python run.py 'e_votes' options.count voters.count 
			N_max=int(sys.argv[3])
			options=int(sys.argv[2])
			code=0
			line=''
			for i in range(options):
				code+=pow(N_max,i)
				line=line+','+str(code)
			print line[1:]
		if sys.argv[1]=='results':#python run.py 'results' total list 
			total=int(sys.argv[2])
			options=sys.argv[3][1:]
			options=options[:len(options)-1]
			options=options.split(',')
			line=''
			for i in reversed(range(len(options))):
				line=line+','+str(total/int(options[i]))
				total=total % int(options[i])
			print line[1:]
	if len(sys.argv) == 5:#python run.py 'e_add' pub_key int1 int2
		if sys.argv[1]=='e_add':
			print(e_add(PublicKey(int(sys.argv[2])),int(sys.argv[3]),int(sys.argv[4])))