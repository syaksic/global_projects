#!/usr/bin/env python
"""
Enviroment for my own PhD experiments
"""
__author__ = """Sergio Yaksic <seanyabe@gmail.com>"""


from logger import logger
import os
import pickle

path='./temp/'
if not os.path.exists(path):
	os.makedirs(path)

from graph_theory import demo as graph_demo
from graph_theory import graph_utils 

def graph_demos(path):
	path=path+'graphs/'
	if not os.path.exists(path):
		os.makedirs(path)
	graph_size=100000
	#graph_demo.maindemo(graph_size,'demo',path)
	graph_demo.showdemo(path,'demo',{'log-log':True,
										'text':True,
										'assortativity':True,
										'degree_dist':False,
										'degree_dist_teo':False,
										'degree_correlations':False,
										'uncorrelated_prob':True,
										'teo_fit':True,
										'exp_fit':True})
	#Mean_demo 
	#number_of_executions=300 #use 0 to avoid this part
	#filename=str(number_of_executions)+'mean.bkp'
	#graph_demo.generatordemo(filename,number_of_executions,path,graph_size)
	#graph_demo.plotdemo(path,filename,{'log-log':True,
	#									'text':True,
	#									'assortativity':False,
	#									'degree_dist':True,
	#									'degree_dist_teo':True,
	#									'degree_correlations':False,
	#									'uncorrelated_prob':False,
	#									'teo_fit':False,
	#									'exp_fit':False})

graph_demos(path)








def Logger_Generator_Demo(path):
	logger.demo(path)
#Logger_Generator_Demo('./temp/logger/')#DESCOMENTAR PARA USAR


def Degree_Inform_generator(degree_dist_path,filename,out_path):
	if not os.path.exists(out_path):
		os.makedirs(out_path)
	with open(degree_dist_path+'degree_distribution'+filename, 'rb') as f:
		degree_distribution=pickle.load(f)
	with open(degree_dist_path+'degree_correlations'+filename, 'rb') as f:
		degree_correlations=pickle.load(f)

	logger.Inform.append('''
\documentclass{beamer}
\usepackage{subcaption}
\usepackage{float}
\usepackage{graphicx}
\usefonttheme[onlymath]{serif}

\usetheme{Warsaw}

\\bibliographystyle{ieeetr}
\hypersetup{pdfstartview={Fit}} 
\setbeamertemplate{footline}[frame number]
\\beamersetuncovermixins{\opaqueness<1>{25}}{\opaqueness<2->{15}}
\\begin{document}
	''')
	logger.add_text('\\title{Graph Analysis}')
	logger.add_text('\\author{Sergio Yaksic}')
	logger.add_text('\date{\\today}')
	logger.add_paragraph('''
\\begin{frame}
\\titlepage
\end{frame}
	''')
	logger.add_text('\section{Abstract}') 
	logger.add_paragraph('''
\\begin{frame}\\frametitle{Abstract}

Using a python program, an statistical analysis about the connectivity patterns over scale-free graphs is presented. 
We compare our statistical results with the theoretical degree distribution $P(k)$ and degree-degree correlation function $P(k|x)$ 

\end{frame}
	''')
	logger.add_text('\section{Degree Distribution}') 
	graph_utils.plot(degree_distribution,degree_correlations,{'log-log':False,
								'text':False,
								'assortativity':False,
								'degree_dist':True,
								'degree_dist_teo':True,
								'degree_correlations':False,
								'uncorrelated_prob':False,
								'teo_fit':False,
								'exp_fit':False},out_path,'Image01')
	logger.add_paragraph('''
\\begin{frame}\\frametitle{Degree Distribution}

\\begin{figure}[hbt!]
%\caption{barabasi-albert-graph(100000,3)}\n'''+
'\includegraphics[width=0.8\\textwidth]{'+out_path+'Image01.eps}\n'+
'''
\end{figure}


Here is a plot of the degree distribution of a barabasi-albert graph. The yellow squares represent the statistical probability of choosing a node of degree $k$.

\end{frame}
	''')
	logger.add_text('\subsection{Power law Distribution}') 
	graph_utils.plot(degree_distribution,degree_correlations,{'log-log':True,
								'text':False,
								'assortativity':False,
								'degree_dist':True,
								'degree_dist_teo':True,
								'degree_correlations':False,
								'uncorrelated_prob':False,
								'teo_fit':False,
								'exp_fit':False},out_path,'Image02')
	logger.add_paragraph('''
\\begin{frame}\\frametitle{Power law Distribution}
\\begin{columns}
\\begin{column}{6.5cm}
\\begin{figure}[hbt!]
%\caption{barabasi-albert-graph(100000,3)}\n'''+
'\includegraphics[width=1.0\\textwidth]{'+out_path+'Image02.eps}\n'+
'''
\end{figure}
\end{column}
\\begin{column}{3.5cm}
\\begin{equation}
\label{eq:degree_dist}
P(k)=Ck{-\gamma}
\end{equation}
\end{column}
\end{columns}


The blue line represents the best fit (the one that minimizes the sum of squared errors) for theoretical equation \\ref{eq:degree_dist}.


\end{frame}
	''')
	logger.add_text('\section{Degree-degree correlation function}') 
	logger.add_paragraph('''
\\begin{frame}\\frametitle{Degree-degree correlation function}


Using equation \\ref{eq:degree-degree_correlation} presented by vespignati we plotted the degree-degree correlation function, that is the probability of choosing a node of degree $k$ connected to a node of degree $x$.


\\begin{equation}
\label{eq:degree-degree_correlation}
P(k|x)=\\frac{kP(k)}{\langle k \\rangle}=\\frac{kCk{-\gamma}}{\langle k \\rangle}
\end{equation}

\end{frame}
	''')
	logger.add_text('\subsection{Theoretical $P(k|x)$}') 
	graph_utils.plot(degree_distribution,degree_correlations,{'log-log':True,
								'text':True,
								'assortativity':True,
								'degree_dist':False,
								'degree_dist_teo':True,
								'degree_correlations':True,
								'uncorrelated_prob':False,
								'teo_fit':True,
								'exp_fit':True},out_path,'Image03')
	logger.add_paragraph('''
\\begin{frame}\\frametitle{Theoretical $P(k|x)$}
Theoretical $P(k|x)$ using the parameters of blue curve $P(k)$ and $P(k|x=\langle k \\rangle)$ as reference.

\\begin{figure}[hbt!]
%\caption{barabasi-albert-graph(100000,3)}\n'''+
'\includegraphics[width=0.8\\textwidth]{'+out_path+'Image03.eps}\n'+
'''
\end{figure}
\end{frame}
	''')

	logger.add_text('\end{document}')

	logger.generate(out_path+'logger.tex')
	logger.compile(out_path+'logger.tex',out_path)

#Degree_Inform_generator('./temp/exp/','test00000.bkp','./temp/exp/results/')



