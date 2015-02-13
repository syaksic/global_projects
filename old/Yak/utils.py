import os
import pickle
import pprint
import time
import random
import subprocess

def back_up(dictionary,filename):
	with open(filename, 'w') as f: 
		pickle.dump(dictionary, f)

def load(filename):
	if os.path.isfile(filename):
		with open(filename, 'rb') as f:
			return pickle.load(f)
	else:
		return {}

def display(word,dictionary,Name=None):
	if word in dictionary:
		dictionary[word]+=1
	else:
		dictionary[word]=1
	if Name==None:
		print word
	else:
		print Name+': '+word

def incremental_sleep(sleepTime):
	time.sleep(sleepTime)
	sleepTime+=0
 	return sleepTime