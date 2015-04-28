from __init__ import *
import time

def create_latex(filename):
	template='''
\documentclass[letterpaper,11pt]{article}
\usepackage[ansinew]{inputenc}
\usepackage{graphicx}
\usepackage[dvips,final]{epsfig}
\usepackage[dvips]{epsfig}
\usepackage{epsfig}
\usepackage{hyperref} 
\usepackage{subcaption}
\usepackage{color}
\usepackage{amssymb, amsmath}
\usepackage{float}
%\usepackage[spanish]{babel}


\\begin{document}

'''	
	with open(filename, "w") as myfile:
		myfile.write(template)

def add_tittle(filename,Tittle):
	template='''
\\begin{center}
\Large{UNIVERSIDAD T\'ECNICA FEDERICO SANTA MAR\'IA\\
Departamento de Electr\'onica}

\\vskip 5cm
\LARGE{\\bf '''+Tittle+'}'+'''
\\vskip 4cm
\end{center}
'''
	with open(filename, "a") as myfile:
		myfile.write(template)

def add_Author(filename,Authors):
	now = time.strftime('%Y-%m-%d-%H-%M-%S')
	template='''
\\begin{center}
	Thesis proposal presented by\\
	'''+Authors[0] +'''
	\\vskip .5cm
	Thesis Advisors\\
	'''+Authors[1]+''', PhD.\\
	'''+Authors[2]+''', PhD.			
	\\vskip 1cm
	'''+now+'''
\end{center}
\\thispagestyle{empty}
\\newpage
\pagenumbering{arabic}
\setcounter{page}{1}
\\newpage
\\tableofcontents
\\newpage
\\listoffigures
\\listoftables
\\newpage
'''
	with open(filename, "a") as myfile:
		myfile.write(template)

def add_Abstract(filename):
	template='''
\section{Thesis Definition}
\subsection{Title}

Information-spreading process over internet social media

\subsection{Abstract}

Internet social media like Facebook, Twitter, Youtube, E-mail or Whatsapp have drastically increased the amount of information that people share. 
Some of these Social Networks sites (SNs) include a history record that keeps a public log about each information shared (profiles, Facebook time line, private message history, etc).
In this work a refined Spreader Ignorant Retired (SIR) rumor-spreading model where this new characteristics are considered is presented. 
The novelty of this work lies in the hypothesis that users in retired or rejected compartment have a probability of being ``persuaded by spreaders" or ``spontaneously remember a rumor". 
The mean field equations that describe the dynamics between states considering these modifications are presented. 
As the aim of this study is to correctly model the information spread process over new social media, we obtain our theoretical results using: 
 A Stochastic Numerical Approach (SNA);
 Monte Carlo Simulation (SIM);
 Runge-kutta method (RKM);
 and an Analytical Approximation.
\\newpage
'''
	with open(filename, "a") as myfile:
		myfile.write(template)

def add_Introduction(filename,intro):
	with open(filename, "a") as myfile:
		myfile.write(intro)

def add_Background(filename,back):
	with open(filename, "a") as myfile:
		myfile.write(back)

def add_Metodology(filename,meto):
	with open(filename, "a") as myfile:
		myfile.write(meto)

def add_Results(filename,resu):
	with open(filename, "a") as myfile:
		myfile.write(resu)