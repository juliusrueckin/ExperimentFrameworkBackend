from sacred import Experiment
from bubblesort_ingredient import data_ingredient, load_data
from operator import attrgetter

import random
import numpy as np
import outputHandler
import sys
import os
import subprocess

ex = Experiment('Bubble Sort', ingredients=[data_ingredient])

repetitionNumber = 1

def parse_params(params):
	parsedParams = ""

	for i in range(len(params)):
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

def doThingsAfterTermination(outputArray, csvFields, csvFilename):
	#outputHandler.prettyPrintOutputToTerminal(outputArray)

	if outputHandler.csvExportWanted(csvFields,csvFilename):

		filename = outputHandler.generateCSVFilename(csvFilename, repetitionNumber)
		outputHandler.exportInCSVFile(filename, [outputArray], csvFields)

@ex.named_config
def bubbleSortConfig():
    
    title = "Bubble Sort Experiment"
    params = [{"name": "unsortedArray", "value": random.sample(range(1000000), 10000)}]
    csvFields = ["unsortedArray", "chaosMeasure", "sortedArray"]
    csvFilename = "output"

@ex.main
@ex.capture
def bubbleSort(params, csvFields, title, csvFilename, cmd, env, path):
	print("\nExperiment: " + title + "\n")

	# use given command param as input data file
	#inputData = params[0]["value"]

	# use ingredient dataset as a default input data file
	#inputData = load_data()

	try:
	    os.remove(title + 'StatusMessages.txt')
	except OSError:
	    pass

	cmd_par = get_execute_command(path, env, cmd) + " " + parse_params(params)
	print(cmd_par)
	
	proc = subprocess.Popen(cmd_par,stdout=open(title + 'StatusMessages.txt', 'w+'), stderr = open(title + 'StatusMessages.txt', 'w+'), shell=True, preexec_fn=os.setsid)
	
	proc.wait()

	output = [param["value"] for param in params]
	output.append([])

	doThingsAfterTermination(output, csvFields, csvFilename)