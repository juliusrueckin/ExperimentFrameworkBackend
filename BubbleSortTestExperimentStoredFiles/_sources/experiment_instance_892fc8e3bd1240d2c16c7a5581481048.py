from sacred import Experiment
from bubblesort_ingredient import data_ingredient, load_data
from operator import attrgetter

import random
import numpy as np
import outputHandler
import sys
import os
import subprocess

ex = Experiment('Experiment Framework', ingredients=[data_ingredient])

repetitionNumber = 1

def parse_params(params):
	parsedParams = ""
	print(len(params))
	for i in range(0,len(params)):
		parsedParams += str(params[i]["value"]) + " "

	return parsedParams

def get_execute_command(path, env, cmd):
    if path:
        return env + " cd " + path + " && " + cmd
    else:
        return env + " " + cmd

def setRepetitionNumber(repNum):
	global repetitionNumber
	repetitionNumber = repNum

#export results of experiment, if required
def doThingsAfterTermination(statusOutputFilePath, csvFields, csvFilename):
	if outputHandler.csvExportWanted(csvFields,csvFilename):
		filename = outputHandler.generateCSVFilename(csvFilename, repetitionNumber)
		outputHandler.exportInCSVFile(filename, statusOutputFilePath, csvFields)

#runs a single experiment instance in a subprocess
@ex.main
@ex.capture
def runExperimentInstance(params, csvFields, title, csvFilename, cmd, env, path):
	print("\nExperiment: " + title + "\n")

	statusOutputFilePath = title + 'StatusMessages.txt'

	#build execution command for experiment
	cmd_par = get_execute_command(path, env, cmd) + " " + parse_params(params)
	
	#open subprocess with built command and status messages output file as stdout
	proc = subprocess.Popen(cmd_par,stdout=open(statusOutputFilePath, 'w+'), stderr = open(title + 'StatusMessages.txt', 'w+'), shell=True, preexec_fn=os.setsid)
	
	proc.wait()
	
	doThingsAfterTermination(statusOutputFilePath, csvFields, csvFilename)