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

	cmd_par = get_execute_command(path, env, cmd) # + " " + " ".join(params)
	print(params)
	proc = subprocess.Popen(cmd_par,stdout=subprocess.PIPE, stderr = subprocess.PIPE, shell=True, preexec_fn=os.setsid)
	#output = subprocess.check_output(('grep', 'process_name'), stdin=proc.stdout)
	
	for stdout_line in iter(proc.stdout.readline, ""):
		print(stdout_line)
	proc.stdout.close()
	return_code = proc.wait()
	if return_code:
		raise subprocess.CalledProcessError(return_code, cmd)

	print(output)

	#oldStdout = sys.stdout
	#try:
	#    os.remove(title + 'StatusMessages.txt')
	#except OSError:
	#    pass
	#sys.stdout = open(title + 'StatusMessages.txt', 'w+')
	#sys.stdout = oldStdout

	#outputArray = [param["value"] for param in params]
	#outputArray.append(sortedArray)

	#doThingsAfterTermination(outputArray, csvFields, csvFilename)