#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import commands
import webbrowser
import subprocess
import shlex

####################################################################################

##############
### BASICS ###
##############
Basics='''2014-09-04
Basic functions of YakForm
- add_notes(author,note)
- add_paragraph(paragraph)
- add_text(text)
- add_tittle(tittle,h=1)
- generate(filename)
- compile(filename)
'''

Inform=[]

def add_notes(author,note):
    Inform.append('<!--'+author+':')
    for lines in note:
        Inform.append(lines)
    Inform.append('-->')
    Inform.append('\n\n')

def add_paragraph(paragraph):
    for lines in paragraph:
        Inform.append(lines)
    Inform.append('\n\n')

def add_text(text):
    Inform.append(text+'\n\n')

def add_tittle(tittle,h=1):
    ht=''
    for i in range(int(h)):
        ht=ht+'#'
    Inform.append(ht+' '+tittle+'\n\n')

def generate(filename):
	print(filename)
	fw = open(filename,'w')
	for lines in Inform:
		fw.write(lines)
	fw.close

def compile(filename,outputFile):
	Name, Extension = os.path.splitext(filename)
	if Extension in ('.md','.MD','.Md','mD'):
		commands.getoutput("pandoc "+filename+" -s -o "+Name+".pdf")
		webbrowser.open(Name+".pdf")
	elif Extension in ('.tex'):
		proc=subprocess.Popen(shlex.split('pdflatex -output-directory='+outputFile+' '+filename))
		proc.communicate()

		webbrowser.open(Name+".pdf")
	else:
		print("COMPILE FAIL not .md file")

###########
### END ###
###########

####################################################################################

##############
### THESIS ###
##############
Thesis='''2014-09-04
Thesis generator
- generateThesisMD(outputFile)

'''

Project_title=''
Authors=[]
Abstract=''
Introduction=''
Sections=[]
Results=''
Conclusions=''
Acknowledgments=''
Bibliography=''

def generateThesisMD(outputFile):
	add_tittle(Project_title)
	add_paragraph(Authors)
	add_tittle('Abstract',2)
	add_paragraph(Abstract)
	add_tittle('Introduction',2)
	add_paragraph(Introduction)
	for section in Sections:
		add_paragraph(section)
	add_tittle('Results',2)
	add_paragraph(Results)
	add_tittle('Conclusions',2)
	add_paragraph(Conclusions)
	add_tittle('Acknowledgments',2)
	add_paragraph(Acknowledgments)
	add_tittle('Bibliography',2)
	add_paragraph(Bibliography)
	generate(outputFile+'.md')
	return outputFile+'.md'

def compileThesisPDF(outputFile):
	compile(generateThesisMD(outputFile))


#######################################################################################################################################
#######################################################################################################################################
#########################  _____                       ################################################################################
######################### |  __ \                      ################################################################################
######################### | |  | | ___ _ __ ___   ___  ################################################################################
######################### | |  | |/ _ \ '_ ` _ \ / _ \ ################################################################################
######################### | |__| |  __/ | | | | | (_) |################################################################################
######################### |_____/ \___|_| |_| |_|\___/ ################################################################################
#########################                              ################################################################################
#########################                              ################################################################################                                    
#######################################################################################################################################
#######################################################################################################################################	


def demo0(tempfolder):
	global Project_title
	global Authors
	global Abstract
	global Introduction
	global Sections
	global Results
	global Conclusions
	global Acknowledgments
	global Bibliography
	Project_title='Demo'
	Authors=['Sergio Yaksic']
	Abstract='Demo de generador de pdf usando markdown_inform'
	Introduction='Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'
	Sections=['Demo1','Demo2','Demo3']
	Results='Zona de Resultados'
	Conclusions='Zona de Conclusiones'
	Acknowledgments='Algunos agradecimientos'
	Bibliography='La bibliografia'
	compileThesisPDF(tempfolder+'logger')

def demo1():
	compileThesisPDF(tempfolder+'logger')

def demo(tempfolder):
	if not os.path.exists(tempfolder):
		os.makedirs(tempfolder)
	demo0(tempfolder)