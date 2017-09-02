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

def sortArray(inputArray):
	x = 1
	for i in range(0, len(inputArray)):
		for j in range(0, len(inputArray)-1):
			if i * len(inputArray) >= ((len(inputArray)**2) * (x/5)):
				print("Algorithm still working fine")
				x += 1

			if inputArray[j] > inputArray[j+1]:
				tmp = inputArray[j+1]
				inputArray[j+1] = inputArray[j]
				inputArray[j] = tmp

	return inputArray

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
	inputData = params[0]["value"]

	# use ingredient dataset as a default input data file
	#inputData = load_data()

	oldStdout = sys.stdout
	try:
	    os.remove(title + 'StatusMessages.txt')
	except OSError:
	    pass
	sys.stdout = open(title + 'StatusMessages.txt', 'w+')

	cmd_par = self.get_execute_command() # + " " + " ".join(params)
	proc = subprocess.Popen(cmd_par,stdout=subprocess.PIPE, stderr = subprocess.PIPE, shell=True, preexec_fn=os.setsid)

	sortedArray = sortArray(inputData)

	sys.stdout = oldStdout

	outputArray = [param["value"] for param in params]
	outputArray.append(sortedArray)

	doThingsAfterTermination(outputArray, csvFields, csvFilename)